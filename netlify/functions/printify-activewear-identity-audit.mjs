import { PRODUCT_IDENTITIES } from './lib/product-identities.mjs';
const SHOP_ID='28816619';
const SIZES=['XS','S','M','L','XL','2XL','3XL','XXL'];
function norm(v=''){return String(v).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
function tokens(v=''){return new Set(norm(v).split(' ').filter(Boolean));}
function overlap(a,b){const A=tokens(a),B=tokens(b);let n=0;for(const x of A)if(B.has(x))n++;return n;}
function aliases(identity){
 const d=identity.design.replaceAll('_',' ');
 const c=identity.collection.replaceAll('_',' ');
 const family=identity.family.replaceAll('_',' ');
 const out=[d,c,family];
 if(d==='onyx')out.push('black');
 if(d==='cream')out.push('white');
 if(d==='oxblood')out.push('red','dark red');
 if(d==='heritage plaid')out.push('plaid');
 if(d==='bougie houndstooth')out.push('houndstooth');
 return out;
}
function candidateScore(identity,p){
 const title=norm(p.title);let score=0;
 for(const a of aliases(identity)){if(title.includes(norm(a)))score+=a===identity.design.replaceAll('_',' ')?45:15;}
 score+=Math.min(30,overlap(identity.website_name,p.title)*6);
 return score;
}
export default async(req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'GET'}});
 const token=process.env.PRINTIFY_API_TOKEN;if(!token)return Response.json({ok:false,error:'Printify API token is not configured.'},{status:500});
 try{
  let page=1,products=[];
  while(page<=20){
   const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=${page}`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});
   const payload=await r.json();if(!r.ok)throw new Error(String(r.status));
   const batch=Array.isArray(payload?.data)?payload.data:[];products.push(...batch);
   const last=Number(payload?.last_page||1);if(page>=last||!batch.length)break;page++;
  }
  const rows=PRODUCT_IDENTITIES.map(identity=>{
   const candidates=products.map(p=>({score:candidateScore(identity,p),printify_product_id:p.id,title:p.title,print_provider_id:p.print_provider_id,blueprint_id:p.blueprint_id,
    variants:(p.variants||[]).filter(v=>v.is_enabled===true&&v.is_available!==false).map(v=>({id:v.id,title:v.title,sku:v.sku,cost:v.cost}))
   })).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,3);
   const top=candidates[0],second=candidates[1];
   const status=top&&top.score>=60&&(!second||top.score-second.score>=15)?'candidate_ready':'review_needed';
   return {...identity,status,candidates};
  });
  return Response.json({ok:true,mode:'activewear_identity_candidates',shop_id:SHOP_ID,website_product_count:rows.length,candidate_ready_count:rows.filter(x=>x.status==='candidate_ready').length,review_needed_count:rows.filter(x=>x.status==='review_needed').length,rows});
 }catch(e){console.error(e);return Response.json({ok:false,error:'Unable to audit activewear identities.'},{status:502});}
};
// Branch-deploy trigger: activewear mapping audit ready.
