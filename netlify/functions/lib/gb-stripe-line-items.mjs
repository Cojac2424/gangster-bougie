// Retrieve every Stripe Checkout Session line item with expanded product metadata.
// Session retrieve normally exposes only the first handful; never drop items from
// fulfillment or affiliate accounting in larger mixed baskets.
export async function retrieveAllStripeLineItems(sessionId,secret,fetcher=fetch){
 const id=String(sessionId||'');
 if(!/^cs_(test_|live_)?[A-Za-z0-9]+$/.test(id)||!secret)throw Error('stripe_line_items_invalid_request');
 let next=null;const all=[];const seen=new Set();
 for(let page=0;page<5;page++){
  const params=new URLSearchParams({limit:'100'});
  params.append('expand[]','data.price.product');
  if(next)params.set('starting_after',next);
  const response=await fetcher('https://api.stripe.com/v1/checkout/sessions/'+encodeURIComponent(id)+'/line_items?'+params,{
    headers:{Authorization:'Bearer '+secret}
  });
  if(!response.ok)throw Error('stripe_line_items_http_'+response.status);
  const value=await response.json();
  if(!Array.isArray(value?.data)||typeof value.has_more!=='boolean')throw Error('stripe_line_items_invalid_response');
  for(const item of value.data){
   if(!item?.id||seen.has(item.id)||!item.price||!item.price.product||typeof item.price.product!=='object')
    throw Error('stripe_line_items_missing_product_metadata');
   if(!Number.isSafeInteger(item.quantity)||item.quantity<1)throw Error('stripe_line_items_invalid_quantity');
   all.push(item);seen.add(item.id);
  }
  if(all.length>100)throw Error('stripe_line_items_excessive');
  if(!value.has_more)return all;
  next=value.data.at(-1)?.id;
  if(!next||value.data.length===0)throw Error('stripe_line_items_pagination_failed');
 }
 throw Error('stripe_line_items_pagination_limit');
}
