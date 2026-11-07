# W2: GEM™ Digital Creative Direction & Experience Architecture Specification

**Lead Author:** Digital Creative Director & UX Architect (Pro Tier)  
**Milestone:** W2 (Digital Creative Direction & Experience Architecture)  
**Target Release:** W3 (GSAP Motion), W4 (Three.js WebGL Studio), W5 (Engineering Build & Integration)  
**Governing Repo / Branch:** `.repo-sync/gem-web-transformation-w1-w6` (`development/website-transformation-w1-w6-20261107`)  
**Design Tokens:** [`DESIGN_TOKENS_AND_COMPONENT_MAP.json`](./DESIGN_TOKENS_AND_COMPONENT_MAP.json)  
**Motion & 3D Storyboards:** [`MOTION_AND_3D_STORYBOARDS.md`](./MOTION_AND_3D_STORYBOARDS.md)  
**Baseline Audit Reference:** [`../w1_audit/W1_CURRENT_STATE_AUDIT.md`](../w1_audit/W1_CURRENT_STATE_AUDIT.md)  

---

## 1. Executive Vision & Brand Narrative

GEM™ occupies a rarefied position in the luxury hospitality ecosystem: it is neither an artisanal boutique curio nor an anonymous industrial contract packager. GEM™ is an **architectural hospitality partner**, serving hotel owners, sovereign hospitality funds, interior architects, and executive procurement teams throughout the Kingdom of Saudi Arabia and the wider Arabian Gulf.

### Brand Core Tenets:
- **"HOSPITALITY, IN PERFECT PROPORTION" / "ضيافة متناسقة الأبعاد":** Proportional harmony governed by classical architectural canons. The height-to-width ratio of the amber bottle mirrors Mediterranean archways; the typography respects axial symmetry; the label hierarchy establishes immediate clarity.
- **"Every arrival, precisely composed" / "كل تفصيل مدروس لاستقبال متكامل":** The guest's first interaction with an amenity bottle in a five-star suite is a tactile arrival ceremony. The satin-finish pump, the cool optical amber glass, and the ceramic screen-printed typography form an indelible impression of hospitality discernment.
- **Material Honesty & Functional Rigor:** True optical amber glass is not a decorative affectation; it provides laboratory-grade UV filtration safeguarding natural essential oils from photochemical oxidation. Tamper-evident wall brackets secure amenities without destroying wall integrity.

---

## 2. Brand Visual Tokens & Palette Architecture

The design token system is grounded in natural Mediterranean and Arabian architectural materials: honed travertine limestone, dark patinated bronze, obsidian pump actuators, and pharmaceutical amber glass.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        GEM™ Color Architecture                         │
├──────────────────┬──────────────────┬──────────────────┬───────────────┤
│ Ink (#12171D)    │ Beige (#BCACA7)  │ Obsidian (#020202) Crisp White   │
│ High-contrast    │ Packaging linen, │ Pump satin, deep │ Label paper,  │
│ text, solid fill │ warm neutral     │ shadow anchor    │ inverted text │
├──────────────────┼──────────────────┼──────────────────┼───────────────┤
│ Amber (#C87D32)  │ Sand (#EFE6D8)   │ Ivory (#F8F3EA)  │ Line Overlay  │
│ Optical glass,   │ Travertine stone,│ Canvas ground,   │ rgba(18,23,29,│
│ hotspot accent   │ card backdrop    │ frosted surface  │ 0.16) border  │
└──────────────────┴──────────────────┴──────────────────┴───────────────┘
```

### CSS Custom Properties Implementation (to be added to `style.css`):
```css
:root {
  /* Brand Chromatic Tokens */
  --color-ink: #12171D;
  --color-beige: #BCACA7;
  --color-obsidian: #020202;
  --color-white: #FFFFFF;
  --color-amber: #C87D32;
  --color-sand: #EFE6D8;
  --color-ivory: #F8F3EA;
  --color-line: rgba(18, 23, 29, 0.16);
  --color-line-strong: rgba(18, 23, 29, 0.32);
  --color-glass-surface: rgba(248, 243, 234, 0.86);

  /* Spacing & Layout Geometry */
  --edge: clamp(20px, 5vw, 88px);
  --container-max: 1280px;
  --container-wide: 1440px;
  --gap: clamp(20px, 3vw, 44px);

  /* Motion & Easing */
  --ease-luxury: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-material: cubic-bezier(0.25, 0.1, 0.25, 1);
  --dur-swift: 0.28s;
  --dur-deliberate: 0.65s;
  --dur-majestic: 1.10s;
}
```

---

## 3. Typographic System & Bilingual Hierarchy

The typographic foundation combines the crisp geometric precision of **Jost** (Latin display) and **Inter** (Latin functional body) with the calligraphic elegance of **Noto Sans Arabic** (`arabic.woff2`).

```
Typographic Scale:
──────────────────────────────────────────────────────────────────────────
Level           Latin (Jost / Inter)               Arabic (Noto Sans Arabic)
──────────────────────────────────────────────────────────────────────────
Display Hero    clamp(46px, 5.8vw, 88px)           clamp(40px, 4.8vw, 70px)
                Line-height: 1.08                  Line-height: 1.52
                Letter-spacing: -0.025em           Letter-spacing: 0

Section H2      clamp(28px, 3.2vw, 46px)           clamp(26px, 2.8vw, 40px)
                Line-height: 1.20                  Line-height: 1.62
                Letter-spacing: -0.015em           Letter-spacing: 0

Subheading H3   clamp(20px, 2.0vw, 26px)           clamp(20px, 2.0vw, 25px)
                Line-height: 1.30                  Line-height: 1.68

Body Lead       clamp(17px, 1.35vw, 19px)          clamp(17px, 1.45vw, 20px)
                Line-height: 1.80 (Inter)          Line-height: 2.00 (Arabic)

Body Regular    16px                               16px
                Line-height: 1.75 (Inter)          Line-height: 1.95 (Arabic)

Signature Tag   11px                               12px
                Letter-spacing: 0.18em             Letter-spacing: 0
                Text-transform: uppercase          Text-transform: none
```

### Essential RTL Rules:
1. **Zero Headings Letter-Spacing:** Never apply negative or positive letter-spacing to Arabic text (`letter-spacing: 0`). Connected cursive scripts sever glyph joins when letter-spacing is applied.
2. **Generous Vertical Breathing Room:** Arabic diacritics and tall vertical ascenders (`ا`, `ل`, `ك`) require 15% to 25% higher line-height than Latin text to prevent visual cramping.
3. **Directional Isolation (`<bdi>`):** All brand monikers (`GEM`, `Property Edition`, `Bespoke Programme`) must be enclosed in `<bdi lang="en" dir="ltr">` inside Arabic templates.

---

## 4. Geometric & SVG Iconography Vocabulary

Three proprietary geometric vectors govern the visual interface:

1. **The GEM Ring (Circular Seal):**
   ```xml
   <svg class="gem-ring" viewBox="0 0 48 48" aria-hidden="true">
     <circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
     <circle cx="24" cy="24" r="14" fill="none" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2 2"/>
   </svg>
   ```
   *Semantic:* Represents circular perfection, the seal of quality, and continuous hotel suite replenishing cycles.

2. **The Quarter-Arc (Travertine Archway Motif):**
   ```xml
   <svg class="quarter-arc" viewBox="0 0 64 64" aria-hidden="true">
     <path d="M0 64 A64 64 0 0 1 64 0" fill="none" stroke="currentColor" stroke-width="1.2"/>
   </svg>
   ```
   *Semantic:* Echoes the architectural arch relief in Mediterranean and Middle Eastern palatial hospitality. Used as a structural framing corner for product imagery.

3. **The Four-Point Spark (Hotspot & Precision Focus):**
   ```xml
   <svg class="four-point-spark" viewBox="0 0 24 24" aria-hidden="true">
     <path d="M12 2 Q12 12 22 12 Q12 12 12 22 Q12 12 2 12 Q12 12 12 2 Z" fill="currentColor"/>
   </svg>
   ```
   *Semantic:* Used as the interactive inspection hotspot anchor in the 3D studio, indicating technical highlights.

---

## 5. Experience Concept Architecture

### Concept 1: The Cinematic Hero
- **Visual Staging:** Architectural portrait framing uniting the M29 master photography on a honed travertine plinth with restrained lighting.
- **Motion Integration:** Restrained GSAP entrance timeline unmasking the background, drawing the quarter-arc framing stroke, and lifting the bilingual editorial headline with split-line stagger.
- **Commercial Availability Guardrail:** Subdued, clear disclaimer: `Commercial availability not established / التوافر التجاري غير مؤكد`.

### Concept 2: Scroll-Driven Collection Reveal (The Five Products)
- **Narrative Sequence:**
  1. `01 / Shampoo / شامبو` — Verified M29 Standard (450ml).
  2. `02 / Conditioner / بلسم` — Verified M29 Standard (450ml).
  3. `03 / Body Wash / غسول الجسم` — Provisional Geometry M34 (450ml).
  4. `04 / Body Lotion / لوشن الجسم` — Provisional Geometry M34 (450ml).
  5. `05 / Hand Wash / غسول اليدين` — Provisional Geometry M34 (300ml).
- **Strict Nomenclature Requirement:** To satisfy `qa/browser-regression.mjs` (which bans `/concept|تصوّر|تصور/i`), models are badged as:
  - M29 baseline: `VERIFIED STANDARD` / `معيار معتمد`.
  - M34 exploratory models: `PROVISIONAL GEOMETRY` / `نموذج أولي تجريبي`.

### Concept 3: Interactive 3D Product Inspection Studio (Three.js)
- **Operator Functionality:** A high-performance WebGL studio allowing procurement officers and hotel general managers to:
  1. Examine the bottle in 360° horizontal rotation with natural inertial damping.
  2. Toggle between all 5 collection products with smooth cross-dissolve mesh transitions.
  3. Switch lighting environments between *Studio Lookdev*, *Warm Suite (2700K)*, and *Architectural Daylight*.
  4. Activate 3D callout hotspots exposing technical specifications (Optical UV Amber Filtration, Satin Pump Ergonomics, and Screen-Printed Label Durability).
- **Graceful Fallback:** If WebGL is unavailable or `prefers-reduced-motion` is active, the component immediately falls back to high-resolution M29/M34 photographic plates, accompanied by accessible semantic tabs.

### Concept 4: Brand Narrative & Proportion System
- **Storytelling Section (`/about/`):** Explains the four architectural principles:
  1. *Geometric Proportion:* Bottle dimensions derived from classical golden ratios.
  2. *Optical Preservation:* Heavy amber glass shielding delicate botanicals from UV light.
  3. *Tactile Restraint:* Satin finish pumps calibrated for silent, effortless 2.0ml actuation.
  4. *Architectural Integration:* Dispenser brackets engineered to integrate seamlessly into travertine, marble, and limewash walls without visible fixing bolts.

### Concept 5: B2B Hospitality Operator & Procurement Pathway
- **Amenity Specification Table:** Clear technical breakdown of capacities, neck finishes, wall-mount bracket dimensions, and replenishment carton pack sizes.
- **Confidential Local Project Brief Generator (`/contact/`):**
  - Allows hotel operators to select property type (Boutique, Luxury Resort, City Hotel, Sovereign Palace), estimated key count, and required delivery formats.
  - Generates an instant, client-side formatted plaintext brief.
  - Zero external network transmission (guaranteed by CSP `form-action 'none'`).
  - One-click copy to clipboard or offline download as `GEM-project-brief-[lang].txt`.

### Concept 6: First-Class Bilingual & RTL Architecture
- Complete symmetrical parity across `/ar/` and `/en/`.
- Logical CSS layout (`margin-inline`, `padding-inline`, `inset-inline-start`).
- Motion vectors reverse in RTL (e.g. entrance sweeps move leftward; horizontal scrub triggers mirror).

---

## 6. Implementation Architecture for W3 (GSAP) & W4 (Three.js)

To maintain 100% compliance with existing regression checks (`check.py`, `qa/production-check.test.py`, `qa/browser-regression.mjs`, `qa/zoom-400.mjs`):

```
website/remake/
├── build.mjs                  # Updates template to load motion modules conditionally
├── content.mjs                # Enriches product technical specs & honest badges
├── style.css                  # Core layout & typography
├── motion.css                 # Dedicated CSS for GSAP & 3D canvas transitions
├── app.js                     # Existing navigation, form, and lightbox shell
├── modules/
│   ├── motion.js              # W3: GSAP + ScrollTrigger module (lazy-loaded)
│   └── studio3d.js            # W4: Three.js WebGL Inspection Studio (lazy-loaded)
└── assets/
    ├── models/                # Optimized GLB models (shampoo.glb, conditioner.glb, etc.)
    └── scenes/                # Static fallback plates
```

### Script Loading & CSP Strategy:
Both `motion.js` and `studio3d.js` will be compiled into the static build pipeline in `build.mjs`, stamped with SHA-256 hashes (`?v=[hash]`), and loaded as native ES modules with dynamic `import()`:

```javascript
// Lazy-load Three.js studio only when approaching viewport
const studioEl = document.getElementById('inspection-studio');
if (studioEl && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      import('/studio3d.js' + window.__v_studio).then(mod => mod.initStudio(studioEl));
      observer.disconnect();
    }
  }, { rootMargin: '200px 0px' });
  observer.observe(studioEl);
}
```

---

## 7. Verification & Acceptance Criteria for W3–W5

Before milestone completion, the implementation must satisfy:
1. `python3 check.py` passes with code 0 (10 localized pages, single H1, valid internal links and anchor IDs).
2. `python3 qa/production-check.test.py` passes with code 0 (disposable clean builds, hash stamping, preview headers).
3. `node qa/browser-regression.mjs` passes with code 0 (all 39 tests pass, zero forbidden "concept" wording).
4. `node qa/zoom-400.mjs` passes with code 0 (all 58 tests pass at 320px zoom without horizontal overflow).
5. Initial DOM First Contentful Paint (FCP) remains under 1.2s on desktop and 1.8s on mobile.
6. Three.js studio maintains steady 60fps on desktop and 30-60fps on mobile without memory accumulation.

---

## 8. Summary

This specification unites classical luxury hospitality aesthetics with contemporary web engineering rigor. It honors GEM™'s architectural identity, respects internationalization and accessibility standards, and sets an unambiguous path for W3 motion engineering and W4 3D studio development.
