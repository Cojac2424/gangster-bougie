const SHOP_ID='28816619';
const TARGETS=[
 {website_name:'Stainless Steel Gym Bottle',keywords:['bottle']},
 {website_name:'Gym Face Towel',keywords:['face','towel']},
 {website_name:'Gym Bag',keywords:['gym','bag']},
 {website_name:'Foam Yoga Mat',keywords:['yoga','mat']},
 {website_name:'GB Faux Leather Travel Bag',keywords:['faux','leather','travel','bag']},
 {website_name:'“Baddie” Faux Leather Travel Bag',keywords:['faux','leather','travel','bag']},
 {website_name:'Mini Wrap Bandana',keywords:['bandana']},
 {website_name:'Embroidered Structured Cap',keywords:['structured','cap']},
 {website_name:'Crowned Luxury Signature Cap',keywords:['crowned','luxury','cap']},
 {website_name:'Crowned Luxury Crew Socks',keywords:['crowned','luxury','crew','socks']}
];
function norm(v=''){return String(v).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
async function all(token){let page=1,out=[];while(page<=20){const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=${page}`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});const p=await r.json();if(!r.ok)throw new Error(String(r.status));const b=Array.isArray(p?.data)?p.data:[];out.push(...b);if(page>=Number(p?.last_page||1)||!b.length)break;page++;}return out;}
function detail(p){return{printify_product_id:p.id,printify_title:p.title,print_provider_id:p.print_provider_id,blueprint_id:p.blueprint_id,variants:(p.variants||[]).filter(v=>v.is_enabled===true&&v.is_available!==false).map(v=>({id:v.id,title:v.title,sku:v.sku,cost:v.cost}))};}
export default async(req)=>{if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405});const token=process.env.PRINTIFY_API_TOKEN;if(!token)return Response.json({ok:false,error:'Token missing'},{status:500});try{const products=await all(token);const rows=TARGETS.map(t=>{const cs=products.filter(p=>{const n=norm(p.title);return t.keywords.every(k=>n.includes(norm(k)));});if(!cs.length)return{website_name:t.website_name,status:'product_not_found',candidate_count:0,candidates:[]};return{website_name:t.website_name,status:cs.length===1?'ready':'review_needed',candidate_count:cs.length,candidates:cs.map(detail)};});return Response.json({ok:true,mode:'accessories_full_candidate_variant_audit',note:'READY means product identity is unique; fulfillment is not complete until every storefront-selectable color/size is mapped to an exact product_id + variant_id.',total:rows.length,ready:rows.filter(x=>x.status==='ready').length,review_needed:rows.filter(x=>x.status!=='ready').length,rows});}catch(e){return Response.json({ok:false,error:'Unable to audit accessories.'},{status:502});}};

// Expanded accessories audit: returns every candidate and every enabled/available variant.
