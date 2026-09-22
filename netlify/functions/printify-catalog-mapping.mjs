const SHOP_ID='28816619';
const WEBSITE_HINTS=[
 'Crowned Luxury','Basketball Rib Shorts','Full-Zip Hoodie','Sports Bra','High-Waisted Leggings',
 'Workout Shorts','Baby Bougie','Gym Bag','Gym Face Towel','Yoga Mat','Stainless Steel Gym Bottle',
 'Faux Leather','Bandana','Structured Cap'
];
function norm(v=''){return String(v).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
function category(title=''){
 const n=norm(title);
 for(const h of WEBSITE_HINTS)if(n.includes(norm(h)))return h;
 return 'Other';
}
export default async(req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'GET'}});
 const token=process.env.PRINTIFY_API_TOKEN;
 if(!token)return Response.json({ok:false,error:'Printify API token is not configured.'},{status:500});
 try{
  const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=1`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});
  const payload=await r.json().catch(()=>null);
  if(!r.ok)return Response.json({ok:false,error:'Printify product lookup failed.',status:r.status},{status:502});
  const products=Array.isArray(payload?.data)?payload.data:(Array.isArray(payload)?payload:[]);
  const inventory=products.map(p=>{
   const enabled=(p.variants||[]).filter(v=>v.is_enabled===true);
   const available=enabled.filter(v=>v.is_available!==false);
   return{
    printify_product_id:p.id,title:p.title,category_hint:category(p.title),
    blueprint_id:p.blueprint_id,print_provider_id:p.print_provider_id,
    enabled_variants:enabled.length,available_enabled_variants:available.length,
    variants:available.map(v=>({id:v.id,title:v.title,sku:v.sku,cost:v.cost}))
   };
  });
  const flagged=inventory.filter(p=>p.enabled_variants===0||p.available_enabled_variants<p.enabled_variants)
    .map(p=>({printify_product_id:p.printify_product_id,title:p.title,enabled_variants:p.enabled_variants,available_enabled_variants:p.available_enabled_variants}));
  return Response.json({ok:true,mode:'catalog_mapping_inventory',shop_id:SHOP_ID,product_count:inventory.length,flagged_count:flagged.length,flagged,products:inventory});
 }catch(e){console.error('Printify catalog mapping inventory error',e);return Response.json({ok:false,error:'Unable to build catalog mapping inventory.'},{status:502});}
};