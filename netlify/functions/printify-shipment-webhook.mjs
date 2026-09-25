// Printify shipment webhook for Gangster Bougie.
// Receives signed order:shipment:created events, verifies the shipment against Printify,
// updates the existing GB order, and sends one tracking email.
import { getStore } from '@netlify/blobs';
import { getGbOrderByNumber, updateGbOrderTracking } from './lib/gb-order-store.mjs';
import { sendShippingConfirmation } from './lib/gb-email.mjs';

const SHOP_ID=String(process.env.PRINTIFY_SHOP_ID||'28816619');
const API='https://api.printify.com/v1';
const enc=new TextEncoder();

function timingSafe(a,b){
 const aa=new Uint8Array(a),bb=new Uint8Array(b); if(aa.length!==bb.length)return false;
 let x=0;for(let i=0;i<aa.length;i++)x|=aa[i]^bb[i];return x===0;
}
async function verifySignature(raw,header,secret){
 if(!secret||!header)return false;
 const key=await crypto.subtle.importKey('raw',enc.encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
 const sig=await crypto.subtle.sign('HMAC',key,enc.encode(raw));
 const hex=[...new Uint8Array(sig)].map(x=>x.toString(16).padStart(2,'0')).join('');
 const b64=btoa(String.fromCharCode(...new Uint8Array(sig)));
 const supplied=String(header).trim().replace(/^sha256=/i,'');
 return timingSafe(enc.encode(supplied),enc.encode(hex))||timingSafe(enc.encode(supplied),enc.encode(b64));
}
async function printifyOrder(id){
 const token=process.env.PRINTIFY_API_TOKEN;
 if(!token)throw new Error('printify_token_missing');
 const r=await fetch(`${API}/shops/${encodeURIComponent(SHOP_ID)}/orders/${encodeURIComponent(id)}.json`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie'}});
 if(!r.ok)throw new Error('printify_order_lookup_failed_'+r.status);
 return r.json();
}
function trackingFrom(order,payload){
 const p=payload?.resource?.data?.carrier||{};
 const shipments=Array.isArray(order?.shipments)?order.shipments:[];
 const s=shipments.find(x=>String(x?.number||'')===String(p.tracking_number||''))||shipments[0]||{};
 return {carrier:String(s.carrier||p.code||''),number:String(s.number||p.tracking_number||''),url:String(s.url||p.tracking_url||''),shipped_at:payload?.resource?.data?.shipped_at||null};
}

export default async(req)=>{
 if(req.method!=='POST')return Response.json({error:'Method not allowed.'},{status:405,headers:{Allow:'POST'}});
 const raw=await req.text(), secret=process.env.PRINTIFY_WEBHOOK_SECRET, signature=req.headers.get('x-pfy-signature')||req.headers.get('x-printify-signature');
 if(!await verifySignature(raw,signature,secret))return Response.json({error:'Invalid signature.'},{status:401});
 let event;try{event=JSON.parse(raw)}catch(_){return Response.json({error:'Invalid JSON.'},{status:400})}
 if(event?.type!=='order:shipment:created')return Response.json({received:true,ignored:true});
 if(String(event?.resource?.data?.shop_id||'')!==SHOP_ID)return Response.json({error:'Wrong shop.'},{status:403});
 const printifyId=String(event?.resource?.id||''); if(!printifyId)return Response.json({error:'Missing order.'},{status:400});
 let po;try{po=await printifyOrder(printifyId)}catch(e){console.error('PRINTIFY SHIPMENT LOOKUP FAILED',e);return Response.json({error:'Unable to verify shipment.'},{status:502})}
 const external=String(po?.external_id||po?.metadata?.shop_order_id||'');
 const store=getStore('gb-orders-v1');
 let orderNumber=await store.get('printify/'+encodeURIComponent(printifyId),{type:'text'}).catch(()=>null);
 if(!orderNumber&&external.startsWith('cs_'))orderNumber=await store.get('stripe/'+encodeURIComponent(external),{type:'text'}).catch(()=>null);
 if(!orderNumber)return Response.json({error:'Matching GB order not found.'},{status:404});
 const order=await getGbOrderByNumber(orderNumber);if(!order)return Response.json({error:'Matching GB order not found.'},{status:404});
 const tracking=trackingFrom(po,event);if(!tracking.number)return Response.json({error:'Tracking number unavailable.'},{status:409});
 const updated=await updateGbOrderTracking(orderNumber,{printify_order_id:printifyId,tracking});
 if(!updated.ok)return Response.json({error:updated.error},{status:500});
 if(!updated.already_notified){
  const sent=await sendShippingConfirmation(updated.record);
  if(!sent.ok){console.error('TRACKING EMAIL FAILED',{order_number:orderNumber,error:sent.error});return Response.json({error:'Tracking email failed.'},{status:502})}
  await updateGbOrderTracking(orderNumber,{tracking,tracking_email_sent_at:new Date().toISOString()});
 }
 return Response.json({received:true,accepted:true,order_number:orderNumber,tracking_saved:true});
};
