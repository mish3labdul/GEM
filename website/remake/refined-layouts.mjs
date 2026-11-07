// Approved R1/R2 Reference-Led Luxury Hospitality Layout Compositions.
// Engineering shell and local tools stay in build.mjs and app.js.
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const br = (s) => esc(s).replace(/\n/g, '<br>')
const wrapEn = (s) => esc(s).replace(/(Property Edition|Bespoke Programme|GEM)/g, '<bdi lang="en">$1</bdi>')

const alt = {
  en: {
    hero: 'GEM amber glass shampoo pump bottle on a travertine ledge in soft morning light, with a branded GEM card beside it',
    family: 'Five GEM amber glass pump bottles with bilingual Arabic and English labels on a travertine ledge',
    vanity: 'Two GEM amber bottles, a rolled towel and a branded GEM card on a stone vanity',
    turndown: 'A GEM amber Body Wash and a cream Body Lotion, both with pumps, on a wooden tray beside a branded GEM card and a linen napkin',
    lobby: 'GEM cream Hand Wash pump bottle on a stone plinth in front of a carved wall with lattice shadows',
    flatlay: 'GEM amber body wash pump bottle lying on linen beside an olive sprig and a branded GEM card',
    packaging: 'Branded GEM cream presentation boxes, a kraft carton and a GEM tag on travertine',
    carton: 'GEM amber shampoo pump bottle in front of a branded cream GEM carton on a stone shelf',
  },
  ar: {
    hero: 'عبوة شامبو زجاجية كهرمانية من GEM بمضخة على حافة من الترافرتين في ضوء الصباح، وبجانبها بطاقة GEM المطبوعة',
    family: 'خمس عبوات زجاجية كهرمانية من GEM بمضخات وملصقات ثنائية اللغة على حافة من الترافرتين',
    vanity: 'عبوتان كهرمانيتان من GEM ومنشفة ملفوفة وبطاقة GEM على سطح حجري',
    turndown: 'عبوة غسول الجسم الكهرمانية وعبوة لوشن الجسم الكريمية من GEM، كلتاهما بمضخة، على صينية خشبية بجانب بطاقة GEM ومنديل كتاني',
    lobby: 'عبوة غسول اليدين الكريمية من GEM بمضخة على قاعدة حجرية أمام جدار منحوت وظلال شبكية',
    flatlay: 'عبوة غسول جسم كهرمانية من GEM بمضخة على قماش كتاني بجانب غصن زيتون وبطاقة GEM',
    packaging: 'علب تقديم كريمية من GEM وعلبة كرافت وبطاقة GEM على سطح من الترافرتين',
    carton: 'عبوة شامبو كهرمانية من GEM بمضخة أمام علبة GEM كريمية على رف حجري',
  },
}

const arrow = '<span aria-hidden="true">→</span>'
const beigeOpen = (up, id = '') => `<section${id} class="tone-beige arc-section"><div class="arc-banner"><img src="${up}assets/tx-arches.webp" alt="" width="2172" height="724" loading="lazy"></div>`
const picture = (src, a, { lazy = true, cls = '' } = {}) =>
  `<img src="${src}" alt="${esc(a)}"${lazy ? ' loading="lazy"' : ''} decoding="async">`

const cta = ({ c, lang, up }) => `<section class="cta on-texture veil">
 <div class="bg"><img src="${up}assets/tx-limewash.webp" alt="" loading="lazy"></div>
 <div class="wrap"><h2>${br(c.next)}</h2><p>${esc(c.nextBody)}</p>
 <div class="actions"><a class="button" href="${up}${lang}/contact/">${esc(c.discuss)} ${arrow}</a></div></div>
</section>`

const concept = (c) => c.concept ? `<figcaption>${esc(c.concept)}</figcaption>` : ''

const quarterArc = '<svg class="gem-quarter-arc" viewBox="0 0 96 96" width="64" height="64" aria-hidden="true" focusable="false"><path class="arc-track" d="M8 88 A80 80 0 0 1 88 8" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.22"/><path class="arc-draw" d="M8 88 A80 80 0 0 1 88 8" fill="none" stroke="currentColor" stroke-width="1.75"/></svg>'

const eyebrowArc = '<svg class="gem-quarter-arc eyebrow-arc-glyph" viewBox="0 0 48 48" width="28" height="28" fill="none" aria-hidden="true" focusable="false"><path class="arc-track" d="M6 42 A36 36 0 0 1 42 6" stroke="currentColor" stroke-width="1" stroke-opacity="0.24"/><path class="arc-draw" d="M6 42 A36 36 0 0 1 42 6" stroke="currentColor" stroke-width="1.4"/><circle cx="42" cy="6" r="2" fill="currentColor"/></svg>'

// Unified Five-Product Collection Stage (R1 Approved / R2.3 & R2.4) ------------
function unifiedCollectionStage(lang, c, up) {
  const rtl = lang === 'ar'
  const oneLineHeading = esc(c.pilotHeading).replace(/\n/g, ' ')
  const subLang = rtl ? 'en' : 'ar'
  const subDir = rtl ? 'ltr' : 'rtl'
  const captionBarLeft = rtl
    ? 'الصيغ المستكشفة: الغرف · التثبيت الجداري · السفر'
    : 'Explored formats: Guest Room · Wall-Mounted · Travel'

  return `<section class="section collection-section" id="pilot-products" aria-labelledby="h1">
 <div class="collection-subheader">
  <div class="collection-subheader-left">
   <span class="collection-kicker" lang="${rtl ? 'ar' : 'en'}">${esc(c.collectionKicker)}</span>
   <h1 id="h1" class="collection-title">${oneLineHeading}</h1>
  </div>
  <p class="pilot-selection collection-status-note" aria-live="polite">
   <span class="sr-only">${rtl ? 'المنتج المحدد:' : 'Selected product:'} <strong id="pilot-selected-name">${esc(c.productNames[0])}</strong> · </span>
   <span>${rtl ? 'التوافر التجاري والمواصفات قيد التحديد' : 'Formulations, capacities & supply specifications pending project brief'}</span>
  </p>
 </div>
 <div class="collection-workspace product-explorer">
  <div class="collection-editorial-col">
   <div>
    <p class="collection-intro-note lead">${esc(c.pilotBody)}</p>
    <div class="product-list essential-index" role="group" aria-label="${rtl ? 'المنتجات الأساسية الخمسة' : 'Five guest amenity essentials'}">
     ${c.productNames.map((p, i) => `<button type="button" class="essential-row-btn" data-product="${i}" aria-pressed="${i === 0}">
      <span class="index essential-num" lang="en" dir="ltr">0${i + 1}</span>
      <span class="essential-name">${esc(p)}</span>
      <span class="essential-bilingual-sub" lang="${subLang}" dir="${subDir}">${esc(c.productSubtitles[i])}</span>
     </button>`).join('\n     ')}
    </div>
    <div class="product-caption essential-active-card" aria-live="polite">
     <div class="essential-active-head">
      <span class="essential-active-num" id="product-active-index" lang="en" dir="ltr">01</span>
      <h3 id="product-name">${esc(c.productNames[0])}</h3>
      <span class="essential-active-sub" id="product-subtitle" lang="${subLang}" dir="${subDir}">${esc(c.productSubtitles[0])}</span>
     </div>
     <p id="product-detail">${esc(c.productDetails[0])}</p>
     <div class="essential-meta-row">
      <p class="disclosure">${esc(c.productStatus)}</p>
      <a class="essential-discuss-link" href="${up}${lang}/contact/">${esc(c.productAction)}</a>
     </div>
    </div>
   </div>
   <div class="editorial-footer-bar">
    <span>${esc(captionBarLeft)}</span>
    <span class="num" id="collection-counter" lang="en" dir="ltr">01 / 05</span>
   </div>
  </div>
  <div class="collection-stage-col product-stage" id="gem-collection-stage">
   <svg class="stage-corner-arc" viewBox="0 0 96 96" fill="none" aria-hidden="true">
    <path d="M8 88 A80 80 0 0 1 88 8" stroke="#12171D" stroke-width="1.5"/>
   </svg>
   <div class="architectural-plinth" aria-hidden="true"></div>
   <div class="bottle-contact-shadow" id="stage-contact-shadow" aria-hidden="true"></div>
   <figure class="art product-art stage-vessel-figure">
    <canvas id="gem-stage-3d-canvas" class="stage-3d-canvas" width="960" height="1200" aria-hidden="true"></canvas>
    <button type="button" class="product-visual stage-vessel-btn" disabled>
     <img id="product-image" src="/assets/shampoo-source.webp" width="960" height="1200" alt="${esc(c.productNames[0])}" fetchpriority="high" decoding="async">
    </button>
   </figure>
   <div class="stage-quiet-annotations">
    <span class="quiet-arc-indicator">
     <svg class="quiet-arc-svg" viewBox="0 0 44 12" fill="none" aria-hidden="true">
      <path d="M2 10 Q22 2 42 10" stroke="#12171D" stroke-width="1.1"/>
      <circle id="stage-arc-dot" cx="22" cy="6" r="2.2" fill="#12171D"/>
     </svg>
     <span>${esc(c.stageMotionCue)}</span>
    </span>
    <span id="stage-bottle-caption">${esc(c.productNames[0])} · <span class="num" lang="en" dir="ltr">01 / 05</span></span>
   </div>
  </div>
 </div>
</section>`
}

// Home ----------------------------------------------------------------------
function home({ c, lang, up, a }) {
  const rtl = lang === 'ar'
  const heroImg = rtl ? 'hero-rtl' : 'hero-ltr'
  const cardImgs = ['carton', 'packaging', 'lobby']
  const cardHrefs = ['amenities-packaging/#pilot-products', 'amenities-packaging/#formats', 'amenities-packaging/#programmes']
  const cardAlts = [a.carton, a.packaging, a.lobby]
  const visualCaption = rtl
    ? 'عائلة مستلزمات الضيوف · زجاج كهرماني وملصق ثنائي اللغة'
    : 'Guest Amenity Family · Amber vessel & bilingual label architecture'

  return `<section class="hero portrait r2-home-hero" aria-labelledby="h1">
 <div class="hero-copy r2-home-copy">
  <div class="r2-hero-top-spacer" aria-hidden="true"></div>
  <div class="r2-hero-main-block">
   <div class="eyebrow-row">
    ${eyebrowArc}
    <span>${esc(c.heroEyebrow)}</span>
   </div>
   <h1 id="h1">${br(c.homeH1)}</h1>
   <p class="intro">${wrapEn(c.homeIntro)}</p>
   <div class="actions">
    <a class="button" href="${up}${lang}/amenities-packaging/">${esc(c.explore)} ${arrow}</a>
    <a class="button ghost" href="${up}${lang}/contact/">${esc(c.discuss)}</a>
   </div>
  </div>
  <div class="hero-addendum">
   <p class="status">${esc(c.status)}</p>
   <span class="num" lang="en" dir="ltr">01 / 04</span>
  </div>
 </div>
 <picture class="r2-home-visual">
  <source media="(max-width:760px)" srcset="${up}assets/hero-mobile.webp">
  <img src="${up}assets/${heroImg}.webp" alt="${esc(a.hero)}" fetchpriority="high" decoding="async">
  <span class="visual-caption-bar" aria-hidden="true">
   <span>${esc(visualCaption)}</span>
   <span class="num" lang="en" dir="ltr">GEM™ — KSA / GCC</span>
  </span>
 </picture>
</section>
<section>
 <div class="wrap split">
  <div class="copy"><h2>${br(c.homeSection)}</h2><p>${wrapEn(c.homeSectionBody)}</p></div>
  <figure>${picture(`${up}assets/turndown.webp`, a.turndown)}${concept(c)}</figure>
 </div>
</section>
<section class="tone-sand">
 <div class="wrap cards">
  ${c.homeLinks.map(([t, d, l], i) => `<article class="card">${picture(`${up}assets/${cardImgs[i]}.webp`, cardAlts[i])}<div class="body"><h3>${wrapEn(t)}</h3><p>${wrapEn(d)}</p><a class="more" href="${up}${lang}/${cardHrefs[i]}">${esc(l)} ${arrow}</a></div></article>`).join('\n  ')}
 </div>
</section>
<section class="on-texture">
 <div class="bg"><img src="${up}assets/tx-travertine.webp" alt="" loading="lazy"></div>
 <div class="wrap split reverse">
  <div class="copy"><h2>${br(c.homeApproach)}</h2><p>${wrapEn(c.homeApproachBody)}</p><div class="actions"><a class="button ghost" href="${up}${lang}/about/">${esc(c.aboutLink)} ${arrow}</a></div></div>
  <figure>${picture(`${up}assets/flatlay.webp`, a.flatlay)}${concept(c)}</figure>
 </div>
</section>
${cta({ c, lang, up })}`
}

// Amenities & packaging ------------------------------------------------------
function portfolio({ c, lang, up, a, legacyBody }) {
  return `${unifiedCollectionStage(lang, c, up)}
${legacyBody.slice(legacyBody.indexOf('<section class="section" id="formats">'), legacyBody.indexOf('<section class="section programmes"'))}
${beigeOpen(up, ' id="programmes"')}
 <div class="wrap">
  <div class="copy"><h2>${br(c.programmesHeading)}</h2></div>
  <div class="programmes" style="margin-top:clamp(28px,4vw,56px)">
   ${c.programmes.map(([t, d]) => `<div><h3><bdi lang="en">${esc(t)}</bdi></h3><p class="tag">${esc(c.programmeStatus)}</p><p style="margin-top:12px">${esc(d)}</p></div>`).join('\n   ')}
  </div>
 </div>
</section>
<section>
 <div class="wrap split">
  <div class="copy"><h2>${br(c.faqHeading)}</h2></div>
  <div>${c.faqs.map(([q, ans]) => `<details><summary>${esc(q)}</summary><p>${wrapEn(ans)}</p></details>`).join('\n  ')}</div>
 </div>
</section>
${cta({ c, lang, up })}`
}

// About ----------------------------------------------------------------------
function about({ c, lang, up, a }) {
  const rtl = lang === 'ar'
  const heroSrc = rtl ? 'lobby' : 'vanity'
  const heroAlt = rtl ? a.lobby : a.vanity
  return `<section class="hero" aria-labelledby="h1">
 <picture><img src="${up}assets/${heroSrc}.webp" alt="${esc(heroAlt)}" fetchpriority="high" decoding="async"></picture>
 <div class="hero-copy">
  ${quarterArc}
  <h1 id="h1">${br(c.aboutH1)}</h1>
  <p class="intro">${esc(c.aboutIntro)}</p>
 </div>
</section>
<section>
 <div class="wrap split">
  <div class="copy"><h2>${br(c.aboutHeading)}</h2><p>${esc(c.aboutBody)}</p><p>${wrapEn(c.aboutBody2)}</p></div>
  <figure>${picture(`${up}assets/flatlay.webp`, a.flatlay)}${concept(c)}</figure>
 </div>
</section>
${beigeOpen(up)}
 <div class="wrap">
  <div class="copy"><h2>${br(c.principlesHeading)}</h2></div>
  <div class="principles" style="margin-top:clamp(28px,4vw,56px)">
   ${c.principles.map(([t, d]) => `<div><h3>${esc(t)}</h3><p>${esc(d)}</p></div>`).join('\n   ')}
  </div>
 </div>
</section>
<section class="tone-sand">
 <div class="wrap">
  <div class="copy"><h2>${br(c.audienceHeading)}</h2></div>
  <div class="audiences" style="margin-top:clamp(28px,4vw,56px)">
   ${c.audiences.map(([t, d]) => `<div><h3>${esc(t)}</h3><p>${esc(d)}</p></div>`).join('\n   ')}
  </div>
 </div>
</section>
${cta({ c, lang, up })}`
}

// Contact --------------------------------------------------------------------
function contact({ c, lang, up, a, legacyBody }) {
  return `<section class="tone-sand" style="padding-top:clamp(120px,14vw,180px)">
 <div class="wrap split">
  <div class="copy"><h1 style="font-size:clamp(36px,4.6vw,68px)">${br(c.contactH1)}</h1><p style="margin-top:24px">${esc(c.contactIntro)}</p></div>
  <figure>${picture(`${up}assets/carton.webp`, a.carton, { lazy: false })}${concept(c)}</figure>
 </div>
</section>
${legacyBody.slice(legacyBody.indexOf('<section class="section contact-layout">'))}`
}

export function refinedBody(key, lang, c, legacyBody) {
  return ({home, about, portfolio, contact})[key]?.({c, lang, up:'/', a:alt[lang], legacyBody}) ?? legacyBody
}
