# Launch readiness refresh — 23 October 2026

This record supersedes [the 21 October register](../launch-readiness-2026-10-21/README.md) for current status. The earlier record stays as dated evidence; its statements that PR #21 was open and that the deployed source was `cbd46be` describe 21 October only.

**Current status: hosted noindex concept preview, owner-accepted. Not indexable.** Production serves deployment `52dd8d17` from source `2552dc8`.

## What changed since 21 October

- PR #21 and PRs #25, #26 and #27 are merged into `main` (gate L11 now Pass).
- Motion and interaction enhancements were reviewed by the owner on a preview URL and shipped (L14).
- A font-load failure mode was made recoverable (L15).
- An M8 brand-presentation audit began (L16). See the [M8 record](../m8-brand-presentation-20261023/README.md).
- The public privacy notice now has a bilingual draft with marked blanks (L09), not yet published.

Full chronology, deployment IDs, test counts and limits: [motion and font-retry record](../motion-and-font-retry-20261023/README.md). The gate register is [GATES.csv](GATES.csv).

## What is still blocking an indexable launch (M7)

Only three decisions, none of which engineering can infer:

| Gate | Input needed | From whom |
|---|---|---|
| L09 | Public operator name; privacy contact email; hosting services that log requests, who may access the logs, retention period; applicable-law and rights wording; response time | Owner and privacy decision-maker |
| L08 | Public-use rights disposition for the Flow scenes, approved arches and product artwork, and any exclusions | Rights decision-maker |
| L07 | Keep the current favicon, or choose the micro-favicon artwork | Owner and artwork decision-maker |

L12 (the indexing decision) then needs the exact candidate, notice text, target and rollback named. Keeping the current favicon is a valid L07 disposition.

## Draft public notice

[PRIVACY-NOTICE-DRAFT.md](PRIVACY-NOTICE-DRAFT.md) holds English and Arabic text for the public-service notice. Every unconfirmed fact is a bracketed `[… — PENDING]` marker, using the same markers as `../refined-preview-20261022/LAUNCH-INPUTS.json`. It is **not** wired into the site, so the live preview notice is unchanged. It is not legal advice, and the Arabic needs native review.

## Limits

No test result here transfers to a different artifact. Engineering checks are not owner, native-language, assistive-technology or physical-device acceptance.
