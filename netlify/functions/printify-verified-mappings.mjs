const SHOP_ID='28816619';
const RULES=[
 ['Cream/Gold Crowned Luxury Full-Zip Hoodie','Cream-Gangster Bougie Crowned Luxury Full-Zip Hoodie'],
 ['Onyx/Gold Crowned Luxury Full-Zip Hoodie','Onyx/Gold-Gangster Bougie Crowned Luxury Full-Zip Hoodie'],
 ['Black Crowned Luxury Cotton Tee','Gangster Bougie Crowned Luxury Cotton Tee'],
 ['White Crowned Luxury Cotton Tee','Gangster Bougie Crowned Luxury Cotton Tee'],
 ['Crowned Luxury Crew Socks','Gangster Bougie Crowned Luxury Crew Socks']
];
function norm(v=''){return String(v).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
export default async(req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'GET'}});
 const token=process.env.PRINTIFY_API_TOKEN;if(!token)return Response.json({ok:false,error:'Printify API token is not configured.'},{status:500});
 try{
  const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=1`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});
  const p=await r.json().catch(()=>null);if(!r.ok)return Response.json({ok:false,error:'Printify lookup failed.',status:r.status},{status:502});
  const products=Array.isArray(p?.data)?p.data:(Array.isArray(p)?p:[]);
  const verified=RULES.map(([website_name,printify_title])=>{
   const x=products.find(p=>norm(p.title)===norm(printify_title));
   return {website_name,verified:!!x,printify_product:x?{id:x.id,title:x.title,print_provider_id:x.print_provider_id,blueprint_id:x.blueprint_id,enabled_variants:(x.variants||[]).filter(v=>v.is_enabled===true).map(v=>({id:v.id,title:v.title,sku:v.sku,cost:v.cost,is_available:v.is_available}))}:null};
  });
  const unresolved=verified.filter(x=>!x.verified);
  return Response.json({ok:true,mode:'verified_mapping_rules',shop_id:SHOP_ID,verified_count:verified.length-unresolved.length,unresolved_count:unresolved.length,note:'Read-only verification. No orders or storefront changes.',verified});
 }catch(e){console.error(e);return Response.json({ok:false,error:'Unable to verify mapping rules.'},{status:502});}
};