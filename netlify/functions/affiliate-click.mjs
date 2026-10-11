import { recordAffiliateClick, getAffiliateByCode } from './lib/gb-affiliate-store.mjs';
export default async(req)=>{
 if(req.method!=='POST')return new Response('Method not allowed',{status:405,headers:{Allow:'POST'}});
 let body={};try{body=await req.json()}catch(_){}
 const a=await getAffiliateByCode(body.code);
 if(!a||a.status!=='active')return Response.json({ok:false},{status:404});
 await recordAffiliateClick({affiliateId:a.id,code:a.code});
 return Response.json({ok:true});
};