import { resolveCart } from './lib/fulfillment-resolver.mjs';

const SHOP_ID='28816619';
const ALLOWED_COUNTRIES=new Set(['CA','US']);

function clean(v,n=120){return String(v||'').trim().slice(0,n)}

export default async (req) => {
  if(req.method!=='POST') return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'POST'}});
  if(!process.env.PRINTIFY_API_TOKEN) return Response.json({error:'Shipping calculator is not configured.'},{status:500});
  let body;
  try{body=await req.json()}catch(_){return Response.json({error:'Invalid request.'},{status:400})}
  if(!Array.isArray(body.items)||!body.items.length||body.items.length>50) return Response.json({error:'Your cart is empty or invalid.'},{status:400});

  const mapped=resolveCart(body.items);
  if(!mapped.ok) return Response.json({error:'One or more cart options are not ready for shipping.',unresolved:mapped.unresolved},{status:400});

  const a=body.address||{};
  const country=clean(a.country,2).toUpperCase();
  if(!ALLOWED_COUNTRIES.has(country)) return Response.json({error:'Shipping is currently available to Canada and the United States.'},{status:400});
  const address_to={
    first_name:clean(a.first_name)||'Customer',
    last_name:clean(a.last_name)||'-',
    email:clean(a.email,254)||'checkout@example.invalid',
    phone:clean(a.phone,40)||'Not provided',
    country,
    region:clean(a.region,80),
    address1:clean(a.address1,180),
    address2:clean(a.address2,180),
    city:clean(a.city,100),
    zip:clean(a.zip,30)
  };
  const missing=['region','address1','city','zip'].filter(k=>!address_to[k]);
  if(missing.length) return Response.json({error:'Please complete your shipping address.',missing},{status:400});

  const payload={
    line_items:mapped.items.map(x=>({product_id:x.product_id,variant_id:x.variant_id,quantity:x.quantity})),
    address_to
  };
  const r=await fetch('https://api.printify.com/v1/shops/'+SHOP_ID+'/orders/shipping.json',{
    method:'POST',
    headers:{Authorization:'Bearer '+process.env.PRINTIFY_API_TOKEN,'Content-Type':'application/json'},
    body:JSON.stringify(payload)
  });
  const d=await r.json().catch(()=>({}));
  if(!r.ok){
    console.error('Printify shipping quote failed',r.status,d);
    return Response.json({error:'Unable to calculate shipping for this address.'},{status:502});
  }
  const options={};
  for(const [name,cents] of Object.entries(d||{})){
    if(Number.isFinite(Number(cents))&&Number(cents)>=0) options[name]={amount:Number(cents),currency:'usd'};
  }
  if(!Object.keys(options).length) return Response.json({error:'No shipping method is available for this order.'},{status:422});
  return Response.json({options});
};
