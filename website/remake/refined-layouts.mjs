// Approved Flow layout compositions. Engineering shell and interactions stay in build.mjs.
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const br = (s) => esc(s).replace(/\n/g, '<br>')
const wrapEn = (s) => esc(s).replace(/(Property Edition|Bespoke Programme|GEM)/g, '<bdi lang="en">$1</bdi>')

// Alt text for the generated scene images. Arabic alt text needs native review like all Arabic copy.
const alt = {
  en: {
    hero: 'GEM amber glass shampoo pump bottle on a travertine ledge in soft morning light, with a branded GEM card beside it',
    family: 'Five GEM amber glass pump bottles in graduated heights with bilingual Arabic and English labels on a travertine ledge',
    vanity: 'Two GEM amber bottles, a rolled towel and a branded GEM card on a stone vanity',
    turndown: 'A GEM amber Body Wash and a cream Body Lotion, both with pumps, on a wooden tray beside a branded GEM card and a linen napkin',
    lobby: 'GEM cream Hand Wash pump bottle on a stone plinth in front of a carved wall with lattice shadows',
    flatlay: 'GEM amber body wash pump bottle lying on linen beside an olive sprig and a branded GEM card',
    packaging: 'Branded GEM cream presentation boxes, a kraft carton and a GEM tag on travertine',
    carton: 'GEM amber shampoo pump bottle in front of a branded cream GEM carton on a stone shelf',
  },
  ar: {
    hero: 'عبوة شامبو زجاجية كهرمانية من GEM بمضخة على حافة من الترافرتين في ضوء الصباح، وبجانبها بطاقة GEM المطبوعة',
    family: 'خمس عبوات زجاجية كهرمانية من GEM بمضخات وملصقات ثنائية اللغة وبأطوال متدرجة على حافة من الترافرتين',
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

function studio3D(lang, c) {
  const ar = lang === 'ar'
  const title = ar ? 'استوديو المعاينة ثلاثية الأبعاد والتناسب البصري' : 'Interactive 3D Optics & Proportion Studio'
  const lead = ar
    ? 'افحص نماذج العبوات الخمس بزاوية 360 درجة، وبدّل بين إعدادات الإضاءة المعمارية، واستعرض تفاصيل الزجاج الكهرماني ومضخة الساتان والملصق ثنائي اللغة.'
    : 'Inspect all five hospitality bottles in 360°, switch architectural lighting rigs, and examine the optical amber glass, satin pump profile, and bilingual ink label.'
  const mode3d = ar ? 'معاينة ثلاثية الأبعاد (GLB)' : 'Interactive 3D (GLB)'
  const modePlate = ar ? 'صورة استوديو مرجعية' : 'Studio Still Plate'
  const lightLabel = ar ? 'إعداد الإضاءة' : 'Lighting environment'
  const lights = ar
    ? [['studio', 'استوديو 85 مم'], ['suite', 'إضاءة جناح دافئة'], ['daylight', 'ضوء نهاري معماري']]
    : [['studio', '85mm Studio'], ['suite', 'Warm Suite'], ['daylight', 'Daylight']]
  const hotspotLabel = ar ? 'زاوية الفحص البصري' : 'Inspection focus'
  const hotspots = ar
    ? [['front', 'الملصق ثنائي اللغة'], ['glass', 'بصريات الزجاج الكهرماني'], ['pump', 'مضخة الساتان الهندسية']]
    : [['front', 'Bilingual Ink Label'], ['glass', 'Amber Glass Optics'], ['pump', 'Satin Pump Profile']]
  const badgeBaseline = ar ? 'خط الأساس المعتمد · معايرة بصرية M27a/M28' : 'Verified CGI Baseline · M27a/M28 Optical Calibration'
  const rotLeft = ar ? 'تدوير لليسار' : 'Rotate left'
  const rotReset = ar ? 'إعادة الضبط' : 'Reset angle'
  const rotRight = ar ? 'تدوير لليمين' : 'Rotate right'
  const canvasLabel = ar
    ? 'عارض ثلاثي الأبعاد تفاعلي لعبوات GEM — اسحب للتدوير أو استخدم أزرار التحكم'
    : 'Interactive 3D viewer for GEM bottles — drag to rotate or use the turntable buttons'
  const fallbackAlt = ar
    ? 'معاينة استوديو لعبوة شامبو GEM الزجاجية الكهرمانية بملصق ثنائي اللغة'
    : 'Studio render of the GEM amber glass Shampoo bottle with bilingual ink label'
  const specDefault = ar
    ? 'شامبو · زجاج كهرماني بمعامل انكسار 1.520 · 20,460 مضلعًا · إضاءة استوديو 85 مم'
    : 'Shampoo · Optical Amber Glass (IOR 1.520) · 20,460 polygons · 85mm Studio Lookdev'

  return `<section class="section studio-3d-section" id="interactive-3d-studio" aria-labelledby="studio-3d-heading">
 <div class="wrap">
  <div class="studio-3d-header">
   <div class="copy">
    <p class="studio-3d-eyebrow">${ar ? 'معاينة رقمية تفاعلية · W4 WebGL2 / glTF 2.0' : 'INTERACTIVE DIGITAL TWIN · W4 WebGL2 / glTF 2.0'}</p>
    <h2 id="studio-3d-heading">${esc(title)}</h2>
    <p class="lead">${esc(lead)}</p>
   </div>
   <div class="studio-3d-meta">
    <p id="studio-3d-badge" class="studio-3d-badge" data-status="baseline" aria-live="polite">${esc(badgeBaseline)}</p>
    <div class="studio-3d-modes" role="group" aria-label="${ar ? 'وضع العرض' : 'Display mode'}">
     <button type="button" class="studio-btn" data-studio-mode="3d" aria-pressed="true">${esc(mode3d)}</button>
     <button type="button" class="studio-btn" data-studio-mode="plate" aria-pressed="false">${esc(modePlate)}</button>
    </div>
   </div>
  </div>
  <div class="studio-3d-grid">
   <div class="studio-3d-controls">
    <div class="studio-control-group" role="group" aria-label="${ ar ? 'اختيار المنتج للمعاينة ثلاثية الأبعاد' : 'Select product for 3D inspection' }">
     <p class="studio-control-label">${ar ? 'المنتج (5 عبوات)' : 'Product family (5 bottles)'}</p>
     <div class="studio-product-pills">
      ${c.productNames.map((p, i) => `<button type="button" class="studio-pill" data-studio-product="${i}" aria-pressed="${i === 0}"><span class="index">0${i + 1}</span><span>${esc(p)}</span></button>`).join('')}
     </div>
    </div>
    <div class="studio-control-group" role="group" aria-label="${esc(lightLabel)}">
     <p class="studio-control-label">${esc(lightLabel)}</p>
     <div class="studio-pill-row">
      ${lights.map(([k, lbl], i) => `<button type="button" class="studio-chip" data-lighting="${k}" aria-pressed="${i === 0}">${esc(lbl)}</button>`).join('')}
     </div>
    </div>
    <div class="studio-control-group" role="group" aria-label="${esc(hotspotLabel)}">
     <p class="studio-control-label">${esc(hotspotLabel)}</p>
     <div class="studio-pill-row">
      ${hotspots.map(([k, lbl], i) => `<button type="button" class="studio-chip" data-hotspot="${k}" aria-pressed="${i === 0}">${esc(lbl)}</button>`).join('')}
     </div>
    </div>
    <div class="studio-readout-box" aria-live="polite">
     <p id="gem-3d-readout" class="studio-readout-title">${esc(specDefault)}</p>
     <p id="gem-3d-hotspot-note" class="studio-readout-note">${ar ? 'الملصق ثنائي اللغة: خلفية حبرية #12171D مع طباعة عربية وإنجليزية متوازنة وقوس ربع دائري.' : 'Bilingual Ink Label: #12171D matte ink field with balanced Arabic/English typography and architectural quarter-arc.'}</p>
    </div>
   </div>
   <div class="studio-3d-viewport" id="gem-3d-viewport" data-lighting-active="studio">
    <canvas id="gem-3d-canvas" width="960" height="720" tabindex="0" role="img" aria-label="${esc(canvasLabel)}"></canvas>
    <img id="gem-3d-fallback-plate" src="/assets/gem_shampoo_hero.webp" width="960" height="1200" alt="${esc(fallbackAlt)}" loading="lazy" decoding="async" hidden>
    <div class="studio-turntable-bar" role="group" aria-label="${ar ? 'التحكم بدوران العبوة' : 'Turntable rotation controls'}">
     <button type="button" class="studio-turn-btn" data-turntable="left" aria-label="${esc(rotLeft)}">↺</button>
     <button type="button" class="studio-turn-btn" data-turntable="reset">${esc(rotReset)}</button>
     <button type="button" class="studio-turn-btn" data-turntable="right" aria-label="${esc(rotRight)}">↻</button>
    </div>
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
  return `<section class="hero portrait" aria-labelledby="h1">
 <picture>
  <source media="(max-width:760px)" srcset="${up}assets/hero-mobile.webp">
  <img src="${up}assets/${heroImg}.webp" alt="${esc(a.hero)}" fetchpriority="high" decoding="async">
 </picture>
 <video autoplay muted loop playsinline preload="metadata" poster="${up}assets/${heroImg}.webp" aria-hidden="true" tabindex="-1"><source src="${up}assets/loop-${rtl ? 'rtl' : 'ltr'}.mp4" type="video/mp4"></video>
 <div class="hero-copy">
  ${quarterArc}
  <h1 id="h1">${br(c.homeH1)}</h1>
  <p class="intro">${wrapEn(c.homeIntro)}</p>
  <div class="actions"><a class="button" href="${up}${lang}/amenities-packaging/">${esc(c.explore)} ${arrow}</a><a class="button ghost" href="${up}${lang}/contact/">${esc(c.discuss)}</a></div>
  <p class="status">${esc(c.status)}</p>
 </div>
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
  const rtl = lang === 'ar'
  const familyImg = rtl ? 'family-rtl' : 'family'
  const prods = ['shampoo', 'conditioner', 'body-wash', 'body-lotion', 'hand-wash']
  const fmts = ['room', 'wall', 'travel']
  return `<section class="hero narrow-copy" aria-labelledby="h1">
 <picture><img src="${up}assets/${familyImg}.webp" alt="${esc(a.family)}" fetchpriority="high" decoding="async"></picture>
 <div class="hero-copy">
  ${quarterArc}
  <h1 id="h1">${br(c.portfolioH1)}</h1>
  <p class="intro">${wrapEn(c.portfolioIntro)}</p>
  <p class="status">${esc(c.status)}</p>
 </div>
</section>
${legacyBody.slice(legacyBody.indexOf('<section class="section" id="pilot-products">'), legacyBody.indexOf('<section class="section" id="formats">'))}
${studio3D(lang, c)}
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
  const f = c.form
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
