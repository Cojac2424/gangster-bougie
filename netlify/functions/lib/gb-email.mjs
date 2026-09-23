// Gangster Bougie transactional email sender via Resend.
// Server-side only. RESEND_API_KEY never reaches the browser.
const API='https://api.resend.com/emails';
function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function from(){return process.env.GB_EMAIL_FROM||'Gangster Bougie <onboarding@resend.dev>'}
async function send({to,subject,html}){
 const key=process.env.RESEND_API_KEY;
 if(!key)return {ok:false,error:'resend_not_configured'};
 const r=await fetch(API,{method:'POST',headers:{Authorization:'Bearer '+key,'Content-Type':'application/json'},body:JSON.stringify({from:from(),to:[to],subject,html})});
 const d=await r.json().catch(()=>({}));
 if(!r.ok)return {ok:false,error:'resend_send_failed',status:r.status,details:d};
 return {ok:true,id:d.id||null};
}
export async function sendVerificationCode({to,code}){
 return send({to,subject:'Your Gangster Bougie verification code',html:`<div style="background:#070707;color:#fff;padding:32px;font-family:Arial,sans-serif"><div style="max-width:560px;margin:auto;border:1px solid #d8a928;border-radius:14px;padding:28px"><h1 style="margin:0 0 14px;color:#d8a928">GANGSTER BOUGIE</h1><p>Use this code to securely access My Orders:</p><div style="font-size:34px;font-weight:800;letter-spacing:8px;margin:24px 0">${esc(code)}</div><p>This code expires in 10 minutes. If you did not request it, you can ignore this email.</p></div></div>`});
}
export async function sendOrderConfirmation(order){
 const rows=(order.items||[]).map(x=>`<tr><td style="padding:8px 0">${esc(x.name)}${x.selection?' — '+esc(x.selection):''}</td><td style="padding:8px 0;text-align:right">× ${esc(x.quantity)}</td></tr>`).join('');
 const money=n=>Number.isFinite(Number(n))?(Number(n)/100).toLocaleString('en-US',{style:'currency',currency:order.currency||'USD'}):'';
 const subtotal=money(order.amount_subtotal), shipping=money(order.amount_shipping), tax=money(order.amount_tax), total=money(order.amount_total);
 const breakdown=(subtotal||shipping||tax)?`<div style="border-top:1px solid #444;padding-top:12px;margin-top:8px"><p style="margin:5px 0"><strong>Subtotal:</strong> ${esc(subtotal)}</p><p style="margin:5px 0"><strong>Shipping:</strong> ${esc(shipping)}</p><p style="margin:5px 0"><strong>Tax:</strong> ${esc(tax)}</p></div>`:'';
 return send({to:order.customer?.email,subject:`Gangster Bougie order ${order.order_number} confirmed`,html:`<div style="background:#070707;color:#fff;padding:32px;font-family:Arial,sans-serif"><div style="max-width:600px;margin:auto;border:1px solid #d8a928;border-radius:14px;padding:28px"><h1 style="color:#d8a928;margin-top:0">ORDER CONFIRMED</h1><p>Thank you for your order.</p><p><strong>Order:</strong> ${esc(order.order_number)}</p><table style="width:100%;color:#fff;border-collapse:collapse">${rows}</table>${breakdown}<p style="border-top:1px solid #444;padding-top:14px"><strong>Total:</strong> ${esc(total)}</p><p>We’ll send another update when your order ships.</p><p style="color:#d8a928;font-weight:700">Gangster Bougie</p></div></div>`});
}
