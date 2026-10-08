# 06 · Token Status Implementation (Owner decision D4, with D5 annotation) — ODI01-R1

**Status: UNAPPROVED IMPLEMENTATION CANDIDATE.** The Brand Owner accepted all 26 AFC02 downward status normalizations (D4). They are applied in candidate copies only; the originals in `PartB_RC2/05_release/tokens/` are untouched.

**Rule applied:** a derived token may not carry a stronger status than its weakest governing dependency unless explicit independent approval exists. Order: APPROVED > CONDITIONAL > PENDING VALIDATION. **Nothing is promoted. No value, name, type, decision ID or semantic meaning is changed.**

## Result

- Tokens re-run: **153**; normalized: **26** (10 APPROVED→CONDITIONAL, 9 APPROVED→PENDING VALIDATION, 7 CONDITIONAL→PENDING VALIDATION); unchanged: 127.
- "Value changed?" = **NO for all 153 rows**.
- Unexplained status inflation after normalization: **0**.
- D5 annotation: the four weight-500 tokens (`type.weight.medium`, `type.styleWeight.label`, `type.styleWeight.arabicH3`, `type.styleWeight.arabicLabel`) carry the added description / CSS comment "500 WEIGHT PENDING ACCEPTED FONT FILE — use 400 until accepted". No token was added.

## Verification run (script `17_scripts/token_status_implementation.py`)

| Verification | Result |
|---|---|
| Value parity (value+type+name set, 153 tokens) | PASS |
| Decision IDs unchanged | PASS |
| Only status/description changed (no other key touched) | PASS |
| Description changed only on the 4 weight-500 tokens | PASS |
| No promotion (every status ≤ original) | PASS |
| 26 normalizations applied | PASS |
| CSS declarations identical (name+value) | PASS |
| JSON↔CSS status parity (153 tokens with a CSS status comment; 0 without) | PASS |
| CSS status comments updated = 26 | PASS |
| D5 CSS annotations on 4 weight-500 tokens | PASS |
| Dependency hierarchy: unexplained inflation (candidate) | PASS — 0 |
| Arabic hierarchy tokens not stronger than PENDING VALIDATION (16 tokens) | PASS |
| Non-Arabic lineHeight ≤ paired size status | PASS |
| Non-Arabic CONDITIONAL size → lineHeight ≤ CONDITIONAL | PASS |
| Part B slide 21 locale table ↔ candidate tokens (value+status, 5 rows) | PASS |
| Part B slides 10/12 typography tables: carry no status column → size/line/weight/tracking values re-verified by audit_tokens.py | SEE audit_tokens.py (run separately) |

Part B slides 10 and 12 (type tables) have no status column; their size / line / weight / tracking values were re-verified against the **unchanged** token values by `17_scripts/audit_tokens.py` (65 PASS · 0 FAIL · 12 INFO, `18_qa_evidence/audit_tokens_original.json`). Because the candidate values are byte-identical in value and type to the original, the same result holds for the candidate.

## The 26 normalizations

| Token | Original | Dependency (weakest) | New |
|---|---|---|---|
| `type.weight.medium` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.size.arabicDisplay` | CONDITIONAL | PENDING VALIDATION | PENDING VALIDATION |
| `type.size.arabicH1` | CONDITIONAL | PENDING VALIDATION | PENDING VALIDATION |
| `type.size.arabicH2` | CONDITIONAL | PENDING VALIDATION | PENDING VALIDATION |
| `type.size.arabicH3` | CONDITIONAL | PENDING VALIDATION | PENDING VALIDATION |
| `type.size.arabicBody` | CONDITIONAL | PENDING VALIDATION | PENDING VALIDATION |
| `type.size.arabicLabel` | CONDITIONAL | PENDING VALIDATION | PENDING VALIDATION |
| `type.size.arabicCaption` | CONDITIONAL | PENDING VALIDATION | PENDING VALIDATION |
| `type.lineHeight.displayXL` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.lineHeight.display` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.lineHeight.h1` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.lineHeight.h2` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.lineHeight.h3` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.lineHeight.eyebrow` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.lineHeight.navLabel` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.lineHeight.labelSmall` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.lineHeight.arabicDisplay` | APPROVED | PENDING VALIDATION | PENDING VALIDATION |
| `type.lineHeight.arabicH1` | APPROVED | PENDING VALIDATION | PENDING VALIDATION |
| `type.lineHeight.arabicH2` | APPROVED | PENDING VALIDATION | PENDING VALIDATION |
| `type.lineHeight.arabicH3` | APPROVED | PENDING VALIDATION | PENDING VALIDATION |
| `type.lineHeight.arabicBody` | APPROVED | PENDING VALIDATION | PENDING VALIDATION |
| `type.lineHeight.arabicLabel` | APPROVED | PENDING VALIDATION | PENDING VALIDATION |
| `type.lineHeight.arabicCaption` | APPROVED | PENDING VALIDATION | PENDING VALIDATION |
| `type.styleWeight.label` | APPROVED | CONDITIONAL | CONDITIONAL |
| `type.styleWeight.arabicH3` | APPROVED | PENDING VALIDATION | PENDING VALIDATION |
| `type.styleWeight.arabicLabel` | APPROVED | PENDING VALIDATION | PENDING VALIDATION |

## Not changed (by design)
- `type.family.display` / `type.family.body` stay APPROVED (families L01/L02 are approved decisions; exact-build freeze is tracked in the font matrix).
- `type.tracking.arabic` stays APPROVED ("never track Arabic", M05, is independent of the interim family).
- Tokens with no dependency edge keep their status; this pass did not re-judge them.

## Files
- `06_Token_Status_Implementation.csv` — all 153 rows with columns Token, Original status, Dependency, Weakest dependency status, New status, Value changed?, Authority, QA result.
- `19_candidate_documents/tokens/gem-tokens.v3.0-rc2.ODI01-R1-candidate.json` and `.css`; `token_verification.json`.

Release effect: none. AC20 remains OPEN; token package remains "WORKING SPECIFICATION · NOT RELEASED".

## R1 change (D5 wording only)
The four weight-500 tokens (`type.weight.medium`, `type.styleWeight.label`, `type.styleWeight.arabicH3`, `type.styleWeight.arabicLabel`) kept value **500** and their D4 statuses. Only the description / CSS comment changed, from "500 WEIGHT PENDING ACCEPTED FONT FILE — use 400 until accepted" to:

> FUTURE DESIGN INTENT = 500 · CURRENT IMPLEMENTATION = 400 · 500 WEIGHT PENDING ACCEPTED FONT FILE (D5; Y03, VAL-05, VAL-19)

This is approach A of the brief (description/status clarification only). The governing future design is not rewritten and no separate current-implementation mapping was introduced. No token, template or deck instruction in the candidate set requires a 500 file. R1 re-run: 153/153 name, type and value identical to the originals; 26 downward status changes retained (10 APPROVED→CONDITIONAL, 9 APPROVED→PENDING VALIDATION, 7 CONDITIONAL→PENDING VALIDATION); 0 promotions; 0 unexplained status inflation; all verifications PASS (`19_candidate_documents/tokens/token_verification.json`).
