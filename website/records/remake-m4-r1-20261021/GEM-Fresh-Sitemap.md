# GEM — fresh website sitemap

Planning baseline: the five business answers approved by the owner on 20 October 2026. This is a new sitemap proposal for review. No previous website drafts, navigation, URLs, or sitemap structures were used.

Scope: Saudi-first B2B hospitality audience, wider GCC secondary; Arabic and English at launch, Arabic default; primary action **Discuss your project**. Concepts and pending programmes are not represented as available products. Approval of the brief does not establish product availability, operational readiness, or localization acceptance.

## 1. Visual hierarchy

```text
/                         Language entry → /ar/
├── /ar/                  Arabic home
│   ├── /ar/about/        About GEM
│   ├── /ar/amenities-packaging/
│   │   ├── #pilot-products       Section: five pilot concepts
│   │   ├── #concept-formats      Section: three concept formats
│   │   └── #programmes           Section: two programmes being defined
│   ├── /ar/contact/      Discuss your project
│   └── /ar/privacy/      Privacy — footer navigation
└── /en/                  English home
    ├── /en/about/        About GEM
    ├── /en/amenities-packaging/
    │   ├── #pilot-products
    │   ├── #concept-formats
    │   └── #programmes
    ├── /en/contact/      Discuss your project
    └── /en/privacy/      Privacy — footer navigation
```

**Primary navigation:** Amenities & Packaging · About GEM · Discuss your project. The logo links to the current language’s home page. Use one prominent project-enquiry action; other contextual links lead to it.

**Footer:** Contact · Privacy · language switch. Final Arabic navigation labels require native review; English labels here identify page purposes, not approved Arabic copy.

There are **five pages per language**, ten indexable pages in total. The root is a redirect, not an additional page. Fragment links are sections, not separate indexable pages or sitemap entries.

## 2. Page planning

Keyword themes below are hypotheses based on the approved business brief, not measured demand or validated rankings. Arabic keyword research and terminology review are still required.

| Page | URL pair | Parent | Purpose and audience | Search intent / provisional theme | Primary action | Priority |
|---|---|---|---|---|---|---|
| Home | `/ar/`, `/en/` | Language root | Orient owners, developers, operators and procurement; introduce GEM and its focus | Brand/navigation; GEM hospitality amenities and packaging | Discuss your project | Launch |
| About GEM | `/ar/about/`, `/en/about/` | Language home | Explain positioning, principles and relevance; support buyer evaluation | Brand evaluation; about GEM, hospitality partner | Discuss your project | Launch |
| Amenities & Packaging | `/ar/amenities-packaging/`, `/en/amenities-packaging/` | Language home | Present the pilot portfolio and development directions to procurement, operations and brand/design teams | Commercial investigation; guest amenities, hospitality packaging, hotel toiletries concepts | Discuss your project | Launch |
| Discuss your project | `/ar/contact/`, `/en/contact/` | Language home | Let qualified business visitors describe a property or project | Action/navigation; contact GEM, amenities project enquiry | Submit project enquiry, only with verified submission; otherwise use a truthful contact action | Launch |
| Privacy | `/ar/privacy/`, `/en/privacy/` | Language home | Explain actual handling of visitor and enquiry information | Trust/navigation; GEM privacy | Return to project enquiry | Launch |

**Portfolio section scope:**

- **Pilot products:** Shampoo, Conditioner, Body Wash, Body Lotion, Hand Wash. Disclose development/concept status. Names do not prove formulas, sizes, stock, or availability.
- **Concept formats:** Room set, Wall-mounted set, Travel set. Keep “Concept · supplier proof required” alongside the presentation; contents and capacities remain unapproved.
- **Programmes:** Property Edition and Bespoke Programme. Keep “Being defined; scope and availability pending.” Do not create purchasable tiers.

These topics share one portfolio page at launch because they support one buyer decision and lack verified detail for useful standalone pages. Give each topic a clear section heading and direct fragment link. Split a topic into its own page only when distinct visitor needs and substantive approved information justify it.

## 3. Page metadata requirements

These are briefs and patterns, not finished metadata or page copy. Localize each field naturally and verify how it displays; do not translate keyword strings mechanically.

| Page | Title-tag requirement | Meta-description requirement | H1 requirement | Structured-data eligibility |
|---|---|---|---|---|
| Home | Brand + primary business focus | Identify GEM, intended business audience and amenities/packaging focus without availability or supply-coverage claims | One clear statement of GEM’s business focus | `Organization` if verified public identity/contact data exist; `WebSite` for the actual site |
| About GEM | About topic + GEM | Summarize positioning and approach using documented facts | About GEM topic | `AboutPage`; reference the same Organization identity |
| Amenities & Packaging | Category topic + GEM | Explain the portfolio and explicitly qualify concept/development status | Amenities & Packaging topic | `CollectionPage`; defer `Product`/`Offer` markup for concept entries and unverified commerce data |
| Contact | Project discussion/contact topic + GEM | Explain the real contact action; include no unverified response-time promise | Invitation to discuss a project | `ContactPage`; include contact details only once verified |
| Privacy | Privacy topic + GEM | Describe the scope of the actual privacy notice | Privacy notice topic | Basic `WebPage`; no special rich-result expectation |

For all ten pages:

- **Canonical:** absolute HTTPS URL on the confirmed production domain, self-referencing and language-specific. Arabic and English pages must not canonicalize to each other.
- **Indexability:** `index,follow` at public launch once content and language checks pass. Keep staging protected and non-indexable; remove launch-blocking directives before publication. Do not use `robots.txt` as access control.
- **Social metadata:** localized `og:title`, `og:description`, `og:url`, `og:site_name`, appropriate `og:type`, and image plus alt text; provide corresponding sharing-card fields. Use an approved brand image. Product visuals must not imply verified goods or availability.
- **Heading and description quality:** one descriptive main H1, unique title and description per page and language, and no fabricated Saudi distribution, certification, sustainability, manufacturing, stock, or client claims.
- **Domain placeholder:** use `{production-domain}` in specifications until the actual canonical domain is confirmed. No domain or published-state claim is established here.

Structured data must match visible, verified content. It does not guarantee enhanced search presentation. Do not add ratings, client relationships, prices, availability, or a physical business address without evidence.

## 4. Bilingual URL and language behavior

Use explicit `/ar/` and `/en/` prefixes, with the same ASCII descriptive slugs beneath each. This keeps language pairs predictable; Arabic page titles, headings and content remain native Arabic. Approval of ASCII slugs is a URL-planning recommendation, not a limit on Arabic content.

- `/` redirects to `/ar/` because Arabic is the approved default. Do not silently override a visitor’s explicit language choice using location or browser language.
- Each language switch leads to the equivalent page, not always to the home page. Preserve a fragment only where an equivalent section exists.
- Each paired page declares reciprocal absolute `hreflang="ar"` and `hreflang="en"` links and a self entry. Use generic language codes because the audience extends beyond one country and no separate country editions are planned.
- Set `x-default` to the equivalent Arabic page for this Arabic-default site. Revisit that choice if a neutral language selector is introduced.
- Use `<html lang="ar" dir="rtl">` and `<html lang="en" dir="ltr">`. Isolate technical identifiers, URLs, emails, and English product names where needed to preserve reading order.
- Confirm Arabic terminology and native composition. No corrupt glyphs or unvalidated font substitutions are acceptable. Keep the English signature unchanged until an Arabic signature is approved.
- Do not expose incomplete language counterparts as finished pages. The approved simultaneous launch depends on equivalent information, native review, and functioning navigation in both languages.

## 5. Internal links and XML sitemap requirements

Home links to the portfolio and About GEM; both lead naturally to the project-enquiry page. Portfolio sections link directly to the enquiry path so a visitor can identify a product, format or programme of interest. Contact links to Privacy beside the data-collection action. Every page retains navigation to its language home and its language counterpart.

The eventual XML sitemap should contain the ten canonical, indexable page URLs and their reciprocal language alternates. Exclude redirects, fragments, form-result URLs and non-public material. Populate `lastmod` only from meaningful content changes. Search-engine submission and production verification are implementation tasks, not performed by this plan.

This fresh plan makes no migration assumptions. If an existing public site must later be replaced, inventory its actual live URLs before preparing a redirect map; do not derive that map from previous drafts.

## 6. Launch essentials and later expansion

| Scope | Decision and rationale | Dependency |
|---|---|---|
| Five page types in both languages | Launch essentials: establish identity, explain the focus, show qualified concepts, enable contact and disclose information handling | Approved content, Arabic acceptance and a real contact route |
| Product detail pages | Later, when each product has distinct, useful information | Verified SKU data, imagery rights and applicable claim approvals |
| Programme detail pages | Later, when Property Edition or Bespoke Programme has a defined buyer proposition | Approved scope, process and availability |
| Project examples | Later, to provide credible evidence | Real work, permission and verified descriptions |
| Downloads | Later, if useful for buyer evaluation | Public-use approval, current files and suitable language/accessibility checks |
| Insights/resources | Optional; add only with a useful editorial purpose | Validated audience questions and an owner able to maintain it |

No cart, checkout, booking engine, separate market pages, internal reference library, or invented product families are included in the launch scope.

## 7. Decisions still needed before implementation

The information architecture can be reviewed now. Implementation still needs the production domain, public business/contact details, the receiving enquiry process, actual information-handling practices for the privacy notice, approved imagery, native Arabic terminology and font validation, and any evidence supporting commercial claims.

These dependencies do not change the approved direction. They prevent the plan from treating concepts, translations or operational promises as verified facts. No website content, code, repository changes or deployment was produced.
