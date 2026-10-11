import { getAffiliateByCode } from './lib/gb-affiliate-store.mjs';
export default async(req)=>{
 if(req.method!=='GET')return new Response('Method not allowed',{status:405,headers:{Allow:'GET'}});
 const raw=new URL(req.url).searchParams.get('code')||'';
 const a=await getAffiliateByCode(raw);
 if(!a||a.status!=='active')return Response.json({valid:false},{status:404});
 return Response.json({valid:true,affiliate:{code:a.code,name:a.name,discount_percent:5}});
};