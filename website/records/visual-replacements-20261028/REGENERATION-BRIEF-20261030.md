# Regeneration brief — brand-aligned replacements — 30 October 2026

Owner decision (30 Oct 2026, in session): regenerate the images that differ from canonical Part D product art. Not yet run. Generation uses the owner's own tool and account (Nano Banana Pro / Gemini EDIT, as in `NanoBanana-EDIT-Package` in the vault); provenance and terms stay the owner's, and the rights gate (L08) stays open for any new output.

## Canonical references (attach to every run)
Under `website/remake/assets/source/`: `shampoo-source.png`, `conditioner-source.png`, `body-wash-source.png`, `body-lotion-source.png`, `hand-wash-source.png`.
What they show (viewed 30 Oct 2026):
- Shampoo, Conditioner, Body Wash, Hand Wash: dark smoked-amber glass, matte black pump, matte charcoal label, GEM™ wordmark, short rule, product name (English, then Arabic), white arc with tick marks.
- Body Lotion: **cream/ivory** bottle, matte black pump, black label art.
- The Conditioner has a **pump**.
Palette: Ink `#12171D`, Beige `#BCACA7`, White; package tokens add Ivory `#F8F3EA` and Sand `#EFE6D8`.

## Acceptance checklist (apply to every output)
1. Five products in the order Shampoo, Conditioner, Body Wash, Body Lotion, Hand Wash (mirrored order for RTL; Arabic text is **not** mirrored).
2. All five have a pump. Body Lotion and Hand Wash are cream; Shampoo, Conditioner and Body Wash are dark smoked amber, not orange-amber.
3. Labels read GEM™, a short rule, product name, Arabic name, arc, exactly as in the references; no changed text.
4. No wordmark is cropped or hidden by another object.
5. Background tones sit within Sand/Ivory/Beige, not saturated tan or orange.
6. No extra objects, no people, no watermark.

## Prompts (replace the reference-pixels-unchanged wording; build a new scene)

**V02 LTR and RTL family plate, 2816×1280.** "Create a photographic wide plate, 2816 × 1280 px (2.2:1), of five GEM bottles on a honed travertine shelf against a warm limewash wall (#EFE6D8, #BCACA7) with soft diffused leaf-shadow light. Use the five attached product images as exact references for shape, colour, label and pump. Order left to right: Shampoo, Conditioner, Body Wash, Body Lotion, Hand Wash. All five have a pump. Body Lotion and Hand Wash are cream bottles; Shampoo, Conditioner and Body Wash are dark smoked-amber glass. Labels unchanged. Bottles occupy about 42% to 92% of the width, left 38% calm empty wall and shelf. No text beyond the labels, no logos, no people, no watermark." For RTL: reverse the bottle order (Hand Wash first), place bottles at about 8% to 58%, keep the right 38% empty, do not mirror the label text.

**V03 social share, 1200×630.** "Create a 1200 × 630 px (1.91:1) photograph of a stone tray with the five GEM bottles (references attached; Conditioner dark amber with pump, Body Lotion cream, others dark amber), one folded white towel and one standing GEM card, fully visible, on a travertine counter against a travertine wall with soft diagonal sunlight (#EFE6D8, #F8F3EA). Keep the central 630 × 538 px safe area. Keep the bottom 92 px plain counter." Then apply the GEM horizontal logo lockup band in the bottom 92 px as in the previous share image (`originals/social-before-v03-crop.png`), using `static/logo-ink.svg`.

**V09 wall-format, 1536×1024.** "Use the attached Body Wash reference. Photographic wall-mounted dispenser on pale travertine tiles in **desaturated ivory-beige (#EFE6D8, #BCACA7)**, not orange or tan, warm side light from the right, full pump head, full amber base, label arc complete, minimalist matte black wall bracket visible, 10% clear margin above and below. No text beyond the label, no plumbing, no hands."

## After generation
Save the approved PNGs under `approved-png/` with SHA-256, keep the replaced files under `originals/`, then run `node website/remake/build.mjs`, `python3 tools/refresh_manifests.py` (from a clean checkout) and the validator, and add the approval record. The owner reviews each image against the checklist above.
