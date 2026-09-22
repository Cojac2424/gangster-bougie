const SHOP_ID='28816619';

// Confirmed by the storefront/Printify review. This endpoint is read-only.
// It resolves exact Printify product IDs and enabled/available variant IDs,
// then checks that the expected storefront sizes exist before fulfillment is wired.
const TARGETS=[
 {website_name:'GB Classic Sports Bra – Cream',product_title:['GB Sports Bra-White'],sizes:['S','M','L','XL','2XL']},
 {website_name:'GB Classic Sports Bra – Red',product_title:['GB Sports Bra-Red'],sizes:['S','M','L','XL','2XL']},
 {website_name:'GB Classic Sports Bra – Blue',product_title:['GB Sports Bra-Midnight Navy'],sizes:['S','M','L','XL','2XL']},
 {website_name:'GB Classic Sports Bra – Green',product_title:['GB Sports Bra-Deep Forrest','GB Sports Bra-Deep Forest'],sizes:['S','M','L','XL','2XL']},
 {website_name:'GB Classic Sports Bra – Espresso',product_title:['GB Sports Bra-Espresso'],sizes:['S','M','L','XL','2XL']},
 {website_name:'Heritage Plaid Sports Bra',product_id:'6aa7383222602c5b46047903',sizes:['S','M','L','XL','2XL']},
 {website_name:'Heritage Plaid Leggings',product_id:'6aa73d67d0d6187b3a0f1a23',sizes:['XS','S','M','L','XL','2XL']},
 {website_name:'GB Classic High-Waisted Leggings – Green',product_title:['GB Classic High-Waisted Leggings – Deep Forrest','GB Classic High-Waisted Leggings – Deep Forest'],sizes:['XS','S','M','L','XL','2XL']},
 {website_name:'Shorts – Black',product_id:'6a9c474cc8dc7ed3a507b76f',sizes:['XS','S','M','L','XL']},
 {website_name:'Shorts – White',product_title:['White-Gangster Bougie Women’s Workout Shorts'],sizes:['XS','S','M','L','XL']}
];

function norm(v=''){return String(v).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
function variantSize(title=''){
 const parts=String(title).split('/').map(x=>x.trim()).filter(Boolean);
 const sizeTokens=['XS','S','M','L','XL','2XL','XXL','3XL'];
 for(let i=parts.length-1;i>=0;i--){const p=parts[i].toUpperCase().replace('XXL','2XL');if(sizeTokens.includes(p))return p;}
 const n=norm(title);
 for(const s of ['3xl','2xl','xxl','xl','xs','l','m','s'])if(new RegExp('(^| )'+s+'($| )').test(n))return s==='xxl'?'2XL':s.toUpperCase();
 return '';
}
async function allProducts(token){
 let page=1,out=[];
 while(page<=20){
  const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=${page}`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});
  const p=await r.json().catch(()=>null);if(!r.ok)throw new Error('Printify lookup '+r.status);
  const batch=Array.isArray(p?.data)?p.data:(Array.isArray(p)?p:[]);out.push(...batch);
  const last=Number(p?.last_page||1);if(page>=last||!batch.length)break;page++;
 }
 return out;
}
export default async(req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'GET'}});
 const token=process.env.PRINTIFY_API_TOKEN;if(!token)return Response.json({ok:false,error:'Printify API token is not configured.'},{status:500});
 try{
  const products=await allProducts(token);
  const mappings=TARGETS.map(t=>{
   const p=t.product_id?products.find(x=>x.id===t.product_id):products.find(x=>(t.product_title||[]).some(title=>norm(x.title)===norm(title)));
   if(!p)return{website_name:t.website_name,status:'product_not_found',expected_sizes:t.sizes};
   const enabled=(p.variants||[]).filter(v=>v.is_enabled===true&&v.is_available!==false);
   const variants_by_size={};
   for(const size of t.sizes){
    const v=enabled.find(v=>variantSize(v.title)===size);
    variants_by_size[size]=v?{id:v.id,title:v.title,sku:v.sku,cost:v.cost}:null;
   }
   const missing_sizes=t.sizes.filter(s=>!variants_by_size[s]);
   return{website_name:t.website_name,status:missing_sizes.length?'size_review_needed':'ready',printify_product_id:p.id,printify_title:p.title,print_provider_id:p.print_provider_id,blueprint_id:p.blueprint_id,expected_sizes:t.sizes,missing_sizes,variants_by_size};
  });
  return Response.json({ok:true,mode:'verified_activewear_variant_map',shop_id:SHOP_ID,total:mappings.length,ready:mappings.filter(x=>x.status==='ready').length,review_needed:mappings.filter(x=>x.status!=='ready').length,note:'Read-only. No orders are created.',mappings});
 }catch(e){console.error(e);return Response.json({ok:false,error:'Unable to build verified activewear variant map.'},{status:502});}
};

// Batched branch-deploy trigger.

// White-shorts correction branch test.
