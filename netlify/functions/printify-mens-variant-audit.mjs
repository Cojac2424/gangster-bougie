const SHOP_ID='28816619';
const TARGETS=[
 {website_name:'Onyx/Gold Crowned Luxury Full-Zip Hoodie',titles:['Onyx/Gold-Gangster Bougie Crowned Luxury Full-Zip Hoodie'],sizes:['S','M','L','XL','2XL']},
 {website_name:'Cream/Gold Crowned Luxury Full-Zip Hoodie',titles:['Cream-Gangster Bougie Crowned Luxury Full-Zip Hoodie'],sizes:['S','M','L','XL','2XL']},
 {website_name:'Black Crowned Luxury Cotton Tee',titles:['Gangster Bougie Crowned Luxury Cotton Tee'],color:'Solid Black',sizes:['S','M','L','XL','2XL']},
 {website_name:'White Crowned Luxury Cotton Tee',titles:['Gangster Bougie Crowned Luxury Cotton Tee'],color:'Solid White',sizes:['S','M','L','XL','2XL']},
 {website_name:'Onyx/Gold Gangster Bougie Basketball Rib Shorts',keywords:['basketball','rib','shorts'],colorHints:['black','onyx'],sizes:['S','M','L','XL','2XL','XXL']},
 {website_name:'Cream/Gold Gangster Bougie Basketball Rib Shorts',keywords:['basketball','rib','shorts'],colorHints:['white','cream'],sizes:['S','M','L','XL','2XL','XXL']},
 {website_name:'Crowned Luxury Signature Cap',keywords:['crowned','luxury','cap'],one_size:true},
 {website_name:'Crowned Luxury Crew Socks',titles:['Gangster Bougie Crowned Luxury Crew Socks'],one_size:true}
];
function norm(v=''){return String(v).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
function sizeOf(title=''){const n=norm(title);for(const s of ['3xl','2xl','xxl','xl','xs','l','m','s'])if(new RegExp('(^| )'+s+'($| )').test(n))return s==='xxl'?'2XL':s.toUpperCase();return '';}
async function allProducts(token){let page=1,out=[];while(page<=20){const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=${page}`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});const p=await r.json().catch(()=>null);if(!r.ok)throw new Error(String(r.status));const b=Array.isArray(p?.data)?p.data:[];out.push(...b);const last=Number(p?.last_page||1);if(page>=last||!b.length)break;page++;}return out;}
function candidates(t,products){if(t.titles){const exact=products.filter(p=>t.titles.some(x=>norm(p.title)===norm(x)));if(exact.length)return exact;}return products.filter(p=>{const n=norm(p.title);return (t.keywords||[]).every(k=>n.includes(norm(k)));});}
export default async(req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405});
 const token=process.env.PRINTIFY_API_TOKEN;if(!token)return Response.json({ok:false,error:'Token missing'},{status:500});
 try{const products=await allProducts(token);const rows=TARGETS.map(t=>{let cs=candidates(t,products);if(t.colorHints&&cs.length>1){const colored=cs.filter(p=>t.colorHints.some(h=>norm(p.title).includes(norm(h))));if(colored.length)cs=colored;}const p=cs[0];if(!p)return{website_name:t.website_name,status:'product_not_found',candidates:[]};const enabled=(p.variants||[]).filter(v=>v.is_enabled===true&&v.is_available!==false);
 if(t.one_size){const v=enabled.find(v=>norm(v.title).includes('one size'))||enabled[0];return{website_name:t.website_name,status:v?'ready':'variant_review_needed',printify_product_id:p.id,printify_title:p.title,variant:v?{id:v.id,title:v.title,sku:v.sku,cost:v.cost}:null,candidate_count:cs.length};}
 const by={};for(const wanted of t.sizes){if(wanted==='XXL')continue;const v=enabled.find(v=>{const title=norm(v.title);const colorOK=!t.color||title.includes(norm(t.color));return colorOK&&sizeOf(v.title)===wanted;});by[wanted]=v?{id:v.id,title:v.title,sku:v.sku,cost:v.cost}:null;}const missing=Object.keys(by).filter(s=>!by[s]);return{website_name:t.website_name,status:missing.length?'variant_review_needed':'ready',printify_product_id:p.id,printify_title:p.title,missing_sizes:missing,variants_by_size:by,candidate_count:cs.length};});return Response.json({ok:true,mode:'mens_variant_audit',total:rows.length,ready:rows.filter(x=>x.status==='ready').length,review_needed:rows.filter(x=>x.status!=='ready').length,rows});}catch(e){return Response.json({ok:false,error:'Unable to audit mens variants.'},{status:502});}
};

// Mens audit branch test.
