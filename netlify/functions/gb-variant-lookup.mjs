// Temporary operator-only Printify product variant lookup.
// Disabled unless explicitly configured with a separate one-time lookup secret.
// Read-only: does not publish products or create orders.
const SHOP_ID='28816619';
const PRODUCTS=Object.freeze({
 black:'6aced4b5b92b4771540221b6',
 white:'6acecc7facbbb7449c0eda70'
});
const ALLOWED_SIZES=new Set(['XS','S','M','L','XL']);
export default async function handler(req){
 if(req.method!=='POST')return Response.json({error:'Not found'},{status:404});
 const secret=process.env.GB_VARIANT_LOOKUP_SECRET;
 const supplied=req.headers.get('x-gb-variant-lookup-secret')||'';
 if(!secret||!supplied||secret.length<32||supplied.length!==secret.length){
  return Response.json({error:'Not found'},{status:404});
 }
 const crypto=await import('node:crypto');
 if(!crypto.timingSafeEqual(Buffer.from(supplied),Buffer.from(secret))){
  return Response.json({error:'Not found'},{status:404});
 }
 const token=process.env.PRINTIFY_API_TOKEN;
 if(!token)return Response.json({error:'Printify not configured'},{status:503});
 const output={};
 for(const [color,id] of Object.entries(PRODUCTS)){
  const response=await fetch('https://api.printify.com/v1/shops/'+SHOP_ID+'/products/'+id+'.json',{
   headers:{Authorization:'Bearer '+token,Accept:'application/json'}
  });
  if(!response.ok)return Response.json({error:'Printify product lookup failed',color,status:response.status},{status:502});
  const product=await response.json();
  output[color]={product_id:id,variants:(product.variants||[]).filter(v=>v.is_enabled!==false).map(v=>({
   id:v.id,sku:v.sku,options:v.options,title:v.title,is_available:v.is_available
  }))};
 }
 return Response.json(output,{headers:{'Cache-Control':'no-store','X-Robots-Tag':'noindex'}});
}
