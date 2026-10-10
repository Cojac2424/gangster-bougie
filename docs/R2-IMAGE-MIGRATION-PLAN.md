# R2 image migration preparation — NOT DEPLOYED

Inventory derived from static image references in index.html on branch optimization/bandwidth-lazy-carousel. Not a complete repository storage audit. No live changes.

## Findings
- 145 unique referenced images: 14 PNG and 131 JPEG.
- Seven outfit carousel images must be prioritized for visual loading.
- Netlify Functions remain necessary for checkout, shipping and customer orders.
- Binary file sizes, dimensions and total storage are unverified.

## Migration safety checklist
1. Confirm Cloudflare R2 access, billing and whether an assets subdomain can be attached without disturbing storefront DNS.
2. Obtain original binaries and record hashes, dimensions, content types and total bytes. Preserve quality; do not recompress blindly.
3. Upload originals to Standard R2 bucket, use a custom domain for production and test Cloudflare cache. Never rely on r2.dev for production.
4. Validate image URL availability, CORS needs, SSL, mobile load timing and cold-cache first-carousel paint.
5. On a development branch rewrite static and dynamically generated image URLs, including CSS and product modals, only after R2 URLs work. Keep Netlify checkout/shipping functions unchanged.
6. Test all seven slides, product variants, lookbook, modal thumbnails, checkout and email.
7. Get explicit approval before one bundled production deployment; retain rollback paths.
8. Compare Netlify bandwidth and R2 operations/storage; R2 egress is free, but excess storage and operations can cost money.

## Referenced image paths
- 0487E238-7F25-47CC-9B2F-913F718A3915.png
- 09D6C9A9-6759-4A5E-8C29-87A00A34A157.png
- 15CD0524-CA40-4621-81A1-3ABDDF6C4FDD.png
- 1C478554-85CA-4F81-8358-47C4F86C0C0F.png
- 55CF2A2E-AA03-4D2F-9D7B-2E523AEC0041.png
- 9BC2D535-588B-4711-8EFE-5D529A685A22.png
- 9DA992EE-4CDE-46D9-A21E-D8EC820F7FBC.png
- BAC0AEC8-24B2-4FD3-AECF-5E789E61CB2A.png
- BE21A058-6B01-4269-8167-A376094E2D70.png
- C30C5493-EC0F-4DC6-B74D-FC2CC515FEB4.png
- C48AD54C-E4ED-42AE-A74B-7A354C337BDA.png
- CAC264CF-EC46-4E8E-AD42-5A4FD048418B.png
- ECA29DBD-304E-493E-8A51-76E7CB5E4BC8.png
- IMG_0092.jpeg
- IMG_0093.jpeg
- IMG_0094.jpeg
- IMG_0095.jpeg
- IMG_0096.jpeg
- IMG_0097.jpeg
- IMG_0098.jpeg
- IMG_0099.jpeg
- IMG_0198.jpeg
- IMG_0199.jpeg
- IMG_0200.jpeg
- IMG_0201.jpeg
- IMG_0203.jpeg
- IMG_0204.jpeg
- IMG_0254.jpeg
- IMG_0255.jpeg
- IMG_0258.jpeg
- IMG_0260.jpeg
- IMG_0262.jpeg
- IMG_0264.jpeg
- IMG_0266.jpeg
- IMG_0268.jpeg
- IMG_0273.jpeg
- IMG_0274.jpeg
- IMG_0275.jpeg
- IMG_0276.jpeg
- IMG_0277.jpeg
- IMG_0278.jpeg
- IMG_0279.jpeg
- IMG_0280.jpeg
- IMG_0281.jpeg
- IMG_0282.jpeg
- IMG_0283.jpeg
- IMG_0284.jpeg
- IMG_0285.jpeg
- IMG_0286.jpeg
- IMG_0287.jpeg
- IMG_0288.jpeg
- IMG_0289.jpeg
- IMG_0290.jpeg
- IMG_0291.jpeg
- IMG_0292.jpeg
- IMG_0293.jpeg
- IMG_0294.jpeg
- IMG_0295.jpeg
- IMG_0296.jpeg
- IMG_0300.jpeg
- IMG_0301.jpeg
- IMG_0302.jpeg
- IMG_0303.jpeg
- IMG_0304.jpeg
- IMG_0305.jpeg
- IMG_0306.jpeg
- IMG_0307.jpeg
- IMG_0308.jpeg
- IMG_0309.jpeg
- IMG_0310.jpeg
- IMG_0311.jpeg
- IMG_0312.jpeg
- IMG_0313.jpeg
- IMG_0314.jpeg
- IMG_0315.jpeg
- IMG_0319.jpeg
- IMG_0320.jpeg
- IMG_0321.jpeg
- IMG_0322.jpeg
- IMG_0323.jpeg
- IMG_0324.jpeg
- IMG_0325.jpeg
- IMG_0326.jpeg
- IMG_0328.jpeg
- IMG_0329.jpeg
- IMG_0330.jpeg
- IMG_0334.jpeg
- IMG_0335.jpeg
- IMG_0336.jpeg
- IMG_0337.jpeg
- IMG_0338.jpeg
- IMG_0339.png
- IMG_0340.jpeg
- IMG_0341.jpeg
- IMG_0342.jpeg
- IMG_0343.jpeg
- IMG_0344.jpeg
- IMG_0345.jpeg
- IMG_0346.jpeg
- IMG_0349.jpeg
- IMG_0351.jpeg
- IMG_0352.jpeg
- IMG_0353.jpeg
- IMG_0354.jpeg
- IMG_0355.jpeg
- IMG_0356.jpeg
- IMG_0357.jpeg
- IMG_0358.jpeg
- IMG_0360.jpeg
- IMG_0361.jpeg
- IMG_0362.jpeg
- IMG_0363.jpeg
- IMG_0364.jpeg
- IMG_0365.jpeg
- IMG_0366.jpeg
- IMG_0367.jpeg
- IMG_0370.jpeg
- IMG_0375.jpeg
- IMG_0382.jpeg
- IMG_0385.jpeg
- IMG_0412.jpeg
- IMG_0413.jpeg
- IMG_0414.jpeg
- IMG_0415.jpeg
- IMG_0416.jpeg
- IMG_0417.jpeg
- IMG_0547.jpeg
- IMG_0548.jpeg
- IMG_0553.jpeg
- IMG_0554.jpeg
- IMG_1848.jpeg
- IMG_1852.jpeg
- IMG_1905.jpeg
- IMG_1913.jpeg
- IMG_1914.jpeg
- IMG_1915.jpeg
- IMG_1916.jpeg
- IMG_1917.jpeg
- IMG_1918.jpeg
- IMG_1919.jpeg
- IMG_2021.jpeg
- IMG_2028.jpeg
- IMG_2029.jpeg
- IMG_2030.jpeg
- IMG_2108.jpeg
