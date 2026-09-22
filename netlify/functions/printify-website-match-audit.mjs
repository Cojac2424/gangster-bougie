const SHOP_ID='28816619';
const WEBSITE_PRODUCTS=["Onyx/Gold Crowned Luxury Full-Zip Hoodie","Black Crowned Luxury Cotton Tee","Cream/Gold Crowned Luxury Full-Zip Hoodie","White Crowned Luxury Cotton Tee","Onyx/Gold Gangster Bougie Basketball Rib Shorts","Cream/Gold Gangster Bougie Basketball Rib Shorts","Crowned Luxury Signature Cap","Crowned Luxury Crew Socks","Bougie Houndstooth Sports Bra","GB Classic Sports Bra – Grey","GB Classic High-Waisted Leggings – Grey","Stainless Steel Gym Bottle","Gym Face Towel","Gym Bag","GB Classic Sports Bra – Green","GB Classic High-Waisted Leggings – Green","Embroidered Structured Cap","“Baddie” Faux Leather Travel Bag","Onyx Sports Bra","Cream Sports Bra","Onyx Leggings","Cream Leggings","Baby Bougie Tee – Caviar","Baby Bougie Tee – Cloud Dancer","Shorts – Black","Shorts – White","Heritage Plaid Sports Bra","Heritage Plaid Leggings","Oxblood Sports Bra","Vault Sports Bra","GB Classic Sports Bra – Cream","GB Classic Sports Bra – Black","GB Classic Sports Bra – Blue","GB Classic Sports Bra – Red","GB Classic Sports Bra – Espresso","Onyx Workout Shorts","Cream Workout Shorts","Oxblood Leggings","Oxblood Workout Shorts","Heritage Plaid Workout Shorts","Vault Leggings","Vault Workout Shorts","Bougie Houndstooth Leggings","Bougie Houndstooth Workout Shorts","GB Classic High-Waisted Leggings – Cream","GB Classic High-Waisted Leggings – Black","GB Classic High-Waisted Leggings – Blue","GB Classic High-Waisted Leggings – Red","GB Classic High-Waisted Leggings – Espresso","Foam Yoga Mat","GB Faux Leather Travel Bag","Mini Wrap Bandana","Women’s Baby Tee","Gangster Bougie Women’s Luxe Bra","Gangster Bougie Sports Bra","Gangster Bougie Women’s Workout Shorts","Gangster Bougie High-Waisted Leggings","Women’s Laguna Cropped Hoodie"];
const STOP=new Set(['gangster','bougie','gb','the','and','womens','women','mens','men']);
function words(v=''){return new Set(String(v).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim().split(/\s+/).filter(x=>x&&!STOP.has(x)));}
function score(a,b){const A=words(a),B=words(b);if(!A.size||!B.size)return 0;let hit=0;for(const x of A)if(B.has(x))hit++;return Math.round((2*hit/(A.size+B.size))*100);}
export default async(req)=>{
 if(req.method!=='GET')return Response.json({error:'Method not allowed'},{status:405,headers:{Allow:'GET'}});
 const token=process.env.PRINTIFY_API_TOKEN;if(!token)return Response.json({ok:false,error:'Printify API token is not configured.'},{status:500});
 try{
  const r=await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=1`,{headers:{Authorization:'Bearer '+token,'User-Agent':'Gangster-Bougie-Netlify'}});
  const p=await r.json().catch(()=>null);if(!r.ok)return Response.json({ok:false,error:'Printify lookup failed.',status:r.status},{status:502});
  const products=Array.isArray(p?.data)?p.data:(Array.isArray(p)?p:[]);
  const results=WEBSITE_PRODUCTS.map(name=>{
   const candidates=products.map(x=>({score:score(name,x.title),printify_product_id:x.id,title:x.title,print_provider_id:x.print_provider_id,enabled_variants:(x.variants||[]).filter(v=>v.is_enabled===true).length})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,3);
   const top=candidates[0]||null, second=candidates[1]||null;
   const auto_confident=!!top&&top.score>=70&&(!second||top.score-second.score>=15);
   return{website_name:name,status:auto_confident?'strong_candidate':'review_needed',candidates};
  });
  return Response.json({ok:true,mode:'website_to_printify_candidate_audit',shop_id:SHOP_ID,website_product_count:WEBSITE_PRODUCTS.length,strong_candidate_count:results.filter(x=>x.status==='strong_candidate').length,review_needed_count:results.filter(x=>x.status==='review_needed').length,note:'Candidates only. No fulfillment mapping is written by this audit.',results});
 }catch(e){console.error(e);return Response.json({ok:false,error:'Unable to audit website-to-Printify candidates.'},{status:502});}
};