const SHOP_ID = '28816619';

const STARTER_PRODUCTS = [
  {
    website_names: ['Crowned Luxury Crew Socks'],
    printify_title_contains: 'Crowned Luxury Crew Socks'
  },
  {
    website_names: ['Black Crowned Luxury Cotton Tee', 'White Crowned Luxury Cotton Tee'],
    printify_title_contains: 'Crowned Luxury Cotton Tee'
  }
];

function normalize(value = '') {
  return String(value).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
}

export default async (req) => {
  if (req.method !== 'GET') {
    return Response.json({ error: 'Method not allowed' }, { status: 405, headers: { Allow: 'GET' } });
  }

  const token = process.env.PRINTIFY_API_TOKEN;
  if (!token) {
    return Response.json({ ok: false, error: 'Printify API token is not configured.' }, { status: 500 });
  }

  try {
    const response = await fetch(`https://api.printify.com/v1/shops/${SHOP_ID}/products.json?limit=50&page=1`, {
      headers: {
        Authorization: 'Bearer ' + token,
        'User-Agent': 'Gangster-Bougie-Netlify'
      }
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      return Response.json({ ok: false, error: 'Printify product lookup failed.', status: response.status }, { status: 502 });
    }

    const products = Array.isArray(payload?.data) ? payload.data : (Array.isArray(payload) ? payload : []);

    const mappings = STARTER_PRODUCTS.map((target) => {
      const needle = normalize(target.printify_title_contains);
      const product = products.find((p) => normalize(p.title).includes(needle));
      if (!product) {
        return { website_names: target.website_names, matched: false };
      }

      const enabled = (product.variants || []).filter((v) => v.is_enabled === true);
      return {
        website_names: target.website_names,
        matched: true,
        printify_product: {
          id: product.id,
          title: product.title,
          blueprint_id: product.blueprint_id,
          print_provider_id: product.print_provider_id
        },
        enabled_variant_count: enabled.length,
        enabled_variants: enabled.map((v) => ({
          id: v.id,
          title: v.title,
          sku: v.sku,
          price: v.price,
          cost: v.cost,
          is_available: v.is_available
        }))
      };
    });

    return Response.json({
      ok: true,
      mode: 'read_only_mapping_check',
      shop_id: SHOP_ID,
      mappings
    });
  } catch (error) {
    console.error('Printify starter mapping error', error);
    return Response.json({ ok: false, error: 'Unable to build the starter mapping right now.' }, { status: 502 });
  }
};
