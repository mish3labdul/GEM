# Wording Candidates (UNAPPROVED — nothing below is applied to an original)

## Release status line (item 10; owner decision D3)
Preferred state:

> **GEM™ V3.0 RC2 — SYNCHRONIZED**
> **NOT RELEASED**
> **EVIDENCE GATES REMAIN**

Basis for "SYNCHRONIZED": 112 automated term/ID/version assertions pass across Parts A, B and C, and the Register is the shared authority. Qualifier: two synchronization defects remain in `main` until D3/D4 are accepted (stale Part A notes, stale Part C slide 44, token statuses). The deck text itself never says "SYSTEM READY"; it appears only in the three notes files covered by the candidate copies in `release_language/` (and in the historical AFC-era audit, left alone).

## Part D (owner decision D6)
| Where | Now | Candidate |
|---|---|---|
| Slide 15 | "Bleed, safe area and tolerances come from the approved supplier dieline." | "Bleed, safe area and tolerances come from the supplier dieline, once supplied and approved." |
| Slide 23 notes | "Supporting CSV registers contain full concept, source, asset, change and open-decision records." | "A mockup register is provided with this package; other registers are not part of it." |
| Slide 14 label | "GEM master artwork" | Keep, or "GEM logo kit (production master acceptance pending)" |
| Repo README line 9 | "approved mockups" | "owner-designated concept mockups (concept direction only)" |
| Asset Sync change log | "the approved Part D concept portfolio" | "the owner-designated Part D concept portfolio" |
| Final Release Notes addendum | "its approved mockups" | "its owner-designated concept mockups" |

Keep unchanged: "CONCEPT / NOT PRODUCTION ARTWORK" markings, "No item in this portfolio is an approved production asset."

## Token status labels
See `tokens/` candidate JSON and CSS (statuses only).
