const PRICE_CENTS = Object.freeze({
  'Onyx Sports Bra':3999,'Cream Sports Bra':3999,'Oxblood Sports Bra':3999,'Heritage Plaid Sports Bra':3999,'Vault Sports Bra':3999,'Bougie Houndstooth Sports Bra':3999,
  'Cream Leggings':6999,'Oxblood Leggings':6999,'Onyx Leggings':6999,'Bougie Houndstooth Leggings':6999,'Vault Leggings':6999,'Heritage Plaid Leggings':6999,
  'Cream High-Waisted Leggings':6999,'Oxblood High-Waisted Leggings':6999,'Onyx High-Waisted Leggings':6999,'Bougie Houndstooth High-Waisted Leggings':6999,'Vault High-Waisted Leggings':6999,'Heritage Plaid High-Waisted Leggings':6999,
  'Cream Workout Shorts':5499,'Oxblood Workout Shorts':5499,'Onyx Workout Shorts':5499,'Bougie Houndstooth Workout Shorts':5499,'Vault Workout Shorts':5499,'Heritage Plaid Workout Shorts':5499,
  'GB Classic Sports Bra – Cream':3999,'GB Classic Sports Bra – Grey':3999,'GB Classic Sports Bra – Black':3999,'GB Classic Sports Bra – Blue':3999,'GB Classic Sports Bra – Green':3999,'GB Classic Sports Bra – Red':3999,'GB Classic Sports Bra – Espresso':3999,
  'GB Classic High-Waisted Leggings – Cream':6999,'GB Classic High-Waisted Leggings – Grey':6999,'GB Classic High-Waisted Leggings – Black':6999,'GB Classic High-Waisted Leggings – Blue':6999,'GB Classic High-Waisted Leggings – Green':6999,'GB Classic High-Waisted Leggings – Red':6999,'GB Classic High-Waisted Leggings – Espresso':6999,
  'Baby Bougie Tee – Caviar':4999,'Baby Bougie Tee – Cloud Dancer':4999,'Shorts – Black':5999,'Shorts – White':5999,
  'Onyx/Gold Crowned Luxury Full-Zip Hoodie':8999,'Cream/Gold Crowned Luxury Full-Zip Hoodie':8999,'Black Crowned Luxury Cotton Tee':3999,'White Crowned Luxury Cotton Tee':3999,
  'Onyx/Gold Gangster Bougie Basketball Rib Shorts':5799,'Cream/Gold Gangster Bougie Basketball Rib Shorts':5799,'Crowned Luxury Signature Cap':4999,'Crowned Luxury Crew Socks':1999,
  'Gangster Bougie Stainless Steel Gym Bottle':4999,'Stainless Steel Gym Bottle':4999,'Gangster Bougie Gym Face Towel':2499,'Gym Face Towel':2499,'Gangster Bougie Gym Bag':5499,'Gym Bag':5499,
  'Gangster Bougie Foam Yoga Mat':10999,'Foam Yoga Mat':10999,'Gangster Bougie GB Faux Leather Travel Bag':10999,'GB Faux Leather Travel Bag':10999,
  'Gangster Bougie “Baddie” Faux Leather Travel Bag':10999,'“Baddie” Faux Leather Travel Bag':10999,'Gangster Bougie Mini Wrap Bandana':2799,'Mini Wrap Bandana':2799,
  'Gangster Bougie Embroidered Structured Cap':3999,'Embroidered Structured Cap':3999
});
const VARIABLE_PRICES = Object.freeze({
  'Gangster Bougie Stainless Steel Gym Bottle': {'18 oz':5499},
  'Stainless Steel Gym Bottle': {'18 oz':5499}
});

function authoritativePrice(name,size){
  const variants=VARIABLE_PRICES[name];
  if(variants && size){
    for(const [needle,cents] of Object.entries(variants)) if(String(size).includes(needle)) return cents;
  }
  return PRICE_CENTS[name];
}
function safeOrigin(req){
  const raw=req.headers.get('origin')||process.env.URL||'';
  try{
    const u=new URL(raw);
    if(u.protocol==='https:'||u.hostname==='localhost'||u.hostname==='127.0.0.1') return u.origin;
  }catch(_){}
  return process.env.URL;
}
export default async (req) => {
  if(req.method!=='POST') return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'POST'}});
  if(!process.env.STRIPE_SECRET_KEY) return Response.json({error:'Stripe is not configured.'},{status:500});
  let body;
  try{ body=await req.json(); }catch(_){ return Response.json({error:'Invalid request.'},{status:400}); }
  if(!Array.isArray(body.items)||body.items.length<1||body.items.length>50) return Response.json({error:'Your cart is empty or invalid.'},{status:400});
  const items=[];
  for(const raw of body.items){
    const name=String(raw.name||'').trim(), size=String(raw.size||'').trim().slice(0,120);
    const quantity=Math.max(1,Math.min(20,Math.floor(Number(raw.qty)||1)));
    const unit_amount=authoritativePrice(name,size);
    if(!unit_amount) return Response.json({error:'An item in your cart is not available for checkout: '+name},{status:400});
    items.push({name,size,quantity,unit_amount});
  }
  const origin=safeOrigin(req);
  if(!origin) return Response.json({error:'Site URL is not configured.'},{status:500});
  const p=new URLSearchParams();
  p.set('mode','payment');
  p.set('success_url',origin+'/?checkout=success&session_id={CHECKOUT_SESSION_ID}');
  p.set('cancel_url',origin+'/?checkout=cancelled');
  p.set('billing_address_collection','auto');
  p.set('shipping_address_collection[allowed_countries][0]','CA');
  p.set('shipping_address_collection[allowed_countries][1]','US');
  items.forEach((x,i)=>{
    p.set(`line_items[${i}][quantity]`,String(x.quantity));
    p.set(`line_items[${i}][price_data][currency]`,'usd');
    p.set(`line_items[${i}][price_data][unit_amount]`,String(x.unit_amount));
    p.set(`line_items[${i}][price_data][product_data][name]`,x.name);
    if(x.size) p.set(`line_items[${i}][price_data][product_data][description]`,'Size / option: '+x.size);
  });
  const stripe=await fetch('https://api.stripe.com/v1/checkout/sessions',{
    method:'POST',
    headers:{Authorization:'Bearer '+process.env.STRIPE_SECRET_KEY,'Content-Type':'application/x-www-form-urlencoded'},
    body:p.toString()
  });
  const data=await stripe.json();
  if(!stripe.ok||!data.url){
    console.error('Stripe Checkout error',data&&data.error?data.error.message:'Unknown Stripe error');
    return Response.json({error:'Unable to start checkout right now.'},{status:502});
  }
  return Response.json({url:data.url});
};
