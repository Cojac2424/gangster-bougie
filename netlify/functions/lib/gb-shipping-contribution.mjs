// Shared planned customer shipping contributions; costs are in USD cents.
export function customerShippingContribution(name){
 const n=String(name||'');
 if(/Full-Zip Hoodie|Faux Leather Travel Bag/.test(n))return 0;
 if(/Gym Face Towel/.test(n))return 249;
 if(/Sports Bra|Baby Bougie Tee|Cotton Tee|Signature Cap|Gym Bag|Structured Cap/.test(n))return 299;
 if(/Leggings|Mini Wrap Bandana/.test(n))return 399;
 if(/Workout Shorts|^Shorts – |Basketball Rib Shorts|Crew Socks|Gym Bottle|Yoga Mat/.test(n))return 499;
 return null;
}
