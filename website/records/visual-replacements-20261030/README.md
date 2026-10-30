# Regenerated brand-aligned candidates — 30 October 2026

**Status: CANDIDATES, awaiting owner approval. No shipped asset has been replaced.** Visual approval only; rights (L08) stay open for these new outputs.

## How they were made
- Tool: Gemini web app (gemini.google.com), signed in as the owner's Google account, **Create image** mode, model picker set to **3.1 Pro**, aspect ratio 16:9, 30 Oct 2026. The picker shows no model named "Nano Banana Pro", so which image model ran is **not established**; record this before any rights claim.
- References attached: the five canonical `website/remake/assets/source/*-source.png` product images (viewed: Shampoo, Conditioner, Body Wash dark smoked amber; Body Lotion and Hand Wash cream; all with pumps).
- Prompts: as in `../visual-replacements-20261028/REGENERATION-BRIEF-20261030.md` (corrected), run as follow-ups in one chat.
- Raw outputs (2752×1536 JPEG, unedited) are in `generated/`. Candidates in `candidates/` are crops and a composited lockup made with Pillow and Chromium.

## Checked by eye against the brief's checklist
| Candidate | Result |
|---|---|
| `family-candidate` (V02 LTR, 2172×724) | Order, colours, pumps, labels and Arabic names correct. **Framing issue:** after the 3:1 crop the bottles fill about 85% of the height with no headroom. A "pull the camera back" regeneration was started and had not returned when this was written. |
| `family-rtl-candidate` (V02 RTL, 2172×724) | Reversed order, labels not mirrored, light from the right, correct colours. Same framing issue. |
| `social-candidate` (V03, 1200×630) | Five bottles correct, one fully visible card, no clipped wordmark, GEM logo lockup band restored in the bottom 92 px (ivory `#F8F3EA`, `static/logo-ink.svg`). |
| `format-wall-candidate` (V09, 1536×1024) | Body Wash correct, bracket and full pump visible, wall now a pale desaturated ivory travertine. 480/960 WebP exports not yet made. |
| `tx-arches` | Unchanged; no brand conflict. |

Limits: colour was judged visually, not measured. Wall and shelf tones sit within the Sand/Ivory/Beige range by eye.

## SHA-256 of candidates
| File | SHA-256 |
|---|---|
| `family-candidate.png` | `97db63a0f530ada2548ab91b72ad2b88cd15f2b83a53779b4b4ed67cafee78c4` |
| `family-candidate.webp` | `36be739dfb039a8f255e7a26a2faf26d7b2b5dcf051664fc4d78d4a05c8e356e` |
| `family-rtl-candidate.png` | `d714f8f63425729b00b1a6ed74551411141a8a28a7f6efa1caa0c016d370e1f0` |
| `family-rtl-candidate.webp` | `bb1b39d1442f1674fa366d2210e6ae44da5e7e1434236e17d48a2e0021a960ea` |
| `format-wall-candidate.png` | `817d49c72564047b1bfa0c8fb8083a49dcae825a4c70648f67ed952ad769316e` |
| `social-candidate.png` | `57a5affe07758ef6560bdfb7d0dd08e3d9a753e1700a54e8dd306c81acd3c759` |

## To ship (after approval)
Copy the approved candidates over `website/remake/assets/{scenes,static,source}`, run `node website/remake/build.mjs` and the 480/960 exports, `tools/refresh_manifests.py` from a clean checkout, the validator and both browser suites, and add an approval record next to the 28 Oct ones.
