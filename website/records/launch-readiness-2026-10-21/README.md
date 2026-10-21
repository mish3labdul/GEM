# M6 current launch readiness — 21 October 2026

For the owner and acceptance reviewers: use this register to assign the remaining reviews, record evidence and decide whether an indexable launch can be proposed. **Current status: hosted noindex concept preview; human acceptance remains pending.** This record supersedes earlier unconfirmed-domain, undeployed and missing-remake-CI statements. Historical handoff archives and dated reports remain unchanged.

## Confirmed delivery

| Item | Verified position |
|---|---|
| Repository / branch / target | `mish3labdul/GEM`; `codex/gem-remake-m4-r1-20261021` → `main` |
| Review | [PR #21](https://github.com/mish3labdul/GEM/pull/21), open and draft when checked; no merge |
| Tested repository revision | `b095fc2daffac078009c8dad713d0f5704b0f71a`; this documentation update follows that revision |
| Hosted review surface | [Arabic](https://gem.mish3l.com/ar/) / [English](https://gem.mish3l.com/en/); both returned HTTP 200 with HTML and response-header noindex during this update |
| Hosting | Existing Cloudflare Pages direct-upload project `gem-website-v01`; deployment branch `main` is separate from Git merge state |
| Deployed source / deployment | `cbd46be2289a6668463fbeac83af8f96e78f4883`; `3e354187-a9f0-4727-81f6-a1e4b721ea6d`; [deployment and rollback evidence](../deployment-2026-10-21/README.md) |
| Hosted CI | [Run 39645066307](https://github.com/mish3labdul/GEM/actions/runs/39645066307): collection integrity, older-site Chromium, remake Chromium and remake Firefox all passed on `b095fc2` |
| Remake verification | Five disposable build tests and 23 browser scenarios per browser; these are engineering checks, not native-language or actual assistive-technology acceptance |
| Artifact controls | Clean build reproduces the 45-file deployed artifact, including Pages policy and redirects; [manual hosting runbook](../../remake/hosting/cloudflare/README.md) |
| Contact behaviour | Brief generation, copy, download and clear stay local; no receiving backend |

Later repository revisions add hosting reproducibility and CI; they are not claimed as deployed revisions. CI contains no deployment step or Cloudflare credentials. This update changes documentation only.

## Remaining work, in order

1. Assign a native Arabic reviewer and an accessibility/device reviewer. Complete the [live acceptance checklist](LIVE-ACCEPTANCE.md) across all ten localized pages and the interactive journeys. Record the actual environment and evidence; do not infer human acceptance from automation.
2. Resolve the [gate register](GATES.csv): micro favicon, image/artwork rights, public operator/privacy practices and explicit retention of the current local-only enquiry flow. A receiving service would require separate implementation scope.
3. Correct evidenced findings, then repeat the affected checks on the revised candidate. Record source commit, deployment ID and review date so results cannot silently transfer to a different artifact.
4. Once blocking acceptance and public-use decisions are resolved, request PR review/merge and a separate, concrete launch decision. Specify the exact candidate, privacy text, indexing changes, target and rollback. Keep noindex until that decision and its implementation are approved.

Native Arabic, actual screen-reader, Safari/physical-device and rights acceptance are **pending**, not failed. Genuine Chromium 400% zoom already has bounded engineering evidence in the M6-R2 handoff; other environments remain unverified. The supplied micro favicon remains a review option, not an applied or approved change. B01/B02/D8 and the source documents' concept/working/production distinctions remain in force; this website process cannot close unrelated supplier or production-artwork gates.

## Recording a decision

Update a gate only with reviewer/decision-maker, date, candidate identity, result and linked evidence. Use `Pending`, `Pass`, `Fail` or `Held`; explain any `Not applicable` decision. An owner's visual selection, a hosted deployment and green CI each retain their distinct scope. No merge, deployment, indexing, artwork substitution or contact-flow change is authorized by completing this register.
