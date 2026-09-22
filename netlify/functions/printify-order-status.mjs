// Read-only Printify order/tracking lookup.
// Requires PRINTIFY_API_TOKEN. Never creates, updates, or cancels an order.
const SHOP_ID='28816619';
export default async(req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'GET'}});
 const token=process.env.PRINTIFY_API_TOKEN;
 if(!token)return Response.json({error:'Printify is not configured.'},{status:500});
 const u=new URL(req.url), id=String(u.searchParams.get('order_id')||'').trim();
 if(!/^[A-Za-z0-9_-]{6,100}$/.test(id))return Response.json({error:'A valid order_id is required.'},{status:400});
 const r=await fetch('https://api.printify.com/v1/shops/'+SHOP_ID+'/orders/'+encodeURIComponent(id)+'.json',{headers:{Authorization:'Bearer '+token}});
 const d=await r.json().catch(()=>({}));
 if(!r.ok)return Response.json({error:'Unable to retrieve order status.',status:r.status},{status:r.status===404?404:502});
 const shipments=Array.isArray(d.shipments)?d.shipments:[];
 return Response.json({
   ok:true,order_id:d.id||id,status:d.status||null,created_at:d.created_at||null,updated_at:d.updated_at||null,
   shipments:shipments.map(x=>({carrier:x.carrier||null,number:x.number||x.tracking_number||null,url:x.url||x.tracking_url||null,delivered_at:x.delivered_at||null}))
 });
};
