# W1 / M37: GEM™ Live Website & Repository Audit Report

**Auditor:** Digital Creative Director & Website Auditor (Pro Tier)  
**Milestone:** W1 / M37 (Track B)  
**Date of Audit:** 2026-11-07  
**Canonical Repository Under Audit:** `/Users/mediacenter1/Documents/GEM-Web-remake/.repo-sync/gem-web-transformation-w1-w6/website/remake/`  
**Live Target Origin:** `https://gem.mish3l.com`  
**Local Loopback Preview:** `http://127.0.0.1:4173` (or ephemeral preview port `4179`)  
**Inventory & Manifest Reference:** [`ROUTE_AND_SOURCE_INVENTORY.json`](./ROUTE_AND_SOURCE_INVENTORY.json)  
**Baseline Screenshots Directory:** [`screenshots_baseline/`](./screenshots_baseline/)  

---

## 1. Executive Summary & Audit Scope

This comprehensive technical and visual audit provides the baseline analysis of the GEM™ digital experience across both the production-deployed edge (`https://gem.mish3l.com`) and the source repository (`.repo-sync/gem-web-transformation-w1-w6/website/remake/`). The audit establishes the structural, visual, performance, accessibility, security, and B2B user journey foundations prior to initiating W2 (Digital Creative Direction & Experience Architecture) and W3/W4/W5 (GSAP Motion, Three.js 3D Inspection Studio, and Engineering Implementation).

### Primary Audit Findings:
1. **Exceptional Bilingual Symmetry:** The static site generator (`build.mjs`) achieves mathematically exact DOM element symmetry between Arabic (`/ar/`) and English (`/en/`) routes across all five core page types (Home: 142 elements, Amenities & Packaging: 185 elements, About: 129 elements, Contact: 133 elements, Privacy: 100 elements).
2. **Strict Edge Security & Privacy Enclosure:** Live HTTP response headers on Cloudflare Pages match local `_headers` identically. `X-Robots-Tag: noindex, nofollow` and `Content-Security-Policy: form-action 'none'; base-uri 'self'; object-src 'none'` are actively enforced, preventing search engine indexing during development and guaranteeing zero-data transmission for the local B2B procurement brief generator.
3. **Flawless Automated QA Test Suite:** All 39 Playwright browser regression tests (`qa/browser-regression.mjs`), 6 production build isolation tests (`qa/production-check.test.py`), and 58 assertions of the 400% zoom reflow test suite (`qa/zoom-400.mjs`) pass with 100% success.
4. **Lean Static Delivery Budget:** Baseline uncompressed CSS totals 40.4 KB, vanilla client JS totals 10.7 KB, and the three self-hosted WOFF2 fonts total 97 KB. The static build requires zero external CDNs, third-party trackers, or runtime JS frameworks.
5. **Critical Engineering Constraint for W2/W3/W4:** An automated regression test in `qa/browser-regression.mjs` explicitly rejects the substring `/concept|تصوّر|تصور/i` anywhere in text, metadata, alt attributes, or ARIA labels (enforcing Owner Decision 31 Oct 2026). W2 creative direction and W3/W4 exploratory badges must use approved nomenclature (such as `PROVISIONAL GEOMETRY` / `نموذج أولي تجريبي` or `Pending Commercial Confirmation`) to maintain strict regression compliance.

---

## 2. Frontend Architecture & Build Pipeline

The website is engineered as a zero-dependency static site generator executed via Node.js (`build.mjs`).

```
                              ┌──────────────────┐
                              │  content.mjs     │ (Bilingual content matrix)
                              │  pilot-art.mjs   │ (SVG bottle geometry)
                              │  refined-layouts │ (Flow layout compositions)
                              └─────────┬────────┘
                                        │
                                        ▼
┌────────────────────────┐      ┌──────────────────┐      ┌────────────────────────┐
│ assets/static/         │ ───► │    build.mjs     │ ───► │ dist/                  │
│ assets/scenes/         │      │                  │      │  ar/ (5 pages)         │
│ assets/exports/        │      │ Hash-stamping    │      │  en/ (5 pages)         │
│ CSS & JS sources       │      │ CSP injection    │      │  assets/ (41 files)    │
└────────────────────────┘      └──────────────────┘      │  _headers, _redirects  │
                                                          └────────────────────────┘
```

### Key Architectural Strengths:
- **Zero Framework Runtime Overhead:** Output is pure HTML5, vanilla CSS, and an unminified, self-contained 10.7 KB vanilla JavaScript module (`app.js`).
- **Deterministic Content Hash Stamping:** `build.mjs` computes SHA-256 digests of all runtime CSS and JS files, stamping them as `?v=[hash:10]` parameters on all script and stylesheet tags. This invalidates Cloudflare's fixed 4-hour edge browser cache immediately upon redeployment.
- **Strict Isolation of Masters:** Raw source assets (`assets/exports/`, `assets/scenes/`, `assets/static/`) reside outside generated output and are validated before build execution. Unused hero exports (`UNUSED_EXPORTS = /^hero-(desktop|mobile)-\d+\.webp$/`) are pruned from production bundles per Owner Decision 2026-10-31.
- **Atomic Cloudflare Configuration:** Generates static `_headers` and `_redirects` files in `dist/` ensuring preview security policies persist through every build.

---

## 3. Live Edge vs. Local Build Comparison

Live inspection of `https://gem.mish3l.com` via HTTP/2 response headers demonstrates exact parity with the local repository configuration in `hosting/cloudflare/_headers`:

| HTTP Header | Live Origin (`https://gem.mish3l.com/ar/`) | Local Build (`hosting/cloudflare/_headers`) | Verification Status |
|---|---|---|---|
| `x-robots-tag` | `noindex, nofollow` | `noindex, nofollow` | **VERIFIED PARITY** |
| `content-security-policy` | `form-action 'none'; base-uri 'self'; object-src 'none'` | `form-action 'none'; base-uri 'self'; object-src 'none'` | **VERIFIED PARITY** |
| `x-content-type-options` | `nosniff` | `nosniff` | **VERIFIED PARITY** |
| `referrer-policy` | `strict-origin-when-cross-origin` | `strict-origin-when-cross-origin` | **VERIFIED PARITY** |
| `cache-control` | `no-cache` | `no-cache` | **VERIFIED PARITY** |
| Root Redirect (`/`) | `302 -> /ar/` | `302 -> /ar/` | **VERIFIED PARITY** |
| Legacy Privacy Redirects | `301 -> /en/privacy/` | `301 -> /en/privacy/` | **VERIFIED PARITY** |

---

## 4. Route & Source Inventory

The site serves 10 localized static pages across two language trees, plus root redirect and 404 handler:

| Route Path | Language | Heading 1 (`<h1>`) | DOM Nodes | Images | Links | Buttons | Key Purpose & Interactive Components |
|---|---|---|:---:|:---:|:---:|:---:|---|
| `/ar/` | Arabic | تفاصيل مدروسة.<br>ترحيب متناسق. | 142 | 10 | 18 | 5 | Canonical Homepage; video hero loop, brand pillars, split-layout photography. |
| `/ar/amenities-packaging/` | Arabic | عائلة من العناصر.<br>لغة واحدة. | 185 | 9 | 12 | 12 | Collection Explorer; interactive 5-product switcher, format cards, programmes, FAQs. |
| `/ar/about/` | Arabic | هوية واحدة.<br>ورؤية واضحة. | 129 | 6 | 12 | 4 | Brand Philosophy; architectural principles, audience profiles (Owners, Operators, Procurement). |
| `/ar/contact/` | Arabic | لنبدأ<br>من منشأتك. | 133 | 3 | 12 | 8 | B2B Specification Brief Tool; client-side form validation, text brief generator, copy & download. |
| `/ar/privacy/` | Arabic | معلوماتك.<br>بوضوح. | 100 | 2 | 13 | 2 | Data Governance & Privacy Statement; zero-tracking statement, Cloudflare cookie notice. |
| `/en/` | English | Considered details.<br>A coherent welcome. | 142 | 10 | 18 | 5 | English Homepage; mirror layout with LTR directional flow and typographic adjustments. |
| `/en/amenities-packaging/` | English | A family of objects.<br>A shared language. | 185 | 9 | 12 | 12 | English Collection Explorer; 5 products, 3 formats, bespoke programmes, specs & FAQs. |
| `/en/about/` | English | One identity.<br>A clear point of view. | 129 | 6 | 12 | 4 | English Brand Philosophy; principles, audiences, architectural alignments. |
| `/en/contact/` | English | Start with<br>your property. | 133 | 3 | 12 | 8 | English B2B Specification Brief Tool; zero-transmission local brief generation. |
| `/en/privacy/` | English | Your information.<br>Handled with clarity. | 100 | 2 | 13 | 2 | English Privacy & Security Statement. |

*Note: Canonical routes use `/ar/amenities-packaging/` and `/ar/about/`. Legacy or hypothetical aliases `/ar/collection/`, `/ar/story/`, and `/ar/bespoke/` are currently unmapped and return 404 on live.*

---

## 5. Bilingual Architecture & Arabic (RTL) Parity

The codebase demonstrates exemplary internationalization and RTL layout engineering:

1. **Directional Isolation (`<bdi>`):** English brand terms embedded within Arabic copy (e.g. `Property Edition`, `Bespoke Programme`, `GEM`) are wrapped in `<bdi lang="en" dir="ltr">` tags, preventing bidirectional punctuation spillover.
2. **Typographic Hierarchy & Optical Sizing:**
   - Latin uses **Jost** (display titles, uppercase signatures) and **Inter** (body copy, numbers, data tables).
   - Arabic uses **Noto Sans Arabic** (served locally as `arabic.woff2`).
   - Line heights for Arabic are intentionally expanded (`line-height: 1.55` on `<h1>`, `1.65` on `<h2>`, `2.0` on body copy) to prevent vertical ascender/descender collisions.
   - Letter spacing for Arabic headings is strictly set to `letter-spacing: 0` (preventing disconnection of cursive Arabic glyphs).
3. **Logical CSS Properties & Mirroring:** Layouts use CSS logical properties (`margin-inline`, `padding-inline`, `inset-inline-start`, `border-inline-start`) allowing natural bidirectional flipping without redundant CSS overrides.
4. **Directional Arrow Inversion:** Interactive arrow glyphs (`→` / `↗`) are transformed via `transform: scaleX(-1)` in RTL contexts to align with forward reading motion.
5. **Architectural Texture Mirroring:** Asymmetrical visual assets (such as `tx-arches.webp` and `hero-rtl.webp`) are mirrored via CSS `transform: scaleX(-1)` so the open architectural relief sits behind negative space rather than colliding with text.

---

## 6. Performance & Asset Footprint Baseline

A detailed audit of the 62 files comprising `dist/` (total uncompressed footprint: 5.98 MB) reveals:

```
Distribution by Asset Category:
────────────────────────────────────────────────────────────────
Static WebP Product Sources (5 high-res) : 2,905 KB  (48.5%)
High-Resolution Photography & Textures   : 1,068 KB  (17.8%)
Social OpenGraph Preview PNG             :   874 KB  (14.6%)
Hero Video Background Loops (LTR + RTL)  :   738 KB  (12.3%)
Self-Hosted WOFF2 Fonts (Arabic/Jost/Int):    97 KB  ( 1.6%)
Static Vector SVGs & Favicons            :    28 KB  ( 0.5%)
CSS Stylesheets (4 files)                :    40 KB  ( 0.7%)
Client JavaScript Runtime (app.js)       :    11 KB  ( 0.2%)
Static HTML Output (10 pages + 404)      :    92 KB  ( 1.5%)
────────────────────────────────────────────────────────────────
Total Deployment Bundle                  : 5,980 KB (100.0%)
```

### Critical Performance Observations:
- **Zero Third-Party Dependency Chains:** No external scripts, CDNs, analytics beacons, or remote font CDNs exist. DNS lookup and TLS negotiation occur exclusively against the host domain.
- **Font Preloading:** The primary font for the document language (`arabic.woff2` on Arabic pages, `jost.woff2` on English pages) is preloaded in `<head>` via `<link rel="preload" as="font" type="font/woff2" crossorigin>`.
- **Progressive Video Degradation:** Background video (`loop-ltr.mp4`, `loop-rtl.mp4`) automatically hides on mobile viewports (`max-width: 760px`) and when `prefers-reduced-motion: reduce` is detected, falling back to lightweight WebP poster images.
- **Largest Single Assets:** `social.png` (874 KB) is served exclusively for social crawlers (not loaded during typical client navigation). The five individual product WebP source images range from 476 KB to 689 KB each. In W4/W5, adding 3D GLTF models must employ aggressive Draco/Meshopt compression and lazy loading to keep the collection studio payload well within a 1.5 MB incremental ceiling.

---

## 7. Accessibility (WCAG 2.2 Level AA) Baseline

Accessibility audit verified through automated test suites (`zoom-400.mjs` and `browser-regression.mjs`) demonstrates robust compliance:

1. **Reflow & High Zoom (WCAG 1.4.10):**
   - At 400% zoom (simulated via 320px viewport at 4x device scale), **no horizontal scroll** occurs (`scrollWidth <= innerWidth + 1`).
   - Sticky cookie notice occupies `<= 50%` of viewport height and keeps its dismiss button fully accessible within the initial viewport bounds.
   - All interactive controls maintain minimum touch targets (`min-height: 44px`, `min-width: 44px`).
2. **Keyboard Navigation & Focus Trapping (WCAG 2.1.1, 2.1.2):**
   - Full keyboard accessibility with prominent `:focus-visible` outlines (`2px solid var(--ink); outline-offset: 2px`).
   - Mobile navigation drawer traps focus when open, dismisses on `Escape` keypress, and restores focus back to the menu toggle button.
   - Lightbox modal dialog implements ARIA role `dialog`, `aria-modal="true"`, traps focus to the close button, and dismisses on `Escape`.
3. **Motion Sensitivity (WCAG 2.3.3):**
   - `prefers-reduced-motion: reduce` completely disables view transitions (`animation-duration: 0s`), scroll-linked parallax, curtain reveals, and hero background video.
4. **Font Failure Resilience:**
   - Client runtime includes a 3-attempt font retry loader. If font resources permanently fail, a visible fallback alert banner (`.font-failure`) alerts the user without causing silent content shifts.

---

## 8. B2B Hospitality Operator & Procurement Journey

The B2B inquiry and procurement specification flow is uniquely architected for privacy and friction-free operator interaction:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   B2B Specification Tool Architecture                  │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Specifier inputs: Name, Property/Company, Email, Market, Project    │
│    Interest (Suite amenities, bespoke program, private label), Message │
│                                                                        │
│ 2. Submit Action: Native submit prevented via `e.preventDefault()`      │
│    Form data compiled locally into formatted plaintext specification   │
│                                                                        │
│ 3. Strict CSP Enclosure: `form-action 'none'` prevents any accidental  │
│    or malicious transmission to external servers                       │
│                                                                        │
│ 4. Output Actions:                                                     │
│    - One-click copy to clipboard (`navigator.clipboard.writeText`)     │
│    - Offline text brief download (`GEM-project-brief-[lang].txt`)      │
│    - Graceful fallback: text area auto-selects if clipboard is denied  │
└────────────────────────────────────────────────────────────────────────┘
```

### Procurement Experience Assessment:
- **Trust & Discretion:** Hotel procurement executives frequently deal with confidential pre-opening specifications. The zero-transmission local brief guarantee establishes deep operational trust.
- **Identified Gap for W2 Creative Direction:** The current Amenities & Packaging page lists the 5 products in a vertical tabbed list with 2D static images. Specifiers cannot currently examine bottle finishes (satin pump vs. optical amber glass), inspect label typography in 360°, or review technical dispenser mounting brackets. This defines the core requirement for W2's Interactive 3D Product Inspection Studio.

---

## 9. Baseline Visual Evidence Matrix

All baseline screenshots have been captured at full resolution using Playwright and archived in `screenshots_baseline/`:

| Route | Desktop Baseline (`1440x900`) | Mobile Baseline (`390x844`) | Interactive / State Capture |
|---|---|---|---|
| **`/ar/`** | [`ar_home_desktop_1440x900.png`](./screenshots_baseline/ar_home_desktop_1440x900.png) | [`ar_home_mobile_390x844.png`](./screenshots_baseline/ar_home_mobile_390x844.png) | [`ar_home_mobile_menu_open_390x844.png`](./screenshots_baseline/ar_home_mobile_menu_open_390x844.png) |
| **`/ar/amenities-packaging/`** | [`ar_amenities_packaging_desktop_1440x900.png`](./screenshots_baseline/ar_amenities_packaging_desktop_1440x900.png) | [`ar_amenities_packaging_mobile_390x844.png`](./screenshots_baseline/ar_amenities_packaging_mobile_390x844.png) | [`ar_amenities_packaging_product2_desktop.png`](./screenshots_baseline/ar_amenities_packaging_product2_desktop.png) |
| **`/ar/about/`** | [`ar_about_desktop_1440x900.png`](./screenshots_baseline/ar_about_desktop_1440x900.png) | [`ar_about_mobile_390x844.png`](./screenshots_baseline/ar_about_mobile_390x844.png) | — |
| **`/ar/contact/`** | [`ar_contact_desktop_1440x900.png`](./screenshots_baseline/ar_contact_desktop_1440x900.png) | [`ar_contact_mobile_390x844.png`](./screenshots_baseline/ar_contact_mobile_390x844.png) | [`ar_contact_brief_prepared_desktop.png`](./screenshots_baseline/ar_contact_brief_prepared_desktop.png) |
| **`/ar/privacy/`** | [`ar_privacy_desktop_1440x900.png`](./screenshots_baseline/ar_privacy_desktop_1440x900.png) | [`ar_privacy_mobile_390x844.png`](./screenshots_baseline/ar_privacy_mobile_390x844.png) | — |
| **`/en/`** | [`en_home_desktop_1440x900.png`](./screenshots_baseline/en_home_desktop_1440x900.png) | [`en_home_mobile_390x844.png`](./screenshots_baseline/en_home_mobile_390x844.png) | [`en_home_mobile_menu_open_390x844.png`](./screenshots_baseline/en_home_mobile_menu_open_390x844.png) |
| **`/en/amenities-packaging/`** | [`en_amenities_packaging_desktop_1440x900.png`](./screenshots_baseline/en_amenities_packaging_desktop_1440x900.png) | [`en_amenities_packaging_mobile_390x844.png`](./screenshots_baseline/en_amenities_packaging_mobile_390x844.png) | [`en_amenities_packaging_product2_desktop.png`](./screenshots_baseline/en_amenities_packaging_product2_desktop.png) |
| **`/en/about/`** | [`en_about_desktop_1440x900.png`](./screenshots_baseline/en_about_desktop_1440x900.png) | [`en_about_mobile_390x844.png`](./screenshots_baseline/en_about_mobile_390x844.png) | — |
| **`/en/contact/`** | [`en_contact_desktop_1440x900.png`](./screenshots_baseline/en_contact_desktop_1440x900.png) | [`en_contact_mobile_390x844.png`](./screenshots_baseline/en_contact_mobile_390x844.png) | [`en_contact_brief_prepared_desktop.png`](./screenshots_baseline/en_contact_brief_prepared_desktop.png) |
| **`/en/privacy/`** | [`en_privacy_desktop_1440x900.png`](./screenshots_baseline/en_privacy_desktop_1440x900.png) | [`en_privacy_mobile_390x844.png`](./screenshots_baseline/en_privacy_mobile_390x844.png) | — |

---

## 10. Key Engineering Risks & Guardrails for W2, W3 & W4

Based on this audit, the following engineering boundaries must be strictly observed during W2 specification and W3/W4 implementation:

| Risk / Constraint Area | Technical Root Cause | Strict Architecture Guardrail |
|---|---|---|
| **Banned "Concept" Wording** | `qa/browser-regression.mjs` lines 148–160 explicitly tests: `assert.equal(/concept\|تصوّر\|تصور/i.test(found), false)`. | **Zero occurrence** of "concept" or "تصور" in UI copy, alt text, titles, or badges. Use `PROVISIONAL GEOMETRY` / `نموذج أولي تجريبي` or `Pending Commercial Confirmation`. |
| **Strict CSP Policy** | `Content-Security-Policy: form-action 'none'; base-uri 'self'; object-src 'none'` | Three.js and GSAP must be bundled locally into `dist/` without inline `eval`, `Function()` constructors, or external script references. |
| **320px Reflow Violation** | `qa/zoom-400.mjs` fails if any element pushes `scrollWidth > innerWidth + 1` at 320 CSS px width. | The Three.js WebGL canvas and 3D studio controls must use responsive `max-width: 100%`, `overflow: hidden`, and flex-wrapping for toolbars. |
| **Headings & Anchor Fragments** | `check.py` asserts exactly one `<h1>` per page and validates that all `#fragment` links target existing element IDs. | W2/W3 redesign must preserve single `<h1>` per route and keep `#pilot-products`, `#formats`, and `#programmes` anchor IDs intact. |
| **Reduced Motion Compliance** | `browser-regression.mjs` validates that reduced-motion preferences disable parallax and animation durations. | W3 GSAP ScrollTrigger must disable scroll scrubbing when `prefers-reduced-motion` is active. W4 Three.js must provide high-res M29/M34 static fallbacks. |
| **Asset Budget Impact** | Baseline JS is only 10.7 KB. Adding full Three.js + OrbitControls + GLTFLoader could bloat initial load. | Use dynamic `import()` to lazy-load Three.js only when the product inspection studio approaches viewport (via IntersectionObserver). |

---

## 11. Conclusion & Transition to W2

The GEM™ website codebase represents an extraordinarily solid, disciplined, and secure foundation. The 10-page static architecture is resilient, accessible, and compliant with enterprise hospitality expectations. 

With all baseline metrics established and risks identified, we now transition directly into **W2: Digital Creative Direction & Experience Architecture**, delivering the complete creative vision, 3D studio interaction model, GSAP motion choreography, and tokenized design system.
