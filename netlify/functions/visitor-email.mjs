const RESEND_API='https://api.resend.com/emails';

function esc(v){
 return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function clean(v,n=300){return String(v??'').trim().slice(0,n)}
function deviceFromUA(ua=''){
 const u=String(ua);
 if(/iPad/i.test(u)||(/Macintosh/i.test(u)&&/Mobile/i.test(u)))return 'iPad';
 if(/iPhone/i.test(u))return 'iPhone';
 if(/Android/i.test(u))return 'Android';
 if(/Mobi/i.test(u))return 'Mobile';
 return 'Desktop';
}
function sourceFrom(ref='',explicit=''){
 const x=clean(explicit,100);
 if(x)return x;
 let host='';
 try{host=new URL(ref).hostname.toLowerCase();}catch{}
 if(!host)return 'Direct / Unknown';
 if(host.includes('tiktok'))return 'TikTok';
 if(host.includes('instagram'))return 'Instagram';
 if(host.includes('facebook')||host==='fb.com'||host.includes('l.facebook'))return 'Facebook';
 if(host.includes('google'))return 'Google';
 return host;
}
function sameSite(req){
 const origin=String(req.headers.get('origin')||'').trim();
 if(!origin)return true;
 const host=String(req.headers.get('x-forwarded-host')||req.headers.get('host')||'').split(',')[0].trim().toLowerCase();
 if(!host)return true;
 try{return new URL(origin).host.toLowerCase()===host;}catch{return false;}
}
function money(v,currency='USD'){
 const n=Number(v);
 return Number.isFinite(n)?n.toLocaleString('en-US',{style:'currency',currency}):'';
}
function normalizedItems(items){
 return (Array.isArray(items)?items:[]).slice(0,30).map(x=>({
  name:clean(x.name||x.item_name||'Item',180),
  variant:clean(x.variant||x.item_variant||x.size||x.selection||'',100),
  price:Number(x.price)||0,
  quantity:Math.max(1,Math.min(50,Number(x.quantity||x.qty)||1))
 }));
}
function labels(event){
 return {
  visit:{subject:'👀 Gangster Bougie website visitor',title:'New Gangster Bougie Visitor'},
  view_item:{subject:'🔥 Gangster Bougie product viewed',title:'Product Viewed'},
  add_to_cart:{subject:'🛒 Gangster Bougie added to cart',title:'Added to Cart'},
  begin_checkout:{subject:'💳 Gangster Bougie checkout started',title:'Checkout Started'},
  purchase:{subject:'💰 Gangster Bougie SALE',title:'Verified Purchase'}
 }[event]||{subject:'Gangster Bougie activity',title:'Gangster Bougie Activity'};
}

export async function sendGangsterBougieActivityEmail({
 event='visit',path='/',referrer='',source='',ua='',device='',items=[],value=null,currency='USD',orderNumber='',customerEmail=''
}={}){
 const key=process.env.RESEND_API_KEY;
 if(!key)throw new Error('RESEND_API_KEY is not configured');
 const to='gangsterbougie@gmail.com';
 const from=process.env.GB_EMAIL_FROM||'Gangster Bougie <onboarding@resend.dev>';
 const safeItems=normalizedItems(items);
 const src=sourceFrom(referrer,source);
 const dev=clean(device,100)||deviceFromUA(ua);
 const time=new Date().toLocaleString('en-CA',{timeZone:'America/Toronto',year:'numeric',month:'short',day:'numeric',hour:'numeric',minute:'2-digit',second:'2-digit'});
 const label=labels(event);
 const first=safeItems[0]?.name;
 const subject=label.subject+(first&&['view_item','add_to_cart'].includes(event)?' — '+first:orderNumber?' — '+orderNumber:'');
 const rows=safeItems.map(x=>`<tr><td style="padding:7px 10px 7px 0">${esc(x.name)}${x.variant?' — '+esc(x.variant):''}</td><td style="padding:7px 0;text-align:right">× ${esc(x.quantity)}${x.price?' · '+esc(money(x.price,currency)):''}</td></tr>`).join('');
 const html=`<div style="background:#070707;color:#fff;padding:26px;font-family:Arial,sans-serif"><div style="max-width:600px;margin:auto;border:1px solid #d8a928;border-radius:12px;padding:22px"><h2 style="margin-top:0;color:#d8a928">${esc(label.title)}</h2>${orderNumber?`<p><strong>Order:</strong> ${esc(orderNumber)}</p>`:''}${customerEmail?`<p><strong>Customer:</strong> ${esc(customerEmail)}</p>`:''}<p><strong>Time:</strong> ${esc(time)}</p><p><strong>Page:</strong> ${esc(path||'/')}</p><p><strong>Source:</strong> ${esc(src)}</p><p><strong>Device:</strong> ${esc(dev)}</p>${rows?`<table style="width:100%;border-collapse:collapse;color:#fff">${rows}</table>`:''}${value!==null?`<p><strong>Total:</strong> ${esc(money(value,currency))}</p>`:''}</div></div>`;
 const text=[
  label.title,
  orderNumber?'Order: '+orderNumber:'',
  customerEmail?'Customer: '+customerEmail:'',
  'Time: '+time,
  'Page: '+(path||'/'),
  'Source: '+src,
  'Device: '+dev,
  ...safeItems.map(x=>x.name+(x.variant?' — '+x.variant:'')+' × '+x.quantity+(x.price?' · '+money(x.price,currency):'')),
  value!==null?'Total: '+money(value,currency):''
 ].filter(Boolean).join('\n');
 const r=await fetch(RESEND_API,{method:'POST',headers:{Authorization:'Bearer '+key,'Content-Type':'application/json'},body:JSON.stringify({from,to:[to],subject,html,text})});
 const data=await r.json().catch(()=>({}));
 if(!r.ok)throw new Error('Resend rejected activity email ('+r.status+'): '+JSON.stringify(data).slice(0,500));
 console.log('GB ACTIVITY EMAIL SENT',JSON.stringify({event,id:data.id||null,to,source:src,device:dev,orderNumber:orderNumber||null}));
 return {ok:true,id:data.id||null};
}

export default async(req)=>{
 if(req.method!=='POST')return new Response('Method not allowed',{status:405,headers:{Allow:'POST'}});
 if(!sameSite(req))return Response.json({ok:false,error:'forbidden'},{status:403});
 let body={};try{body=await req.json();}catch{return Response.json({ok:false,error:'invalid_request'},{status:400})}
 const allowed=new Set(['visit','view_item','add_to_cart','begin_checkout']);
 if(!allowed.has(body.event))return Response.json({ok:false,error:'unsupported_event'},{status:400});
 try{
  await sendGangsterBougieActivityEmail({
   event:body.event,
   path:clean(body.path||'/',400),
   referrer:clean(body.referrer||'',500),
   source:clean(body.source||'',100),
   ua:clean(body.ua||req.headers.get('user-agent')||'',500),
   items:body.items,
   value:body.value===null||body.value===undefined?null:Number(body.value)||0,
   currency:'USD'
  });
  return Response.json({ok:true});
 }catch(e){
  console.error('GB ACTIVITY EMAIL FAILED',JSON.stringify({event:body.event,error:String(e?.message||e)}));
  return Response.json({ok:false,error:'send_failed'},{status:502});
 }
};