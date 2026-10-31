# Regenerated room, travel, lobby and turndown images — 31 October 2026

**Status: CANDIDATES, awaiting owner approval. No shipped asset has been replaced.** Visual approval only; rights (L08) stay open for these outputs.

Owner decision (31 Oct 2026, in session): regenerate all four images that differ from the Part D slide 4 rule ("Regenerate all to the slide 4 rule - yes"). The rule: Shampoo, Conditioner and Body Wash dark smoked-amber, Body Lotion and Hand Wash cream, all five with matte black pumps (released Part D V3.0, slide 4).

## How they were made
Gemini web app (gemini.google.com), owner's Google account, Create image, model picker "3.1 Pro", 16:9, 31 Oct 2026; the owner has confirmed the model as Gemini 3.1. The five canonical `website/remake/assets/source/*-source.png` product images were attached as references. Raw outputs (2752×1536 JPEG, unedited) are in `generated/`; candidates are crops and exports made with Pillow, cwebp and sharp (quality 86).

## Checked by eye against the slide 4 rule
| Candidate | Replaces | Result |
|---|---|---|
| `format-room-candidate.png` (1536×1024) plus 480/960 webp | `source/format-room-source.png`, `exports/format-room-*.webp` | Order Shampoo, Conditioner, Body Wash, Body Lotion, Hand Wash; three dark, two cream; pumps; labels read correctly; card wordmark visible (the towel slightly overlaps the card's arc). The old image showed a cream Conditioner and a dark Hand Wash (as Part D slide 20 does). |
| `format-travel-candidate.png` (1536×1024) plus 480/960 webp | `source/format-travel-source.png`, `exports/format-travel-*.webp` | Travel-size bottles in a gift box: three dark, two cream, with pumps; lid shows GEM wordmark, arc and "Amenities Collection". **This departs from Part D slide 13**, which shows five cream bottles with black caps; the owner chose the slide 4 rule. |
| `lobby-candidate.webp` (1600×893) | `scenes/lobby.webp` | Single cream Hand Wash with pump on a brass tray, carved geometric wall, lattice shadows. The old image showed a dark Hand Wash. |
| `turndown-candidate.webp` (1400×781) | `scenes/turndown.webp` | Dark Body Wash and cream Body Lotion, ivory card, linen napkin. The old image showed both bottles amber. |

Colour judged by eye, not measured.

## Integration notes (after approval)
- Replace the sources and scene files, regenerate the 480/960 exports (sharp, quality 86), update `assets/manifest.json` and `scene-manifest.json`, rebuild `dist`, refresh manifests from a clean tree, run the validator and both browser suites.
- **Update the alt text** in `refined-layouts.mjs`: the turndown alt says "Two GEM amber pump bottles" (now one amber, one cream) and the lobby alt says "GEM amber hand wash pump bottle" (now cream), in English and Arabic.
- The travel image now differs from Part D slide 13; the Part D deck itself is not changed.

## SHA-256 of candidates
| File | SHA-256 |
|---|---|
| `format-room-candidate.png` | `43c6bb04661a25bb83e5679bc88f1275af3a913f61d354b86a0f58bdd5d748ec` |
| `format-travel-candidate.png` | `f292928cb6bcd9a6dc3544b6b5e398191924fb43fe2d0744c50770788307c43e` |
| `lobby-candidate.png` | `f12ccbc96bda77e26021481fdd353a90db0ae3ca44823e09ea0d0106b917f817` |
| `turndown-candidate.png` | `1b6b73b8d58026aece9edc562ff86fe9b0eb69e6a69f830fbd62c26170779bf1` |
| `format-room-candidate-480.webp` | `6e2b757c1f48f9c7495d3c0aee70f3050a60c35a510d5d1dd8cf9832596a90ee` |
| `format-room-candidate-960.webp` | `b0f8bee6ac1799e1f7242fd7abe108c510b725a2e5696ea17d9be04306c4d3ef` |
| `format-travel-candidate-480.webp` | `a708122a04ca8938fd306c1c3329d4913b4233562bba602bb1c1ff50a90b8f37` |
| `format-travel-candidate-960.webp` | `0248d52ab301d4b591cd047fa86e3569928fc28029e22190c08327afc772f8f8` |
| `lobby-candidate.webp` | `6bbfcf5760b01393819f163a8426ed09b79f9c7a7bf612e99c9104e30107fe1d` |
| `turndown-candidate.webp` | `1d8d33b5a079a90ba6ca48fe2b41d1f3cb4f28cdd57521f9b70a03801d7bb4c1` |
