# GEM tokens · 3.0.0 (V3.0)

**Status:** OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE · TOKEN VALUES UNCHANGED FROM RC2 · COMPONENT IMPLEMENTATION NOT AUTHORIZED. **Document:** GEM-DDS-V3.0 · 2026-10-09.

This package is **derived from the approved specification** (Part B RC2 deck slides 3, 6, 7, 8, 10, 12, 14, 17, 21 and the V3.0 review PDF). It is complete for every token group the specification defines (153 tokens across foundation.color, semantic.surface/text/border/action/focus/feedback, type.family/weight/size/lineHeight/tracking, space, radius, size.target/logo/glyph, motion.duration/easing, layout.breakpoint/columns/gutter/margin/maxWidth, locale). No value is invented; each token carries `status` (APPROVED / CONDITIONAL / PENDING VALIDATION) and the register `decision` it traces to.

What it is **not**: the DS03 living source (`tokens.json` maintained with the component bundle) and the React/Storybook build, which do not exist in the workspace. VAL-13 (tokens and components implemented and tested) and VAL-20 remain open. Tracking values are CONDITIONAL until optical QA (VAL-19); Arabic values are PENDING VALIDATION (VAL-07); `locale.currencyFormat` and the Hijri policy are [REQUIRES OWNER].

Files: `gem-tokens.v3.0.json` (W3C design-tokens shape, `$value/$type`, aliases as `{path}`), `gem-tokens.v3.0.css` (`--gem-*` custom properties, aliases resolved, reduced-motion block). Checksums: see the RP01 package SHA256SUMS.txt.
