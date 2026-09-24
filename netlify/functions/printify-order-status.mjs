// Printify status is exposed to customers only through the authenticated My Orders flow.
// This legacy public lookup is intentionally disabled so arbitrary Printify order IDs cannot be queried.
export default async(req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'GET'}});
 return Response.json({error:'Direct order-status lookup is disabled. Use My Orders.'},{status:404});
};
