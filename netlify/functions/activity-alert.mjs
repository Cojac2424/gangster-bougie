import { sendAdminActivityAlert } from './lib/gb-email.mjs';

function clean(v,n=160){return String(v??'').replace(/[<>]/g,'').trim().slice(0,n)}
function sourceFrom(ref,explicit){
 const x=clean(explicit||'',80).toLowerCase();
 if(x)return clean(explicit,80);
 let host='';try{host=new URL(ref||'').hostname.toLowerCase()}catch(_){}
 if(/tiktok/.test(host))return 'TikTok';
 if(/instagram/.test(host))return 'Instagram';
 if(/facebook|fb\.com|l\.facebook/.test(host))return 'Facebook';
 if(/google/.test(host))return 'Google';
 return host?host:'Direct / Unknown';
}
export default async(req)=>{
 if(req.method!=='POST')return new Response('Method not allowed',{status:405,headers:{Allow:'POST'}});
 let body;try{body=await req.json()}catch(_){return Response.json({ok:false,error:'invalid_request'},{status:400})}
 const allowed=new Set(['visit','view_item','add_to_cart','begin_checkout']);
 if(!allowed.has(body.event))return Response.json({ok:false,error:'unsupported_event'},{status:400});
 const items=(Array.isArray(body.items)?body.items:[]).slice(0,20).map(x=>({name:clean(x.name||x.item_name,180),variant:clean(x.variant||x.item_variant||x.size,100),price:Number(x.price)||0,quantity:Math.max(1,Math.min(20,Number(x.quantity||x.qty)||1))}));
 const payload={event:body.event,source:sourceFrom(body.referrer,body.source),device:clean(body.device,100)||'Unknown device',browser:clean(body.browser,100)||'Unknown browser',items,value:body.value===null||body.value===undefined?null:Number(body.value)||0,currency:'USD',time:new Date().toISOString()};
 try{const sent=await sendAdminActivityAlert(payload);return Response.json({ok:!!sent.ok})}catch(e){console.error('GB ACTIVITY ALERT FAILED',String(e?.message||e));return Response.json({ok:false},{status:502})}
};