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
    turndown: 'Two GEM amber pump bottles on a wooden tray beside a branded GEM card and a linen napkin',
    lobby: 'GEM amber hand wash pump bottle on a stone plinth in front of a carved wall with lattice shadows',
    flatlay: 'GEM amber body wash pump bottle lying on linen beside an olive sprig and a branded GEM card',
    packaging: 'Branded GEM cream presentation boxes, a kraft carton and a GEM tag on travertine',
    carton: 'GEM amber shampoo pump bottle in front of a branded cream GEM carton on a stone shelf',
  },
  ar: {
    hero: 'عبوة شامبو زجاجية كهرمانية من GEM بمضخة على حافة من الترافرتين في ضوء الصباح، وبجانبها بطاقة GEM المطبوعة',
    family: 'خمس عبوات زجاجية كهرمانية من GEM بمضخات وملصقات ثنائية اللغة وبأطوال متدرجة على حافة من الترافرتين',
    vanity: 'عبوتان كهرمانيتان من GEM ومنشفة ملفوفة وبطاقة GEM على سطح حجري',
    turndown: 'عبوتان كهرمانيتان من GEM بمضخة على صينية خشبية بجانب بطاقة GEM ومنديل كتاني',
    lobby: 'عبوة غسول يدين كهرمانية من GEM بمضخة على قاعدة حجرية أمام جدار منحوت وظلال شبكية',
    flatlay: 'عبوة غسول جسم كهرمانية من GEM بمضخة على قماش كتاني بجانب غصن زيتون وبطاقة GEM',
    packaging: 'علب تقديم كريمية من GEM وعلبة كرافت وبطاقة GEM على سطح من الترافرتين',
    carton: 'عبوة شامبو كهرمانية من GEM بمضخة أمام علبة GEM كريمية على رف حجري',
  },
}


const arrow = '<span aria-hidden="true">→</span>'
const beigeOpen = (up, id = '') => `<section${id} class="tone-beige arc-section"><div class="arc-banner"><img src="${up}assets/tx-arches.webp" alt="" width="2752" height="1536" loading="lazy"></div>`
const picture = (src, a, { lazy = true, cls = '' } = {}) =>
  `<img src="${src}" alt="${esc(a)}"${lazy ? ' loading="lazy"' : ''} decoding="async">`

const cta = ({ c, lang, up }) => `<section class="cta on-texture veil">
 <div class="bg"><img src="${up}assets/tx-limewash.webp" alt="" loading="lazy"></div>
 <div class="wrap"><h2>${br(c.next)}</h2><p>${esc(c.nextBody)}</p>
 <div class="actions"><a class="button" href="${up}${lang}/contact/">${esc(c.discuss)} ${arrow}</a></div></div>
</section>`

const concept = (c) => `<figcaption>${esc(c.concept)}</figcaption>`

// Home ----------------------------------------------------------------------
function home({ c, lang, up, a }) {
  const rtl = lang === 'ar'
  const heroImg = rtl ? 'hero-rtl' : 'hero-ltr'
  const cardImgs = ['carton', 'packaging', 'lobby']
  const cardHrefs = ['amenities-packaging/#pilot-products', 'amenities-packaging/#concept-formats', 'amenities-packaging/#programmes']
  const cardAlts = [a.carton, a.packaging, a.lobby]
  return `<section class="hero portrait" aria-labelledby="h1">
 <picture>
  <source media="(max-width:760px)" srcset="${up}assets/hero-mobile.webp">
  <img src="${up}assets/${heroImg}.webp" alt="${esc(a.hero)}" fetchpriority="high" decoding="async">
 </picture>
 <video autoplay muted loop playsinline preload="metadata" poster="${up}assets/${heroImg}.webp" aria-hidden="true" tabindex="-1"><source src="${up}assets/loop-${rtl ? 'rtl' : 'ltr'}.mp4" type="video/mp4"></video>
 <div class="hero-copy">
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
  const prods = ['shampoo', 'conditioner', 'body-wash', 'body-lotion', 'hand-wash']
  const fmts = ['room', 'wall', 'travel']
  return `<section class="hero flip-rtl narrow-copy" aria-labelledby="h1">
 <picture><img src="${up}assets/family.webp" alt="${esc(a.family)}" fetchpriority="high" decoding="async"></picture>
 <div class="hero-copy">
  <h1 id="h1">${br(c.portfolioH1)}</h1>
  <p class="intro">${wrapEn(c.portfolioIntro)}</p>
  <p class="status">${esc(c.status)}</p>
 </div>
</section>
${legacyBody.slice(legacyBody.indexOf('<section class="section" id="pilot-products">'), legacyBody.indexOf('<section class="section programmes"'))}
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
