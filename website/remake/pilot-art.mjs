// M2 concept presentation. Original source product pixels are preserved in lossless exports.
const escape = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('"', '&quot;');

export function pilotHero(lang, c) {
  const description = lang === 'ar'
    ? 'تصوّر لعبوة غير معنونة وبطاقة مطوية، بإضاءة جانبية على سطح محايد. ' + c.concept
    : 'Concept study of an unlabelled bottle and folded card in directional light. ' + c.concept;
  return `<figure class="art hero-art"><picture><source media="(max-width:760px)" srcset="/assets/hero-mobile-640.webp 640w, /assets/hero-mobile-960.webp 960w" sizes="100vw"><img src="/assets/hero-desktop-1280.webp" srcset="/assets/hero-desktop-640.webp 640w, /assets/hero-desktop-960.webp 960w, /assets/hero-desktop-1280.webp 1280w" sizes="(max-width:760px) 100vw, 50vw" width="1536" height="1024" alt="${escape(description)}" fetchpriority="high" decoding="async"></picture><figcaption>${escape(c.concept)}</figcaption></figure>`;
}

export function pilotProduct(lang, c, familyMarkup) {
  return `<figure class="art product-art"><div class="product-visual"><img id="product-image" src="/assets/shampoo-source.webp" width="1263" height="1246" alt="${escape(c.productNames[0] + '. ' + c.concept)}" decoding="async"></div><figcaption>${escape(c.concept)}</figcaption></figure>`;
}
