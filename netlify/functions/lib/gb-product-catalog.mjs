// Authoritative Gangster Bougie checkout price and product-name allowlists.
// Shared by checkout and affiliate owner dashboard so new approved products appear in commission setup.
export const PRICE_CENTS=Object.freeze({'Onyx Sports Bra':2999,'Cream Sports Bra':2999,'Oxblood Sports Bra':2999,'Heritage Plaid Sports Bra':2999,'Vault Sports Bra':2999,'Bougie Houndstooth Sports Bra':2999,'Cream Leggings':5999,'Oxblood Leggings':5999,'Onyx Leggings':5999,'Bougie Houndstooth Leggings':5999,'Vault Leggings':5999,'Heritage Plaid Leggings':5999,'Cream High-Waisted Leggings':5999,'Oxblood High-Waisted Leggings':5999,'Onyx High-Waisted Leggings':5999,'Bougie Houndstooth High-Waisted Leggings':5999,'Vault High-Waisted Leggings':5999,'Heritage Plaid High-Waisted Leggings':5999,'Cream Workout Shorts':4999,'Oxblood Workout Shorts':4999,'Onyx Workout Shorts':4999,'Bougie Houndstooth Workout Shorts':4999,'Vault Workout Shorts':4999,'Heritage Plaid Workout Shorts':4999,'GB Classic Sports Bra – Cream':2999,'GB Classic Sports Bra – Grey':2999,'GB Classic Sports Bra – Black':2999,'GB Classic Sports Bra – Blue':2999,'GB Classic Sports Bra – Green':2999,'GB Classic Sports Bra – Red':2999,'GB Classic Sports Bra – Espresso':2999,'GB Classic High-Waisted Leggings – Cream':5999,'GB Classic High-Waisted Leggings – Grey':5999,'GB Classic High-Waisted Leggings – Black':5999,'GB Classic High-Waisted Leggings – Blue':5999,'GB Classic High-Waisted Leggings – Green':5999,'GB Classic High-Waisted Leggings – Red':5999,'GB Classic High-Waisted Leggings – Espresso':5999,'Gangster Bougie Women’s Signature Crop Tee – Black':3999,'Gangster Bougie Women’s Signature Crop Tee – White':3999,'Shorts – Black':4999,'Shorts – White':4999,'Onyx/Gold Crowned Luxury Full-Zip Hoodie':6999,'Cream/Gold Crowned Luxury Full-Zip Hoodie':6999,'Black Crowned Luxury Cotton Tee':2999,'White Crowned Luxury Cotton Tee':2999,'Onyx/Gold Gangster Bougie Basketball Rib Shorts':5999,'Cream/Gold Gangster Bougie Basketball Rib Shorts':5999,'Crowned Luxury Signature Cap':4499,'Crowned Luxury Crew Socks':2999,'Gangster Bougie Stainless Steel Gym Bottle':4499,'Stainless Steel Gym Bottle':4499,'Gangster Bougie Gym Face Towel':1999,'Gym Face Towel':1999,'Gangster Bougie Gym Bag':4999,'Gym Bag':4999,'Gangster Bougie Foam Yoga Mat':10499,'Foam Yoga Mat':10499,'Gangster Bougie GB Faux Leather Travel Bag':8499,'GB Faux Leather Travel Bag':8499,'Gangster Bougie “Baddie” Faux Leather Travel Bag':8499,'“Baddie” Faux Leather Travel Bag':8499,'Gangster Bougie Mini Wrap Bandana':2799,'Mini Wrap Bandana':2799,'Gangster Bougie Embroidered Structured Cap':3999,'Embroidered Structured Cap':3999});
export const VARIABLE_PRICES=Object.freeze({'Gangster Bougie Stainless Steel Gym Bottle':{'18 oz':4999},'Stainless Steel Gym Bottle':{'18 oz':4999}});
export const SELLABLE_PRODUCT_NAMES=Object.freeze(Object.keys(PRICE_CENTS).sort());

// Alternate storefront names refer to the same physical items. Commission is configured once.
// Older high-waisted descriptors remain in the checkout price list pending storefront cleanup;
// they do not have a separate verified Printify fulfillment mapping and are not payable SKUs.
export const COMMISSION_PRODUCT_ALIASES=Object.freeze({
  "Gangster Bougie Stainless Steel Gym Bottle": "Stainless Steel Gym Bottle",
  "Gangster Bougie Gym Face Towel": "Gym Face Towel",
  "Gangster Bougie Gym Bag": "Gym Bag",
  "Gangster Bougie Foam Yoga Mat": "Foam Yoga Mat",
  "Gangster Bougie GB Faux Leather Travel Bag": "GB Faux Leather Travel Bag",
  "Gangster Bougie “Baddie” Faux Leather Travel Bag": "“Baddie” Faux Leather Travel Bag",
  "Gangster Bougie Mini Wrap Bandana": "Mini Wrap Bandana",
  "Gangster Bougie Embroidered Structured Cap": "Embroidered Structured Cap"
});
export const AFFILIATE_LEGACY_UNMAPPED_NAMES=Object.freeze(["Cream High-Waisted Leggings","Oxblood High-Waisted Leggings","Onyx High-Waisted Leggings","Bougie Houndstooth High-Waisted Leggings","Vault High-Waisted Leggings","Heritage Plaid High-Waisted Leggings"]);
// All 52 distinct physical products still need individual cost and shipping verification.
// Women’s garments share a BASE production cost by type, regardless of pattern or colour.
// A common affiliate rate must be calculated against the LEAST profitable member of its family.
export const AFFILIATE_COST_PRODUCTS=Object.freeze(SELLABLE_PRODUCT_NAMES.filter(
 name=>!Object.hasOwn(COMMISSION_PRODUCT_ALIASES,name)&&!AFFILIATE_LEGACY_UNMAPPED_NAMES.includes(name)
));
export const AFFILIATE_RATE_GROUP_LABELS=Object.freeze({
 'Onyx Sports Bra':'Women’s Sports Bras — All Designs',
 'Onyx Leggings':'Women’s Leggings — All Designs',
 'Onyx Workout Shorts':'Women’s Workout Shorts — All Designs'
});
export function canonicalCommissionName(value){
 const raw=String(value||'').trim(),name=COMMISSION_PRODUCT_ALIASES[raw]||raw;
 if(!AFFILIATE_COST_PRODUCTS.includes(name))return name;
 if(name.endsWith('Sports Bra')||name.includes('Sports Bra – '))return 'Onyx Sports Bra';
 if(name.endsWith('Leggings'))return 'Onyx Leggings';
 if(name.endsWith('Workout Shorts')||name==='Shorts – Black'||name==='Shorts – White')return 'Onyx Workout Shorts';
 return name;
}
export const AFFILIATE_RATE_PRODUCTS=Object.freeze(
 [...new Set(AFFILIATE_COST_PRODUCTS.map(canonicalCommissionName))].sort()
);
export const AFFILIATE_RATE_MEMBERS=Object.freeze(Object.fromEntries(AFFILIATE_RATE_PRODUCTS.map(key=>[
 key,Object.freeze(AFFILIATE_COST_PRODUCTS.filter(name=>canonicalCommissionName(name)===key))
])));

