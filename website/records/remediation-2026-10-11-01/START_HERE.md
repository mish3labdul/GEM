# Confirmed audit corrections — 11 October 2026

Implemented locally under the user's instruction to apply confirmed CLAUDE_HANDOFF corrections. No deployment, form connection, mailto follow or real enquiry occurred. Website remains a proposed preview based on v0.5.1; this is not owner acceptance or a public release.

## Implemented

| Finding | Change | Status |
|---|---|---|
| G26-02 | Privacy describes both draft types and the external email application's privacy/sync boundary. Absolute device and unverified downstream-use assurances removed. | Confirmed correction implemented; final operator/legal notice still pending. |
| G26-03 | Disabled/failed form notices say drafting is unavailable, account for initialization failure, and identify placeholder contacts without directing visitors to them. | Failure-guidance correction implemented; verified identity/contact decision remains pending. |
| G26-06 | Hint and error state the existing 1–100,000 whole-number range. No constraint or commercial limit changed. | Implemented; owner rationale for the existing ceiling remains pending. |
| G26-04 | Added explicit brand-font/glyph validation with blocked-font and unsupported-Arabic negative checks. Current required faces/glyphs pass; missing support returns FAIL. | QA correction implemented. Runtime fallback remains readable; no preview diagnostic UI or font substitution added. |
| G26-05 | Semantic `em` uses accepted regular styling; font synthesis disabled. | Implemented; no italic font added. |
| G26-09 | Email handoff describes the full-copy fallback; long output/copy is preserved and tested. | Partially addressed. No untested URI threshold invented; native client compatibility and threshold proposal remain pending. |
| G26-10 | Two served Finder metadata files removed, preserved in `before/`; public-root denial probes added. | Implemented; both URLs return 404 on tested site-only root. |

Fresh QA: **484/484 regression assertions** and **76/76 targeted correction assertions** pass in Chromium 143.0.7499.4. The earlier 482 checks are retained with updated expected room wording, plus two metadata probes. Both forms remain fail closed; no backend added; stale drafts/copy/reset, menu/focus, responsive assets and concept labels remain verified.

Read [CHANGELOG.md](CHANGELOG.md), [VERIFICATION.md](VERIFICATION.md), [CODE_REVIEW.md](CODE_REVIEW.md) and [PENDING_DECISIONS.md](PENDING_DECISIONS.md). [INTEGRITY.md](INTEGRITY.md) records final hashes and change attribution. `CHANGES.diff` and `before/` preserve the reviewable changes; previous audits/records/creative packages remain historical and unchanged.

## Pending

G26-01 package readiness/quotation copy; G26-03 verified entity/address/phone/contact placement; G26-07 colorway/collection/artwork acceptance; G26-08 native human/other-engine acceptance; G26-09 email-client envelope/threshold. Part D stays concept, logo kit stays working, legal/IP deferral is not clearance, no WCAG certification is claimed, and legacy B01/B02 dispositions remain intact. No images, logo masters, fonts, owner decision records or accepted package names were changed.
