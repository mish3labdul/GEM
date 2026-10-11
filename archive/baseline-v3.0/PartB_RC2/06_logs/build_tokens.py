"""Builds the Part B RC2 token package strictly from values documented in the approved
specification (deck slides 3, 6, 7, 8, 10, 12, 14, 17, 21; PDF pp.7–12, 17, 22, 28, 41).
No value is invented; each token carries status and the register decision it traces to."""
import json, pathlib, re

OUT = pathlib.Path(__file__).resolve().parents[1] / "02_build" / "tokens"
OUT.mkdir(parents=True, exist_ok=True)
A = "APPROVED"; C = "CONDITIONAL"; P = "PENDING VALIDATION"

def tok(value, type_, status, decision, desc=""):
    d = {"$value": value, "$type": type_, "status": status, "decision": decision}
    if desc: d["description"] = desc
    return d

T = {
 "$schema": "https://design-tokens.github.io/community-group/format/",
 "meta": {"name": "GEM Digital Design System tokens", "version": "3.0.0-rc.2", "edition": "V3.0 RC2", "documentId": "GEM-DDS-V3.0-RC2",
          "issued": "2026-10-06", "derivedFrom": "GEM Digital Design System V3.0 — Part B — RC2 (deck) and the V3.0 review specification",
          "note": "Derived token package. tokens.json as the DS03 living source and the component bundle do not exist in the workspace; VAL-13 and VAL-20 remain open. Every value below is stated in the approved specification; none is invented.",
          "status": "WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING)"},
 "foundation": {"color": {
    "ink": tok("#12171D", "color", A, "J01", "Principal dark field and default text"),
    "beige": tok("#BCACA7", "color", A, "J02", "Signature tone, selected fill, hairlines"),
    "black": tok("#020202", "color", A, "J03", "Monochrome, hover and pressed fill"),
    "white": tok("#FFFFFF", "color", A, "J04", "Canvas")}},
 "semantic": {
  "surface": {"canvas": tok("{foundation.color.white}", "color", A, "Q03"), "signature": tok("{foundation.color.ink}", "color", A, "Q03"),
              "selected": tok("{foundation.color.beige}", "color", A, "Q03"), "disabled": tok("{foundation.color.white}", "color", A, "Q03"),
              "scrim": tok("rgba(18, 23, 29, 0.64)", "color", A, "Q03", "INK at 64%, modal scrim; the only permitted elevation device")},
  "text": {"primary": tok("{foundation.color.ink}", "color", A, "Q03"), "inverse": tok("{foundation.color.white}", "color", A, "Q03"),
           "signatureAccent": tok("{foundation.color.beige}", "color", A, "K01", "On INK only; never essential text on WHITE (K05)")},
  "border": {"essential": tok("{foundation.color.ink}", "color", A, "Q03"), "decorative": tok("{foundation.color.beige}", "color", A, "K07"),
             "focus": tok("{foundation.color.ink}", "color", A, "Q08"), "error": tok("{foundation.color.ink}", "color", A, "Q09", "2px"),
             "disabled": tok("{foundation.color.beige}", "color", A, "Q03")},
  "action": {"background": tok("{foundation.color.ink}", "color", A, "Q11"), "foreground": tok("{foundation.color.white}", "color", A, "Q11"),
             "hoverBackground": tok("{foundation.color.black}", "color", A, "Q11"), "pressedBackground": tok("{foundation.color.black}", "color", A, "Q11"),
             "disabledBackground": tok("{foundation.color.white}", "color", A, "Q11"), "disabledText": tok("{foundation.color.ink}", "color", A, "Q11", "aria-disabled with reason in text")},
  "focus": {"ringLight": tok("{foundation.color.ink}", "color", A, "Q08"), "ringDark": tok("{foundation.color.white}", "color", A, "Q08"),
            "ringWidth": tok("2px", "dimension", A, "V08"), "ringOffset": tok("2px", "dimension", A, "V08")},
  "feedback": {"errorText": tok("{foundation.color.ink}", "color", A, "Q10", "No functional colours; state label + border weight + text"),
               "successText": tok("{foundation.color.ink}", "color", A, "Q10"),
               "errorBorderWidth": tok("2px", "dimension", A, "Q09"), "infoBorderWidth": tok("1px", "dimension", A, "Q10")}},
 "type": {
  "family": {"display": tok("Jost", "fontFamily", A, "L01", "Exact build to freeze (L06, VAL-19)"), "body": tok("Inter", "fontFamily", A, "L02"),
             "arabic": tok("Noto Sans Arabic", "fontFamily", P, "M02", "Interim; VAL-07"), "fallback": tok(["Arial", "system-ui", "sans-serif"], "fontFamily", A, "R13", "Email and non-embedding contexts")},
  "weight": {"regular": tok(400, "fontWeight", A, "L08"), "medium": tok(500, "fontWeight", A, "L08", "Max two weights per composition")},
  "size": {k: tok(f"{v}px", "dimension", A if k in ("tagline", "body", "caption", "label") else C, "L09" if k not in ("body",) else "L12")
           for k, v in {"displayXL": 96, "display": 64, "h1": 48, "h2": 32, "h3": 24, "tagline": 14, "eyebrow": 13, "navLabel": 14, "labelSmall": 12, "body": 16, "caption": 14, "label": 16,
                        "arabicDisplay": 56, "arabicH1": 40, "arabicH2": 30, "arabicH3": 24, "arabicBody": 18, "arabicLabel": 16, "arabicCaption": 15}.items()},
  "lineHeight": {k: tok(f"{v}px", "dimension", A, "L12") for k, v in {"displayXL": 104, "display": 72, "h1": 56, "h2": 40, "h3": 32, "tagline": 20, "eyebrow": 16, "navLabel": 20, "labelSmall": 16, "body": 26, "caption": 20, "label": 24,
                        "arabicDisplay": 76, "arabicH1": 60, "arabicH2": 46, "arabicH3": 38, "arabicBody": 32, "arabicLabel": 26, "arabicCaption": 26}.items()},
  "styleWeight": {k: tok(v, "fontWeight", A, "L08") for k, v in {"label": 500, "arabicH3": 500, "arabicLabel": 500}.items()},
  "tracking": {"displayXL": tok("0.12em", "dimension", C, "L09"), "display": tok("0.08em", "dimension", C, "L09"), "h1": tok("0.02em", "dimension", C, "L09"),
               "h2": tok("0.01em", "dimension", C, "L09"), "h3": tok("0", "dimension", C, "L09"), "tagline": tok("0.18em", "dimension", A, "L09"),
               "eyebrow": tok("0.16em", "dimension", C, "L09"), "navLabel": tok("0.08em", "dimension", C, "L09", "Editorial signature surfaces only; product UI navigation uses body/label at 0"),
               "labelSmall": tok("0.08em", "dimension", C, "L09"), "body": tok("0", "dimension", A, "L10"), "caption": tok("0", "dimension", A, "L10"),
               "label": tok("0", "dimension", A, "L10"), "arabic": tok("0", "dimension", A, "M05", "Never track Arabic")},
  "measure": {"maxReading": tok("70ch", "dimension", A, "L11", "45–75 characters")},
  "arabicLineHeightMin": tok(1.7, "number", P, "M04")},
 "space": {k: tok(f"{v}px", "dimension", A, "N13") for k, v in {"1": 4, "2": 8, "3": 12, "4": 16, "6": 24, "8": 32, "12": 48, "16": 64, "24": 96}.items()},
 "radius": {"editorial": tok("0", "dimension", A, "Q06", "Cards, panels, images, hero fields"), "control": tok("4px", "dimension", A, "Q06", "Buttons, inputs, selects, chips. No pills")},
 "size": {"target": {"min": tok("44px", "dimension", A, "V12")}, "logo": {"lockupMin": tok("120px", "dimension", A, "H10"), "symbolMin": tok("32px", "dimension", A, "H11", "Below: no-spark micro mark (H12), not supplied")},
          "glyph": {"box": tok("24px", "dimension", A, "N15"), "stroke": tok("2px", "dimension", A, "N15"), "sizes": tok([16, 20, 24, 32], "number", C, "N15")},
          "hairline": tok("1px", "dimension", A, "Q03"), "emphasisBorder": tok("2px", "dimension", A, "Q03")},
 "motion": {"duration": {"instant": tok("0ms", "duration", A, "P09", "All, under reduced motion"), "hover": tok("150ms", "duration", A, "P03"),
                         "confirmation": tok("180ms", "duration", A, "P03"), "modal": tok("200ms", "duration", A, "P03"), "reveal": tok("1500ms", "duration", A, "P02"),
                         "revealRing": tok("900ms", "duration", C, "P01", "from 0"), "revealSpark": tok("200ms", "duration", C, "P01", "from 900ms"), "revealQuarter": tok("400ms", "duration", C, "P01", "from 1100ms")},
            "easing": {"out": tok("cubic-bezier(0.22, 0.61, 0.36, 1)", "cubicBezier", A, "P03", "Only easing; reversed for exits")}},
 "layout": {"breakpoint": {"compact": tok("0px", "dimension", A, "Q17"), "mobile": tok("480px", "dimension", A, "Q17"), "tablet": tok("720px", "dimension", A, "Q17"), "desktop": tok("1024px", "dimension", A, "Q17"), "wide": tok("1440px", "dimension", A, "Q17", "Max-width enhancement, not a separate model")},
            "columns": {"compact": tok(4, "number", C, "Q17"), "mobile": tok(4, "number", C, "Q17"), "tablet": tok(8, "number", C, "Q17"), "desktop": tok(12, "number", C, "Q17"), "wide": tok(12, "number", C, "Q17")},
            "gutter": {"compact": tok("16px", "dimension", C, "Q17"), "mobile": tok("16px", "dimension", C, "Q17"), "tablet": tok("24px", "dimension", C, "Q17"), "desktop": tok("24px", "dimension", C, "Q17"), "wide": tok("24px", "dimension", C, "Q17")},
            "margin": {"compact": tok("16px", "dimension", C, "Q17"), "mobile": tok("24px", "dimension", C, "Q17"), "tablet": tok("32px", "dimension", C, "Q17"), "desktop": tok("48px", "dimension", C, "Q17"), "wide": tok("48px", "dimension", C, "Q17")},
            "maxWidth": {"desktop": tok("1080px", "dimension", C, "Q17"), "wide": tok("1280px", "dimension", C, "Q17"), "modal": tok("440px", "dimension", C, "Q17")},
            "reflowMin": tok("320px", "dimension", A, "V01", "WCAG 1.4.10")},
 "locale": {"source": tok("en", "string", A, "D03"), "arabic": tok("ar-SA", "string", P, "D04"), "numeralsTechnical": tok("latn", "string", A, "M12"),
            "numeralsGuestArabic": tok("arab", "string", C, "M11"), "calendarDefault": tok("gregory", "string", C, "DS06", "Hijri display [REQUIRES OWNER · Arabic / Localization Lead]"),
            "currencyFormat": tok("[REQUIRES OWNER]", "string", P, "DS06", "SAR symbol/code position for ar-SA and en; no price invented"),
            "textExpansion": tok("30-40%", "string", A, "DS06"), "direction": tok({"en": "ltr", "ar-SA": "rtl"}, "string", A, "M06")}
}

(OUT / "gem-tokens.v3.0-rc2.json").write_text(json.dumps(T, indent=2, ensure_ascii=False), encoding="utf-8")

# CSS custom properties (flattened, aliases resolved)
flat = {}
def walk(node, path):
    if isinstance(node, dict) and "$value" in node:
        flat[".".join(path)] = node; return
    if isinstance(node, dict):
        for k, v in node.items():
            if k.startswith("$") or k == "meta": continue
            walk(v, path + [k])
walk(T, [])
def resolve(v):
    while isinstance(v, str) and v.startswith("{") and v.endswith("}"):
        v = flat[v[1:-1]]["$value"]
    return v
lines = ["/* GEM Digital Design System tokens · 3.0.0-rc.2 · V3.0 RC2 · GEM-DDS-V3.0-RC2 · 2026-10-06",
         "   Derived from the approved specification; status per token in the JSON. WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING). */",
         ":root {"]
for k, node in flat.items():
    v = resolve(node["$value"])
    if isinstance(v, (list, dict)): v = json.dumps(v)
    name = "--gem-" + re.sub(r"[^a-z0-9]+", "-", re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", k).lower())
    lines.append(f"  {name}: {v}; /* {node['status']} · {node['decision']} */")
lines += ["}", "", "@media (prefers-reduced-motion: reduce) {", "  :root {"]
for k, node in flat.items():
    if k.startswith("motion.duration."):
        name = "--gem-" + re.sub(r"[^a-z0-9]+", "-", re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", k).lower())
        lines.append(f"    {name}: 0ms; /* V11, P09 */")
lines += ["  }", "}", "", '[dir="rtl"] { /* logical properties carry direction; no overrides needed (M06) */ }', ""]
(OUT / "gem-tokens.v3.0-rc2.css").write_text("\n".join(lines), encoding="utf-8")

# validation: parity, palette discipline
hexes = {re.sub(r"\s", "", str(resolve(n["$value"]))).upper() for n in flat.values() if n["$type"] == "color"}
hexes = {h for h in hexes if h.startswith("#")}
assert hexes <= {"#12171D", "#BCACA7", "#020202", "#FFFFFF"}, hexes
css_count = sum(1 for l in lines if l.startswith("  --gem-"))
assert css_count == len(flat), (css_count, len(flat))
(OUT / "README.md").write_text(f"""# GEM tokens · 3.0.0-rc.2 (V3.0 RC2)

**Status:** WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING). **Document:** GEM-DDS-V3.0-RC2 · 2026-10-06.

This package is **derived from the approved specification** (Part B RC2 deck slides 3, 6, 7, 8, 10, 12, 14, 17, 21 and the V3.0 review PDF). It is complete for every token group the specification defines ({len(flat)} tokens across foundation.color, semantic.surface/text/border/action/focus/feedback, type.family/weight/size/lineHeight/tracking, space, radius, size.target/logo/glyph, motion.duration/easing, layout.breakpoint/columns/gutter/margin/maxWidth, locale). No value is invented; each token carries `status` (APPROVED / CONDITIONAL / PENDING VALIDATION) and the register `decision` it traces to.

What it is **not**: the DS03 living source (`tokens.json` maintained with the component bundle) and the React/Storybook build, which do not exist in the workspace. VAL-13 (tokens and components implemented and tested) and VAL-20 remain open. Tracking values are CONDITIONAL until optical QA (VAL-19); Arabic values are PENDING VALIDATION (VAL-07); `locale.currencyFormat` and the Hijri policy are [REQUIRES OWNER].

Files: `gem-tokens.v3.0-rc2.json` (W3C design-tokens shape, `$value/$type`, aliases as `{{path}}`), `gem-tokens.v3.0-rc2.css` (`--gem-*` custom properties, aliases resolved, reduced-motion block). Checksums in `../../06_logs/release_sha256.txt`.
""", encoding="utf-8")
print(len(flat), "tokens; palette", sorted(hexes))
