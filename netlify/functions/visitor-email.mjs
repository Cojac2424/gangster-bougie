const RESEND_API='https://api.resend.com/emails';

function esc(v){
 return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function deviceFromUA(ua=''){
 const u=String(ua);
 if(/iPad/i.test(u)||(/Macintosh/i.test(u)&&/Mobile/i.test(u)))return 'iPad';
 if(/iPhone/i.test(u))return 'iPhone';
 if(/Android/i.test(u))return 'Android';
 if(/Mobi/i.test(u))return 'Mobile';
 return 'Desktop';
}
function sourceFromReferrer(ref=''){
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

export default async(req)=>{
 if(req.method!=='POST')return new Response('Method not allowed',{status:405,headers:{Allow:'POST'}});
 if(!sameSite(req))return Response.json({ok:false,error:'forbidden'},{status:403});
 let body={};
 try{body=await req.json();}catch{}
 const key=process.env.RESEND_API_KEY;
 if(!key){
  console.error('GB VISITOR EMAIL FAILED: RESEND_API_KEY missing');
  return Response.json({ok:false,error:'email_not_configured'},{status:500});
 }
 const to='gangsterbougie@gmail.com';
 const from=process.env.GB_EMAIL_FROM||'Gangster Bougie <onboarding@resend.dev>';
 const path=String(body.path||'/').slice(0,400);
 const referrer=String(body.referrer||'').slice(0,500);
 const source=sourceFromReferrer(referrer);
 const device=deviceFromUA(body.ua||req.headers.get('user-agent')||'');
 const time=new Date().toLocaleString('en-CA',{timeZone:'America/Toronto',year:'numeric',month:'short',day:'numeric',hour:'numeric',minute:'2-digit',second:'2-digit'});
 const subject='👀 Gangster Bougie website visitor';
 const html=`<div style="background:#070707;color:#fff;padding:26px;font-family:Arial,sans-serif"><div style="max-width:560px;margin:auto;border:1px solid #d8a928;border-radius:12px;padding:22px"><h2 style="margin-top:0;color:#d8a928">New Gangster Bougie Visitor</h2><p><strong>Time:</strong> ${esc(time)}</p><p><strong>Page:</strong> ${esc(path)}</p><p><strong>Source:</strong> ${esc(source)}</p><p><strong>Device:</strong> ${esc(device)}</p></div></div>`;
 const text=`New Gangster Bougie Visitor\nTime: ${time}\nPage: ${path}\nSource: ${source}\nDevice: ${device}`;
 try{
  const r=await fetch(RESEND_API,{method:'POST',headers:{Authorization:'Bearer '+key,'Content-Type':'application/json'},body:JSON.stringify({from,to:[to],subject,html,text})});
  const data=await r.json().catch(()=>({}));
  if(!r.ok)throw new Error('Resend rejected visitor email ('+r.status+'): '+JSON.stringify(data).slice(0,500));
  console.log('GB VISITOR EMAIL SENT',JSON.stringify({id:data.id||null,to,source,device,path}));
  return Response.json({ok:true});
 }catch(e){
  console.error('GB VISITOR EMAIL FAILED',String(e?.message||e));
  return Response.json({ok:false,error:'send_failed'},{status:502});
 }
};