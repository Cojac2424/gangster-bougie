const SHOP_ID='28816619',PRODUCT_ID='6aa06ae32b7606c81303d5ee';
export default async(req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405});
 const token=process.env.PRINTIFY_API_TOKEN;if(!token)return Response.json({ok:false,error:'Token missing'},{status:500});
 try{
  const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products/${PRODUCT_ID}.json`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});
  const p=await r.json();if(!r.ok)throw new Error(String(r.status));
  const wanted=(p.variants||[]).filter(v=>/Caviar|Cloud Dancer/i.test(v.title)).map(v=>({id:v.id,title:v.title,cost:v.cost,is_enabled:v.is_enabled,is_available:v.is_available}));
  return Response.json({ok:true,product_id:p.id,title:p.title,variants:wanted});
 }catch(e){return Response.json({ok:false,error:'Unable to audit Baby Bougie tee variants.'},{status:502});}
};