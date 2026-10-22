# Gangster Bougie affiliate program — operator guide (staging only)

**Status:** Implementation assembled on staging PR #22 / `crop-tee-replacement-staging-20261013`. Owner confirmed all 15 eligible commission groups saved in the deploy preview on 2026-10-21. Replacement crop tee IDs, XS–XL fulfillment variants and storefront images are configured. Final live-service integration checks and explicit owner approval are still required before production merge. No production deployment is authorized.

## Architecture

- `/affiliate.html`: public application, emailed one-time-code login, affiliate dashboard and link sharing.
- `/affiliate-admin.html`: private owner approval, rate setting, refund/review, payout reconciliation.
- `netlify/functions/affiliate.mjs` and `affiliate-admin.mjs`: protected API endpoints.
- `netlify/functions/lib/gb-affiliates.mjs`: persistent Netlify Blobs application records and commission ledger.
- `netlify/functions/lib/gb-product-catalog.mjs`: authoritative checkout prices, 51 individually cost-checked physical products, and 20 commission rate groups. Thirteen women's sports bras share one rate, thirteen leggings share one, and eight workout shorts (including black/white) share one. Other product types retain separate rates.
- `create-checkout-session.mjs`: validates affiliate code on the server and stores approved affiliate ID/code on the Stripe Checkout Session metadata, **without applying a customer discount**.
- `stripe-webhook.mjs`: creates a commission ledger entry **only from a verified paid Stripe session**, with a unique key per Checkout Session to avoid duplicate affiliate orders. It also flags refunds for manual review. Stripe is *not* used to pay affiliates.
- `tests/affiliate.test.mjs`: rule and script checks; GitHub Actions runs automatically in staging.

## Temporary non-commissionable products (owner-approved policy)

As agreed on October 21, **four product categories (five commission keys)** are temporarily excluded because Canadian production and shipping costs leave inadequate margins:

- Men's basketball rib shorts: both Onyx/Gold and Cream/Gold designs.
- Crowned Luxury crew socks.
- Stainless steel gym bottles: 12 oz and 18 oz.
- Mini wrap bandanas.

They **remain for sale** and can appear on referred orders. The server sets their commission to $0, regardless of any outdated saved rate. The ledger marks each excluded line with `excluded: true`. An excluded-only paid order is recorded as `excluded_only`, with a $0 total and no payment action. Mixed orders receive the sum of eligible item commissions only. The rate editor refuses new nonzero rates on excluded products.

The affiliate application and dashboard clearly identify the exclusion list and explain it without revealing confidential production costs or margins. Suggested reply to an affiliate: "Certain products are temporarily excluded because of their production and delivery costs. The list is reviewed periodically, and eligible items in the same order still earn their listed commissions."

Printify sync can still review all 51 physical products. **Only eligible products** need verified positive rate recommendations for bulk approval. The 20 group keys comprise 15 eligible rates and 5 excluded keys. Exclusion stays in force until the owner explicitly approves changing the policy; a cost sync alone never activates an excluded product.

## Automated Printify cost review — no spreadsheet required

The owner-only `affiliate-admin.html` page now has **Sync all Printify costs** and **Approve all reviewed proposals** controls. They do not operate until `GB_AFFILIATE_ADMIN_SECRET` is configured. The Printify sync also needs the site's pre-existing `PRINTIFY_API_TOKEN`, used by Gangster Bougie shipping and order fulfillment. Do not paste either token into chat or embed one in website JavaScript.

**How the workflow works:**

1. Unlock the private admin page with the admin secret. Click **Sync all Printify costs** once; it processes up to three physical products per request, and automatically continues until all 51 have been checked. Even shared-rate garments are verified individually for safe sizing and shipping allowances.
2. The server fetches the configured Printify product(s) and variant `cost` for every size or colour. It fetches the print provider's standard first-item shipping profiles for both the US and Canada. The Printify API calls are server-only.
3. The planning formula intentionally uses **the LOWEST retail price across offered options, the HIGHEST Printify production cost, and the HIGHEST first-item shipping cost among US and Canada**, minus the customer contribution from the same rules used by checkout. It reserves an **estimated 4.5% plus USD $0.30 per product** for processing. These are conservative *planning assumptions*, not verified Stripe fees, and omit extra operating costs or returns.
4. Compute about 20% of the estimated profit. Default is to round **DOWN** to a whole dollar, except a target between $0.75 and $0.99 can be proposed as **$1** if at least $4 estimated profit remains *before* the payout (the agreed slim-margin leggings case). The admin also shows what the owner keeps after the proposed commission. Each proposal remains private in Netlify Blobs (`gb-owner-printify-affiliate-cost-v1`), never exposed to affiliates.
5. Review the full product report. Missing/unavailable variants, missing Canadian or US shipping profiles, or non-positive suggested commissions receive a **needs review** flag. **Bulk approval requires every eligible product to have a fresh, positive, owner-reviewed proposal; explicitly excluded items are not blockers or payout candidates.**
6. Only after reviewing the proposals, click **Approve all reviewed proposals** and confirm. The private API saves 15 eligible fixed commission rates in small batches; five explicitly excluded keys remain at $0. For shared women's bras, leggings, and workout shorts, each family's rate is the **lowest safe proposed amount across every one of its designs**. The verified Stripe webhook automatically totals (fixed group/product rate × purchased quantity) across every item on a referred order; actual line-item names remain visible.
7. In future, new products require verified checkout/fulfillment mappings, cost sync and approval before affiliates can earn commissions on them.

**Do not confuse the estimated per-item fixed commission with actual accounting profit**: order-specific Printify shipping, currency conversion, card processing, taxes, discounts and returns can differ. If margins are unusually narrow, revise the selling price or commission rather than approve an unsafe payout.

No live production deployment, Stripe customer payment or real affiliate payout occurs during cost setup. The old Excel/CSV worksheet is optional bookkeeping and is not required to operate the admin.

## Owner actions required before launch

1. **Create a long, random admin secret** in a password manager (at least 24 characters). In Netlify site configuration > Environment variables, set `GB_AFFILIATE_ADMIN_SECRET` to that value in the appropriate contexts. **Never put the value in source code, support tickets, screenshots, or chat.** The admin page refuses to open without it.
2. Confirm **Resend** environment settings `RESEND_API_KEY` and `GB_EMAIL_FROM` are valid for sending to external affiliates. The Resend testing address cannot reliably deliver to arbitrary affiliate emails.
3. In Stripe, confirm the existing Gangster Bougie webhook forwards `checkout.session.completed`, `checkout.session.async_payment_succeeded`, and `charge.refunded` to the existing signed `stripe-webhook` endpoint. Do not confuse it with the BELLCON Stripe account.
4. Before applications go public, **sync and review all Printify cost proposals** in private affiliate admin. When all eligible individual product checks are ready, approve the resulting 15 payable grouped commissions once in the admin. Excluded products stay at $0. If any needs review, resolve it and rerun; do not invent missing costs. Rates are stored server-side; affiliates see only the approved rate. An item without a rate is flagged `needs_rates` and is not automatically payable.
5. Verify real end-to-end behavior **on staging** without risking a live customer's payment: application > owner notification > approval > affiliate approval email > sign-in code > affiliate link or typed code > checkout metadata > paid-order webhook > ledger > refund review > 30-day hold > manual payout reference. If using Stripe test keys, verify the deploy context and webhook secret are the test-mode ones before simulating paid orders.
6. Storefront cleanup: retired yoga mats are removed from the staging catalog, cart, checkout, fulfillment and affiliate surfaces; crop tee black/white size maps and images are wired. Temporary `variant-verification.html` and `gb-variant-lookup.mjs` are absent from the staging tree. Require explicit owner approval for merge/deploy.

**Preview-to-production note:** The 15 owner-approved rate groups were confirmed in the deploy-preview admin. Before launching, verify that the production admin sees the identical values after merge; preview-stored records must not be assumed to migrate across Netlify deploy contexts. Do not overwrite or invent payouts if those records are missing.\n\n**Stripe preview:** A Stripe `cs_test_` session could not be loaded by the preview browser. Check that `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` in the preview refer to the same Stripe account and mode before the final integration test. Do not change working production keys. Checkout rejects mixed live/test key prefixes in the staged guard.\n\n## Everyday use

- Affiliate applies. Owner approves in `/affiliate-admin.html`; generated referral code and link become available in affiliate dashboard.
- Customer either follows `https://gangsterbougie.com/?ref=CODE` or types `CODE` in cart. The browser remembers the most recent referral for 30 days, and the server checks active code at checkout.
- A paid order creates one ledger record with item quantities, fixed commission rates, and a 30-day payout hold. Excluded items earn $0; excluded-only orders are recorded but not payable. Missing eligible rates, self-referrals, inactive affiliates, and refunds require manual review.
- Owner manually pays after the hold, then marks it paid and enters the **actual payout confirmation/reference**. Never mark an unpaid transfer as paid.
- New products: create the Printify product; upload imagery to Cloudflare R2; add/storefront-verify the exact name in the shared checkout catalogue and Printify fulfillment mapping; review its cost and shipping with the owner dashboard and update its fixed USD garment-family rate or individual product rate as appropriate; then reference the item in cards/Build Your Fit/carousel. Existing gold-card navigation remains unchanged.

## Important limitations

- The system does **not** pay affiliates automatically or calculate actual transaction-level accounting profit for payouts. It can now **estimate conservative per-product commissions** from Printify cost/shipping data in the protected owner dashboard; the owner must explicitly review and activate those fixed rates. The system cannot reverse a refund after commission has already been paid. Refunds after payout are flagged for manual recovery.
- Setting a commission rate later does not silently pay older `needs_rates` orders: the owner must click **Recalculate** on those records.
- Budget/hosting is not related to commission payouts. Codes are for referral attribution, **not customer discounts**.
- Automated tests check logic and syntax, but a real account/email/paid-session integration test is still required before the first live affiliate promotion.
