// Temporary authenticated admin helper for installing/testing the Printify shipment webhook.
// Remove after successful setup. Uses secrets already stored in Netlify.
const SHOP_ID=String(process.env.PRINTIFY_SHOP_ID||'28816619');
const API='https://api.printify.com/v1';
const TOPIC='order:shipment:created';
function auth(req){const expected=process.env.PRINTIFY_WEBHOOK_SECRET||'';const got=String(req.headers.get('x-gb-admin-secret')||'');return expected&&got&&got===expected}
async function pf(path,options={}){
 const token=process.env.PRINTIFY_API_TOKEN;if(!token)throw new Error('printify_token_missing');
 const r=await fetch(API+path,{...options,headers:{Authorization:'Bearer '+token,'Content-Type':'application/json',...(options.headers||{})}});
 const text=await r.text();let data;try{data=text?JSON.parse(text):null}catch(_){data={raw:text}}
 if(!r.ok){const e=new Error('printify_'+r.status);e.status=r.status;e.data=data;throw e}return data;
}
export default async(req)=>{
 if(req.method!=='POST')return Response.json({error:'Method not allowed.'},{status:405,headers:{Allow:'POST'}});
 if(!auth(req))return Response.json({error:'Unauthorized.'},{status:401});
 let body={};try{body=await req.json()}catch(_){}
 const action=String(body.action||'');
 try{
  if(action==='install'){
   const origin=new URL(req.url).origin;
   const url=origin+'/.netlify/functions/printify-shipment-webhook';
   const hooks=await pf('/shops/'+encodeURIComponent(SHOP_ID)+'/webhooks.json');
   let hook=(Array.isArray(hooks)?hooks:[]).find(x=>x.topic===TOPIC&&x.url===url);
   if(!hook)hook=await pf('/shops/'+encodeURIComponent(SHOP_ID)+'/webhooks.json',{method:'POST',body:JSON.stringify({topic:TOPIC,url,secret:process.env.PRINTIFY_WEBHOOK_SECRET})});
   return Response.json({ok:true,installed:true,webhook:{id:hook.id,topic:hook.topic,url:hook.url,shop_id:hook.shop_id}});
  }
  if(action==='simulate'){
   const hooks=await pf('/shops/'+encodeURIComponent(SHOP_ID)+'/webhooks.json');
   const origin=new URL(req.url).origin,url=origin+'/.netlify/functions/printify-shipment-webhook';
   const hook=(Array.isArray(hooks)?hooks:[]).find(x=>x.topic===TOPIC&&x.url===url);
   if(!hook)return Response.json({error:'Webhook not installed.'},{status:404});
   // Printify simulation returns supplied data as resource data. This checks signed delivery/rejection safely.
   const result=await pf('/shops/'+encodeURIComponent(SHOP_ID)+'/webhooks/'+encodeURIComponent(hook.id)+'/simulate',{method:'POST',body:JSON.stringify({shop_id:Number(SHOP_ID),shipped_at:new Date().toISOString(),carrier:{code:'TEST',tracking_number:'GB-TRACKING-SIMULATION',tracking_url:'https://example.com/gb-tracking-test'},skus:['GB-TEST']})});
   return Response.json({ok:true,simulation_requested:true,webhook_id:hook.id,result});
  }
  if(action==='status'){
   const hooks=await pf('/shops/'+encodeURIComponent(SHOP_ID)+'/webhooks.json');
   return Response.json({ok:true,webhooks:(Array.isArray(hooks)?hooks:[]).filter(x=>x.topic===TOPIC).map(x=>({id:x.id,topic:x.topic,url:x.url,shop_id:x.shop_id}))});
  }
  return Response.json({error:'Unsupported action.'},{status:400});
 }catch(e){console.error('PRINTIFY WEBHOOK ADMIN FAILED',e);return Response.json({error:e.message,status:e.status||null,details:e.data||null},{status:502})}
};
