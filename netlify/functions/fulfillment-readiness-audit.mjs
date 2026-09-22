import { resolveFulfillment } from './lib/fulfillment-resolver.mjs';
import { VERIFIED_ACTIVEWEAR_PRODUCTS } from './lib/verified-activewear-fulfillment.mjs';
import { VERIFIED_MENS_PRODUCTS } from './lib/verified-mens-fulfillment.mjs';
import { VERIFIED_ACCESSORIES_PRODUCTS, VERIFIED_TRAVEL_BAGS } from './lib/verified-accessories-fulfillment.mjs';

function testsFrom(group){
 const out=[];
 for(const [name,p] of Object.entries(group)){
   if(p.sizes) for(const s of Object.keys(p.sizes)) out.push([name,s]);
   else if(p.colors) for(const color of Object.keys(p.colors)) out.push([name,color]);
   else out.push([name,'One Size']);
 }
 return out;
}
export default async(req)=>{
 if(req.method!=='GET') return Response.json({error:'Method not allowed'},{status:405});
 const tests=[...testsFrom(VERIFIED_ACTIVEWEAR_PRODUCTS),...testsFrom(VERIFIED_MENS_PRODUCTS),...testsFrom(VERIFIED_ACCESSORIES_PRODUCTS),...testsFrom(VERIFIED_TRAVEL_BAGS)];
 const results=tests.map(([name,option])=>({name,option,...resolveFulfillment(name,option)}));
 const failed=results.filter(x=>!x.ok);
 return Response.json({ok:failed.length===0,mode:'exact_fulfillment_readiness',unique_storefront_groups:{women:Object.keys(VERIFIED_ACTIVEWEAR_PRODUCTS).length,men:Object.keys(VERIFIED_MENS_PRODUCTS).length,accessories:8},option_routes_tested:results.length,passed:results.length-failed.length,failed:failed.length,failures:failed});
};
