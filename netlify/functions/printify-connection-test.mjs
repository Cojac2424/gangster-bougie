export default async (req) => {
  if (req.method !== 'GET') {
    return Response.json(
      { error: 'Method not allowed' },
      { status: 405, headers: { Allow: 'GET' } }
    );
  }

  const token = process.env.PRINTIFY_API_TOKEN;
  if (!token) {
    return Response.json(
      { ok: false, error: 'Printify API token is not configured.' },
      { status: 500 }
    );
  }

  try {
    const response = await fetch('https://api.printify.com/v1/shops.json', {
      headers: {
        Authorization: 'Bearer ' + token,
        'User-Agent': 'Gangster-Bougie-Netlify'
      }
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      console.error('Printify API connection test failed', response.status);
      return Response.json(
        { ok: false, error: 'Printify connection failed.', status: response.status },
        { status: 502 }
      );
    }

    const shops = Array.isArray(data)
      ? data.map((shop) => ({
          id: shop.id,
          title: shop.title,
          sales_channel: shop.sales_channel
        }))
      : [];

    return Response.json({
      ok: true,
      message: 'Printify connection successful.',
      shops
    });
  } catch (error) {
    console.error('Printify API connection error', error);
    return Response.json(
      { ok: false, error: 'Unable to contact Printify right now.' },
      { status: 502 }
    );
  }
};
