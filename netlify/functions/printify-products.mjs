const SHOP_ID = '28816619';

export default async (req) => {
  if (req.method !== 'GET') {
    return Response.json({ error: 'Method not allowed' }, { status: 405, headers: { Allow: 'GET' } });
  }

  const token = process.env.PRINTIFY_API_TOKEN;
  if (!token) {
    return Response.json({ ok: false, error: 'Printify API token is not configured.' }, { status: 500 });
  }

  try {
    const response = await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json`, {
      headers: {
        Authorization: 'Bearer ' + token,
        'User-Agent': 'Gangster-Bougie-Netlify'
      }
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      console.error('Printify product lookup failed', response.status);
      return Response.json({ ok: false, error: 'Printify product lookup failed.', status: response.status }, { status: 502 });
    }

    const source = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
    const target = new URL(req.url).searchParams.get('id');
    const products = source.filter(product=>!target||product.id===target).map((product) => ({
      id: product.id,
      title: product.title,
      blueprint_id: product.blueprint_id,
      print_provider_id: product.print_provider_id,
      visible: product.visible,
      variants: Array.isArray(product.variants)
        ? product.variants.map((variant) => ({
            id: variant.id,
            title: variant.title,
            sku: variant.sku,
            price: variant.price,
            cost: variant.cost,
            is_enabled: variant.is_enabled,
            is_available: variant.is_available
          }))
        : []
    }));

    return Response.json({
      ok: true,
      shop_id: SHOP_ID,
      count: products.length,
      products
    });
  } catch (error) {
    console.error('Printify product lookup error', error);
    return Response.json({ ok: false, error: 'Unable to retrieve Printify products right now.' }, { status: 502 });
  }
};
