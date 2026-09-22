// Stripe webhook endpoint for Gangster Bougie.
// SECURITY: verifies Stripe's signature before accepting a payment event.
// SAFETY: does NOT create a Printify order yet.

const enc=new TextEncoder();
function hex(bytes){return [...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');}
function constantTime(a,b){
 if(a.length!==b.length)return false;
 let x=0;for(let i=0;i<a.length;i++)x|=a.charCodeAt(i)^b.charCodeAt(i);return x===0;
}
async function hmac(secret,payload){
 const key=await crypto.subtle.importKey('raw',enc.encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
 return hex(await crypto.subtle.sign('HMAC',key,enc.encode(payload)));
}
async function verify(raw,header,secret){
 const parts=String(header||'').split(',').map(x=>x.split('='));
 const t=parts.find(x=>x[0]==='t')?.[1];
 const sigs=parts.filter(x=>x[0]==='v1').map(x=>x[1]);
 if(!t||!sigs.length)return false;
 const age=Math.abs(Math.floor(Date.now()/1000)-Number(t));
 if(!Number.isFinite(age)||age>300)return false;
 const expected=await hmac(secret,t+'.'+raw);
 return sigs.some(s=>constantTime(expected,s));
}
export default async(req)=>{
 if(req.method!=='POST')return new Response('Method not allowed',{status:405,headers:{Allow:'POST'}});
 const secret=process.env.STRIPE_WEBHOOK_SECRET;
 if(!secret)return Response.json({error:'Webhook secret is not configured.'},{status:500});
 const raw=await req.text();
 if(!(await verify(raw,req.headers.get('stripe-signature'),secret)))return Response.json({error:'Invalid Stripe signature.'},{status:400});
 let event;try{event=JSON.parse(raw)}catch(_){return Response.json({error:'Invalid payload.'},{status:400})}
 if(event.type==='checkout.session.completed'){
   const s=event.data?.object||{};
   if(s.payment_status!=='paid')return Response.json({received:true,accepted:false,reason:'payment_not_paid'});
   console.log('VERIFIED PAID CHECKOUT',JSON.stringify({event_id:event.id,session_id:s.id,payment_status:s.payment_status,amount_total:s.amount_total,currency:s.currency,customer_email:s.customer_details?.email||s.customer_email||null,printify_order_created:false}));
   return Response.json({received:true,accepted:true,verified_paid:true,printify_order_created:false});
 }
 return Response.json({received:true,ignored:true,type:event.type});
};

// Branch deploy refresh after webhook secret configuration.
