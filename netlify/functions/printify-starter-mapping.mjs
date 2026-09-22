const SHOP_ID = '28816619';

const TARGETS = [
  { website_name:'Black Crowned Luxury Cotton Tee', printify_title_contains:'Crowned Luxury Cotton Tee', color:'Solid Black', sizes:['S','M','L','XL','2XL'] },
  { website_name:'White Crowned Luxury Cotton Tee', printify_title_contains:'Crowned Luxury Cotton Tee', color:'Solid White', sizes:['S','M','L','XL','2XL'] },
  { website_name:'Crowned Luxury Crew Socks', printify_title_contains:'Crowned Luxury Crew Socks', one_size:true }
];
function norm(v=''){return String(v).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
function parseVariant(title=''){const p=String(title).split('/').map(x=>x.trim());return{color:p[0]||'',size:p[1]||(p.length===1?p[0]:'')};}

export default async (req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'GET'}});
 const token=process.env.PRINTIFY_API_TOKEN;
 if(!token)return Response.json({ok:false,error:'Printify API token is not configured.'},{status:500});
 try{
  const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=1`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});
  const payload=await r.json().catch(()=>null);
  if(!r.ok)return Response.json({ok:false,error:'Printify product lookup failed.',status:r.status},{status:502});
  const products=Array.isArray(payload?.data)?payload.data:(Array.isArray(payload)?payload:[]);
  const mappings=TARGETS.map(target=>{
   const product=products.find(p=>norm(p.title).includes(norm(target.printify_title_contains)));
   if(!product)return{website_name:target.website_name,matched:false,reason:'Printify product not found'};
   const enabled=(product.variants||[]).filter(v=>v.is_enabled===true&&v.is_available!==false);
   if(target.one_size){
    const v=enabled.find(v=>norm(v.title).includes('one size'));
    return{website_name:target.website_name,matched:!!v,printify_product_id:product.id,print_provider_id:product.print_provider_id,variant:v?{id:v.id,title:v.title,sku:v.sku,cost:v.cost}:null};
   }
   const bySize={};
   for(const wantedSize of target.sizes){
    const v=enabled.find(v=>{const x=parseVariant(v.title);return norm(x.color)===norm(target.color)&&norm(x.size)===norm(wantedSize);});
    bySize[wantedSize]=v?{id:v.id,title:v.title,sku:v.sku,cost:v.cost}:null;
   }
   return{website_name:target.website_name,matched:Object.values(bySize).every(Boolean),printify_product_id:product.id,print_provider_id:product.print_provider_id,expected_color:target.color,variants_by_size:bySize};
  });
  return Response.json({ok:true,mode:'exact_variant_mapping_check',shop_id:SHOP_ID,mappings});
 }catch(e){console.error('Exact Printify mapping error',e);return Response.json({ok:false,error:'Unable to build exact variant mappings right now.'},{status:502});}
};
