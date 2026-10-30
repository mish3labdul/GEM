# GEM asset alternatives — 28 October 2026

These alternatives are for owner review only and are not integrated into the website. Existing canonical images remain unchanged.

## English website mockup

- Current source: `website/assets-hub/assets/website-mockup-en.webp` (2560×1440), with an incorrect `GEA` mark on the standing card.
- Review candidate: `website/records/visual-replacements-20261028/candidates/website-mockup-en-alternative.webp` (2560×1440; SHA-256 `982f6a57a794e754c848c80de6f2f85da026296e2f229c3996a943640c33002a`).
- Method: the card lettering was removed in a localized image edit; the supplied `website/remake/assets/static/logo-ink.svg` lockup was composited onto the card. The rest of the original mockup and its interface text were preserved.

## Social preview

- Current source: `website/remake/assets/static/social.png` (1200×630), the owner-approved V03 crop derived from the previous social image.
- The owner did not approve the first alternative, `candidates/social-preview-alternative.png`, because it did not brand the products.
- The owner also rejected `candidates/social-preview-products-branded.png` because its product shapes, colors, and labels did not match GEM's product assets.
- Current review candidate: `website/records/visual-replacements-20261028/candidates/social-preview-asset-matched.png` (1200×630; SHA-256 `160cd5475cb7d9b4bc71656a165b4d9223f3d47af3af00a77e099f5fcfd57fe5`).
- Method: a new warm limestone vanity background was generated without products. The five product cutouts were taken directly from `website/remake/assets/source/`: `shampoo-source.png`, `conditioner-source.png`, `body-wash-source.png`, `body-lotion-source.png`, and `hand-wash-source.png`. Their source silhouettes, colors, GEM marks, English and Arabic labels are retained; only scale and placement changed. No product copy was added.
- The owner rejected this version because the products lacked realistic depth. A follow-up visual inspection also found a visible halo/pattern around the composited group.
- New review candidate: `website/records/visual-replacements-20261028/candidates/social-preview-depth-refined.png` (1200×630; SHA-256 `36ce0e0c850aefb38fc796616fbad5a06317e55fbaa0ac778a5b7930268ed348`). It is a landscape crop of the existing `website/remake/assets/source/format-room-source.png`, preserving its five GEM-branded products, natural cast shadows, tray occlusion, towel, and limestone vanity. This uses an already-rendered GEM scene rather than newly compositing isolated product cutouts.
- The owner then rejected that version because the product silhouettes still looked unrealistic and requested a crop from previously approved assets.
- V03 crop candidate: `website/records/visual-replacements-20261028/candidates/social-preview-approved-v03-crop.png` (1200×630; SHA-256 `3f2fd71aa9780ecc8f1e20be1a283142deba9a09b5765de0f48bf3b6ba007a18`). It is cropped directly from the previously approved `website/remake/assets/static/social.png` to enlarge the five-product scene and remove the footer. The approved source's product shapes and labels are unchanged.
- V09 crop candidate: `website/records/visual-replacements-20261028/candidates/social-preview-approved-v09-crop.png` (1200×630; SHA-256 `97a280ef124dba91f64e64a85c0fc9d66170d2962dfa985fc701b020253d8333`). It is cropped directly from the previously approved `website/remake/assets/source/format-wall-source.png`, showing the single GEM body-wash bottle with its approved silhouette, label, and natural wall shadow.
- The owner approved the V03 crop (“V03 sounds good”). It now replaces `website/remake/assets/static/social.png`; the generated `website/remake/dist/assets/social.png` copy was synchronized. The previous canonical image is preserved in `originals/social-before-v03-crop.png`.
- The V09 crop remains a review candidate and has not been integrated.

Visual review candidates do not establish product specifications, image rights, or release approval.
