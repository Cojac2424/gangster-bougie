# Gangster Bougie affiliate program — operator guide (staging only)

**Status:** Implemented in PR #22 / `crop-tee-replacement-staging-20261013`. Do not merge until the full storefront cleanup, crop tees, affiliate setup, and order testing are approved.

## Architecture

- `/affiliate.html`: public application, emailed one-time-code login, affiliate dashboard and link sharing.
- `/affiliate-admin.html`: private owner approval, rate setting, refund/review, payout reconciliation.
- `netlify/functions/affiliate.mjs` and `affiliate-admin.mjs`: protected API endpoints.
- `netlify/functions/lib/gb-affiliates.mjs`: persistent Netlify Blobs application records and commission ledger.
- `netlify/functions/lib/gb-product-catalog.mjs`: exact currently checkout-supported names/prices. The owner commission UI automatically suggests every product from this catalogue.
- `create-checkout-session.mjs`: validates affiliate code on the server and stores approved affiliate ID/code on the Stripe Checkout Session metadata, **without applying a customer discount**.
- `stripe-webhook.mjs`: creates a commission ledger entry **only from a verified paid Stripe session**, with a unique key per Checkout Session to avoid duplicate affiliate orders. It also flags refunds for manual review. Stripe is *not* used to pay affiliates.
- `tests/affiliate.test.mjs`: rule and script checks; GitHub Actions runs automatically in staging.

## Owner actions required before launch

1. **Create a long, random admin secret** in a password manager (at least 24 characters). In Netlify site configuration > Environment variables, set `GB_AFFILIATE_ADMIN_SECRET` to that value in the appropriate contexts. **Never put the value in source code, support tickets, screenshots, or chat.** The admin page refuses to open without it.
2. Confirm **Resend** environment settings `RESEND_API_KEY` and `GB_EMAIL_FROM` are valid for sending to external affiliates. The Resend testing address cannot reliably deliver to arbitrary affiliate emails.
3. In Stripe, confirm the existing Gangster Bougie webhook forwards `checkout.session.completed`, `checkout.session.async_payment_succeeded`, and `charge.refunded` to the existing signed `stripe-webhook` endpoint. Do not confuse it with the BELLCON Stripe account.
4. Before applications go public, use **Product commission amounts** in private affiliate admin to enter fixed USD rates based on roughly 20% of actual per-unit profit **after reviewing the Printify costs and relevant fulfillment costs**. Rates are stored server-side; affiliates see only the rate. An item without a rate is flagged `needs_rates` and is not automatically payable.
5. Verify real end-to-end behavior **on staging** without risking a live customer's payment: application > owner notification > approval > affiliate approval email > sign-in code > affiliate link or typed code > checkout metadata > paid-order webhook > ledger > refund review > 30-day hold > manual payout reference. If using Stripe test keys, verify the deploy context and webhook secret are the test-mode ones before simulating paid orders.
6. Complete the storefront cleanup; remove temporary `variant-verification.html` and `gb-variant-lookup.mjs` before production merge. Require explicit owner approval for merge/deploy.

## Everyday use

- Affiliate applies. Owner approves in `/affiliate-admin.html`; generated referral code and link become available in affiliate dashboard.
- Customer either follows `https://gangsterbougie.com/?ref=CODE` or types `CODE` in cart. The browser remembers the most recent referral for 30 days, and the server checks active code at checkout.
- A paid order creates one ledger record with item quantities, fixed commission rates, and a 30-day payout hold. A missing rate, self-referral, inactive affiliate, or refund requires manual review.
- Owner manually pays after the hold, then marks it paid and enters the **actual payout confirmation/reference**. Never mark an unpaid transfer as paid.
- New products: create the Printify product; upload all imagery to Cloudflare R2; add/storefront-verify the exact name in the shared checkout catalogue and Printify fulfillment mapping; set a fixed USD commission in the owner dashboard; then reference the item in cards/Build Your Fit/carousel. Existing gold-card navigation remains unchanged.

## Important limitations

- The system does **not** pay affiliates automatically, calculate profit from Printify automatically, or stop a refund after commission has already been paid. Refunds after payout are flagged for manual recovery.
- Setting a commission rate later does not silently pay older `needs_rates` orders: the owner must click **Recalculate** on those records.
- Budget/hosting is not related to commission payouts. Codes are for referral attribution, **not customer discounts**.
- Automated tests check logic and syntax, but a real account/email/paid-session integration test is still required before the first live affiliate promotion.
