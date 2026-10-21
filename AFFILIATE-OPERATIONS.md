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

## Automated Printify cost review — no spreadsheet required

The owner-only `affiliate-admin.html` page now has **Sync all Printify costs** and **Approve all reviewed proposals** controls. They do not operate until `GB_AFFILIATE_ADMIN_SECRET` is configured. The Printify sync also needs the site's pre-existing `PRINTIFY_API_TOKEN`, used by Gangster Bougie shipping and order fulfillment. Do not paste either token into chat or embed one in website JavaScript.

**How the workflow works:**

1. Unlock the private admin page with the admin secret. Click **Sync all Printify costs** once; it processes up to three products per request, and automatically continues until all 52 have been checked.
2. The server fetches the configured Printify product(s) and variant `cost` for every size or colour. It fetches the print provider's standard first-item shipping profiles for both the US and Canada. The Printify API calls are server-only.
3. The planning formula intentionally uses **the LOWEST retail price across offered options, the HIGHEST Printify production cost, and the HIGHEST first-item shipping cost among US and Canada**, minus the customer contribution from the same rules used by checkout. It reserves an **estimated 4.5% plus USD $0.30 per product** for processing. These are conservative *planning assumptions*, not verified Stripe fees, and omit extra operating costs or returns.
4. Compute about 20% of the estimated profit. Default is to round **DOWN** to a whole dollar, except a target between $0.75 and $0.99 can be proposed as **$1** if at least $4 estimated profit remains *before* the payout (the agreed slim-margin leggings case). The admin also shows what the owner keeps after the proposed commission. Each proposal remains private in Netlify Blobs (`gb-owner-printify-affiliate-cost-v1`), never exposed to affiliates.
5. Review the full product report. Missing/unavailable variants, missing Canadian or US shipping profiles, or non-positive suggested commissions receive a **needs review** flag. **Bulk approval is blocked unless every currently listed product has a fresh, positive and owner-reviewed proposal.**
6. Only after reviewing the proposals, click **Approve all reviewed proposals** and confirm. The private API saves the proposed fixed per-product amounts in small batches. After that, the existing verified Stripe webhook automatically totals (fixed product rate × purchased quantity) across every item on a referred order.
7. In future, new products require verified checkout/fulfillment mappings, cost sync and approval before affiliates can earn commissions on them.

**Do not confuse the estimated per-item fixed commission with actual accounting profit**: order-specific Printify shipping, currency conversion, card processing, taxes, discounts and returns can differ. If margins are unusually narrow, revise the selling price or commission rather than approve an unsafe payout.

No live production deployment, Stripe customer payment or real affiliate payout occurs during cost setup. The old Excel/CSV worksheet is optional bookkeeping and is not required to operate the admin.

## Owner actions required before launch

1. **Create a long, random admin secret** in a password manager (at least 24 characters). In Netlify site configuration > Environment variables, set `GB_AFFILIATE_ADMIN_SECRET` to that value in the appropriate contexts. **Never put the value in source code, support tickets, screenshots, or chat.** The admin page refuses to open without it.
2. Confirm **Resend** environment settings `RESEND_API_KEY` and `GB_EMAIL_FROM` are valid for sending to external affiliates. The Resend testing address cannot reliably deliver to arbitrary affiliate emails.
3. In Stripe, confirm the existing Gangster Bougie webhook forwards `checkout.session.completed`, `checkout.session.async_payment_succeeded`, and `charge.refunded` to the existing signed `stripe-webhook` endpoint. Do not confuse it with the BELLCON Stripe account.
4. Before applications go public, **sync and review all Printify cost proposals** in private affiliate admin. When all 52 are ready, approve them once in the admin. If any needs review, resolve it and rerun; do not invent missing costs. Rates are stored server-side; affiliates see only the approved rate. An item without a rate is flagged `needs_rates` and is not automatically payable.
5. Verify real end-to-end behavior **on staging** without risking a live customer's payment: application > owner notification > approval > affiliate approval email > sign-in code > affiliate link or typed code > checkout metadata > paid-order webhook > ledger > refund review > 30-day hold > manual payout reference. If using Stripe test keys, verify the deploy context and webhook secret are the test-mode ones before simulating paid orders.
6. Complete the storefront cleanup; remove temporary `variant-verification.html` and `gb-variant-lookup.mjs` before production merge. Require explicit owner approval for merge/deploy.

## Everyday use

- Affiliate applies. Owner approves in `/affiliate-admin.html`; generated referral code and link become available in affiliate dashboard.
- Customer either follows `https://gangsterbougie.com/?ref=CODE` or types `CODE` in cart. The browser remembers the most recent referral for 30 days, and the server checks active code at checkout.
- A paid order creates one ledger record with item quantities, fixed commission rates, and a 30-day payout hold. A missing rate, self-referral, inactive affiliate, or refund requires manual review.
- Owner manually pays after the hold, then marks it paid and enters the **actual payout confirmation/reference**. Never mark an unpaid transfer as paid.
- New products: create the Printify product; upload all imagery to Cloudflare R2; add/storefront-verify the exact name in the shared checkout catalogue and Printify fulfillment mapping; set a fixed USD commission in the owner dashboard; then reference the item in cards/Build Your Fit/carousel. Existing gold-card navigation remains unchanged.

## Important limitations

- The system does **not** pay affiliates automatically or calculate actual transaction-level accounting profit for payouts. It can now **estimate conservative per-product commissions** from Printify cost/shipping data in the protected owner dashboard; the owner must explicitly review and activate those fixed rates. The system cannot reverse a refund after commission has already been paid. Refunds after payout are flagged for manual recovery.
- Setting a commission rate later does not silently pay older `needs_rates` orders: the owner must click **Recalculate** on those records.
- Budget/hosting is not related to commission payouts. Codes are for referral attribution, **not customer discounts**.
- Automated tests check logic and syntax, but a real account/email/paid-session integration test is still required before the first live affiliate promotion.
