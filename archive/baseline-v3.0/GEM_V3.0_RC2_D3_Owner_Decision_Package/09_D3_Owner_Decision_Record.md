# 09 · D3 Owner Decision Record

**D3A — RESOLVED · D3B — RESOLVED · D3 — RESOLVED AT OWNER-DECISION LEVEL · X12 STREAM = BRAND**
Recorded 2026-10-09 from the Brand Owner's explicit instruction. Not to be re-confirmed.

D3A — Synchronization corrections C1–C4

[x] ACCEPTED
[ ] PARTIALLY ACCEPTED
[ ] REJECTED

Decision:
C1–C4 are accepted as supported synchronization corrections and remain implemented in controlled candidate copies.

Evidence:
`02_D3A_Authority_Verification.md` (all four SUPPORTED against the Register and the current Parts A–D) and `03_D3A_Implementation_Trace.md`. Scope: candidate copies only; promotion into authoritative folders is a separate authorized change.

D3B — X12 STREAM token

[x] BRAND
[ ] Logo
[ ] OTHER
[ ] OWNER DECISION STILL REQUIRED

Decision:
Use BRAND as the controlled X12 STREAM token for the GEM master-brand asset family.

Owner rationale (recorded in full):
- X12 STREAM follows the asset-library / controlled stream taxonomy.
- The governing asset-library category is Brand Masters.
- BRAND applies coherently across logo, symbol and related master-brand assets.
- BRAND avoids semantic duplication between STREAM and ASSET.
- The Part A slide 75 example using Logo conflicts with the rule stated on the same slide and is therefore treated as a synchronization defect in the example, not as the governing taxonomy.
- Existing source / historical filenames are not automatically renamed by this decision.
- No asset-ID algorithm is approved. No new checksum algorithm is approved. Source assets remain unchanged unless separately authorized through controlled migration.

Evidence (decision history, preserved):
- BRAND aligns with the Brand Masters / asset-library-folder reading (Part A slide 75 rule; Register X02 "01 Brand Masters"), has no STREAM/ASSET duplication (0 of 128 names, even if ASSET carried the noun "Logo"), scales to the other master-brand assets, and is already used by the 11 working files.
- Logo matched the explicit Part A slide 75 example and reads as self-describing; it is **NOT SELECTED** and is retained as history only.
- The governing evidence conflicted (rule vs example on the same slide; no authoritative enumeration of STREAM tokens). The owner resolved the conflict in favour of the rule. The conflict stays documented in `04` and `07`.

Effect recorded in this package: STREAM = BRAND is the SELECTED CONTROLLED STREAM; `D3B_X12_Selected_BRAND_Mapping.csv` is the SELECTED CONTROLLED MAPPING (128 rows, manifest-only, no source renames); the Logo mapping is NOT SELECTED; the Part A slide 75 example is corrected in a controlled candidate (STREAM token only).

D3 = RESOLVED AT OWNER-DECISION LEVEL.

This does NOT mean:
- AC20 closed, or release authorized;
- Legal/IP cleared (D7 remains LEGAL/IP DECISION PENDING; NO PUSH);
- source assets migrated or renamed;
- an asset-ID algorithm or checksum algorithm approved;
- production readiness established, or any font, native-QA or supplier evidence gate closed.

Brand Owner: owner instruction of 2026-10-09 (named signature/initials not recorded in this file): __________________

Conditions / comments: STREAM = BRAND applies prospectively to controlled names and manifests (X12). The ASSET and VARIANT value lists remain subject to controlled taxonomy confirmation (`10`).
