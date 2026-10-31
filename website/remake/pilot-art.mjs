// M2 concept presentation. Original source product pixels are preserved in lossless exports.
const escape = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('"', '&quot;');

export function pilotHero(lang, c) {
  const description = lang === 'ar'
    ? 'عبوة غير معنونة وبطاقة مطوية، بإضاءة جانبية على سطح محايد.'
    : 'Unlabelled bottle and folded card in directional light.';
  return `<figure class="art hero-art"><picture><source media="(max-width:760px)" srcset="/assets/hero-mobile-640.webp 640w, /assets/hero-mobile-960.webp 960w" sizes="100vw"><img src="/assets/hero-desktop-1280.webp" srcset="/assets/hero-desktop-640.webp 640w, /assets/hero-desktop-960.webp 960w, /assets/hero-desktop-1280.webp 1280w" sizes="(max-width:760px) 100vw, 50vw" width="1536" height="1024" alt="${escape(description)}" fetchpriority="high" decoding="async"></picture><figcaption>${escape(c.concept)}</figcaption></figure>`;
}

export function pilotProduct(lang, c, familyMarkup) {
  return `<figure class="art product-art"><button type="button" class="product-visual" disabled><img id="product-image" src="/assets/shampoo-source.webp" width="1263" height="1246" alt="${escape(c.concept ? c.productNames[0] + '. ' + c.concept : c.productNames[0])}" decoding="async"></button>${c.concept ? `<figcaption>${escape(c.concept)}</figcaption>` : ''}</figure>`;
}
