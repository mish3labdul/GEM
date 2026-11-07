# GEM™ M33–M40 + W1–W6 — Open Items & Risk Register

**Date:** 2026-11-07  
**Program:** GEM™ Autonomous Multi-Agent Packaging & Digital Experience Transformation  

| Item ID | Track | Description | Severity | Mitigation / Status | Owner Action Required |
|---|---|---|---|---|---|
| `OPEN-M34-001` | Track A (`M34`) | Physical bottle geometry, capacity (`~204 mL` overflow vs `250/300 mL`), and pump neck finish (`24/410` vs `28/410`) for all 5 products remain provisional CGI geometry (`PROVISIONAL_M27A` / `PROVISIONAL_EXPLORATORY_GEOMETRY`). | Medium | Explicitly tagged in Blender custom properties, contact sheet banners, `PRODUCT_ASSET_REGISTRY.json`, and `#studio-3d-badge` on staging website. | Dispatch `m38_coordination/SUPPLIER_INQUIRY_SAFEGUARD_PACKAGE.md` (`GEM-SUP-INQ-20261107-01..03`). |
| `OPEN-M38-001` | Track C (`M38`) | Qualified human native Arabic editorial/packaging typography sign-off on M15 `v1.0` vs unapplied M30 `v1.1` (`+8%` Arabic scale, `+10 px` inter-script gap) remains pending. | Medium | M15 `v1.0` remains locked in all 3D scenes and GLB exports; outreach package prepared and verified in `m38_coordination/`. | Dispatch `m38_coordination/QUALIFIED_ARABIC_REVIEWER_OUTREACH_PACKAGE.md` (`GEM-AR-REV-20261107-01`). |
| `OPEN-W6-001` | Track B (`W6`) | Production website (`https://gem.mish3l.com`, `main` branch) has not yet been updated with the W3–W5 transformation. | Low (By Design) | Isolated on branch `development/website-transformation-w1-w6-20261107` with `noindex,nofollow` preview guard intact. | Review staging preview and authorize merge/deployment on `OWNER_REVIEW_DECISION_SHEET.md`. |
