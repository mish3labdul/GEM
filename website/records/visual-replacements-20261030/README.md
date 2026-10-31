# Regenerated brand-aligned candidates — 30 October 2026

**Status: OWNER-APPROVED 30 Oct 2026 and integrated** (see `APPROVAL-20261030.md`). Supersedes the 28 Oct replacements for V02, V03 and V09. Visual approval only; rights (L08) stay open for these new outputs.

## How they were made
- Tool: Gemini web app (gemini.google.com), signed in as the owner's Google account, **Create image** mode, model picker set to **3.1 Pro**, aspect ratio 16:9, 30 Oct 2026. The picker shows no model named "Nano Banana Pro". **The owner confirmed on 31 Oct 2026 that the model was Gemini 3.1** (owner-reported; the app's own picker label was "3.1 Pro"). The exact image-model build is still not shown by the app.
- References attached: the five canonical `website/remake/assets/source/*-source.png` product images (viewed: Shampoo, Conditioner, Body Wash dark smoked amber; Body Lotion and Hand Wash cream; all with pumps).
- Prompts: as in `../visual-replacements-20261028/REGENERATION-BRIEF-20261030.md` (corrected), run as follow-ups in one chat.
- Raw outputs (2752×1536 JPEG, unedited) are in `generated/`. Candidates in `candidates/` are crops and a composited lockup made with Pillow and Chromium.

## Checked by eye against the brief's checklist
| Candidate | Result |
|---|---|
| `family-candidate` (V02 LTR, 2172×724) | **Second, pulled-back generation** (`generated/v02-family-ltr-v2-pulledback-gemini-raw.jpeg`, downloaded by the owner from the Gemini chat). Order, colours, pumps, labels and Arabic names correct; bottles about 38% to 79% of the height with clear wall above and a visible shelf; left 40% empty. The first generation (`v02-family-ltr-gemini-raw.jpeg`) is kept but its bottles filled about 85% of the crop. |
| `family-rtl-candidate` (V02 RTL, 2172×724) | **Second, pulled-back generation** (`generated/v02-family-rtl-v2-pulledback-gemini-raw.jpeg`). Reversed order, labels not mirrored, correct colours and pumps, bottles about 39% to 80% of the height, right 40% empty, light from the right. The first RTL generation is kept in `generated/` but its framing was too tight. |
| `social-candidate` (V03, 1200×630) | Five bottles correct, one fully visible card, no clipped wordmark, GEM logo lockup band restored in the bottom 92 px (ivory `#F8F3EA`, `static/logo-ink.svg`). |
| `format-wall-candidate` (V09, 1536×1024) | Body Wash correct, bracket and full pump visible, wall now a pale desaturated ivory travertine. 480/960 WebP exports not yet made. |
| `tx-arches` | Unchanged; no brand conflict. |

Limits: colour was judged visually, not measured. Wall and shelf tones sit within the Sand/Ivory/Beige range by eye.

## SHA-256 of candidates
| File | SHA-256 |
|---|---|
| `family-candidate.png` | `ada65a4db32a7e9d622408c9ee51120bd291740409658a9a745a385f3a99355a` |
| `family-candidate.webp` | `fd7f49e17b313fb65168901189f82fca96a560d6f2687a856d63c8a1e6b5dd6d` |
| `family-rtl-candidate.png` | `d34f28727908a1ba1e4d4afe98257c099efff8739333b425d82991310eb7ba3d` |
| `family-rtl-candidate.webp` | `7c55185486b1bdc96ce13f4dda299dce06d5165505b52dc79e81ce53df072d18` |
| `format-wall-candidate.png` | `817d49c72564047b1bfa0c8fb8083a49dcae825a4c70648f67ed952ad769316e` |
| `social-candidate.png` | `57a5affe07758ef6560bdfb7d0dd08e3d9a753e1700a54e8dd306c81acd3c759` |

## To ship (after approval)
Copy the approved candidates over `website/remake/assets/{scenes,static,source}`, run `node website/remake/build.mjs` and the 480/960 exports, `tools/refresh_manifests.py` from a clean checkout, the validator and both browser suites, and add an approval record next to the 28 Oct ones.
