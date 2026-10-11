# 16 · PR Proposal (NOT OPENED)

**No PR is opened. Nothing is pushed, merged or published.** This text is a proposal for the Brand Owner to use only if they later explicitly authorize a branch push and a PR.

**Title:** Audit: ODI01-R1 technical reconciliation (validation-ID checker; 400-only fonts) — unapproved, AC20 open

**Base:** `main` (`4ea0d11`) · **Head:** `claude/gem-worktree-safety-30b559`

## Summary
- Fixes the validation-ID QA check so explanatory references to the intentionally unallocated validation ID pass while active use fails (30 regression cases; cross-document QA 20/20).
- Completes D5: 228 brand-font bold flags → 0; five weight-500 wordings corrected; four 500-weight tokens now state FUTURE DESIGN INTENT = 500 / CURRENT IMPLEMENTATION = 400. No font added, no token value or status changed.
- Adds only a new folder `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/`; authoritative originals are untouched.
- Status: GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE.

## Review checklist
- [ ] `05` validation-ID rule and `validation_id_checker_tests.json`
- [ ] `07` 400-only implementation; `07_Font_Bold_Flag_Before_After.csv`; the 9 Part B slides with weaker run-in-head emphasis (owner-accepted as a temporary 400 treatment; no workaround)
- [ ] `18_qa_evidence/affected_slide_visual_qa.md` (LibreOffice evidence only)
- [ ] Tokens: 153/153 values; 26 downward statuses; 0 promotions
- [ ] Nothing promoted; AC20 still OPEN; D3 unresolved; D7 no change

## Not in scope / not claimed
Release, production readiness, native-application validation (PowerPoint, Word, Acrobat, AT), supplier values, Arabic approval, rights clearance, visibility change, D3 resolution.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
