# Gangster Bougie Affiliate Program — deployment checklist

Status: feature branch only. Do not merge until all blockers below are complete.

## Locked business rules
- Program name: Gangster Bougie Affiliate Program.
- Customer receives 5% off merchandise through one valid affiliate attribution.
- Affiliate attribution can come from ?ref=CODE or a manually entered Affiliate Code.
- Manual code replaces stored link attribution; same code never stacks.
- Affiliate earns a private fixed-dollar payout per product. Costs and margins are never exposed.
- Commission begins as pending and is eligible for payout after 30 days.

## Implemented on this branch
- Netlify Blobs affiliate records and private payout schedules.
- Public active-code validation with safe fields only.
- Referral link capture and local persistence.
- Cart Affiliate Code field and professional affiliate messaging.
- Referral click counter without storing raw IP addresses.
- Server-side affiliate validation before Stripe Checkout.
- Affiliate ID/code attached to Stripe session metadata.
- Referral record keyed to Stripe Checkout Session.
- Verified-payment commission creation, idempotent per Stripe session.
- Commission void helper for refund integration.
- Checkout fails closed if affiliate coupon environment variable is missing.

## Production blockers
1. Connect the Gangster Bougie Stripe account to the Stripe connector.
2. Create a live 5% once-per-order merchandise coupon in that account.
3. Set Netlify STRIPE_AFFILIATE_COUPON_ID to that coupon ID in the appropriate deploy contexts.
4. Wire Stripe refund events to void/reverse affiliate commissions and test full/partial refunds.
5. Build secure owner admin authentication + affiliate management/ledger UI.
6. Build secure affiliate login/dashboard (clicks, orders, pending, payable, paid).
7. Test referral link, manual override, duplicate webhook, expired/inactive code, checkout, refund and mobile layouts in a non-production deploy.
8. Only then merge to main and deploy live.

No live Stripe, Printify or production-site settings were changed by this branch.
