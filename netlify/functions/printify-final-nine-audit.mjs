const SHOP_ID='28816619';
const TARGETS=[
 ['GB Classic Sports Bra – Grey',['sports bra','grey']],
 ['GB Classic High-Waisted Leggings – Grey',['classic','legging','grey']],
 ['GB Classic Sports Bra – Black',['sports bra','black']],
 ['Women’s Baby Tee',['women','baby tee']],
 ['Gangster Bougie Women’s Luxe Bra',['luxe bra']],
 ['Gangster Bougie Sports Bra',['sports bra']],
 ['Gangster Bougie Women’s Workout Shorts',['workout shorts']],
 ['Gangster Bougie High-Waisted Leggings',['high waisted leggings']],
 ['Women’s Laguna Cropped Hoodie',['cropped hoodie']]
];
const norm=v=>String(v||'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
async function all(token){let out=[];for(let page=1;page<=20;page++){const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=${page}`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});const p=await r.json();if(!r.ok)throw new Error(String(r.status));const b=Array.isArray(p?.data)?p.data:[];out.push(...b);if(page>=Number(p?.last_page||1)||!b.length)break;}return out;}
const details=p=>({product_id:p.id,title:p.title,provider:p.print_provider_id,blueprint:p.blueprint_id,variants:(p.variants||[]).filter(v=>v.is_enabled===true).map(v=>({id:v.id,title:v.title,cost:v.cost,is_available:v.is_available}))});
export default async(req)=>{if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405});const token=process.env.PRINTIFY_API_TOKEN;if(!token)return Response.json({ok:false,error:'Token missing'},{status:500});try{const ps=await all(token);const rows=TARGETS.map(([website_name,terms])=>{let candidates=ps.filter(p=>terms.every(t=>norm(p.title).includes(norm(t))));if(!candidates.length){const family=terms[terms.length-1].split(' ').pop();candidates=ps.filter(p=>norm(p.title).includes(norm(family)));}return{website_name,candidate_count:candidates.length,status:candidates.length===1?'ready':candidates.length?'review_needed':'not_found',candidates:candidates.map(details)};});return Response.json({ok:true,mode:'final_nine_candidate_audit',total:rows.length,rows});}catch(e){return Response.json({ok:false,error:'Unable to audit final nine.'},{status:502});}};