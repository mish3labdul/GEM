# gem.mish3l.com replacement — 21 October 2026

**Status: deployed and verified.** Owner authorization: “use gem.mish3l.com, replace old one”. The accepted M4-R1 bilingual site replaces the former homepage at https://gem.mish3l.com. Arabic is the default; English is at `/en/`.

| Item | Evidence |
|---|---|
| Pages project / production branch | `gem-website-v01` / `main`; existing direct-upload project |
| New production deployment | `3e354187-a9f0-4727-81f6-a1e4b721ea6d`, https://3e354187.gem-website-v01.pages.dev |
| Tested preview | https://6ff97d6a.gem-website-v01.pages.dev; 23 browser scenarios passed before replacement |
| Accepted source | `cbd46be2289a6668463fbeac83af8f96e78f4883`, draft PR #21; no Git merge or release |
| Previous production deployment | `1707ac00-6cc2-420a-ac29-7e8ea1fedc39`, https://1707ac00.gem-website-v01.pages.dev; retained for rollback |
| DNS | Existing proxied CNAME to `gem-website-v01.pages.dev` retained; no DNS mutation |
| Local preparation | Isolated copy, build/static checker and four disposable build tests PASS |
| Live artifact | All 42 served artifact files verified, including all ten localized HTML pages; robots checked for retained disallow policy |
| Live behaviour | 23 scenarios verified: 22 passed initially, one navigation timeout passed on targeted retry with a remote-appropriate timeout; original failure evidence preserved |
| Visual checks | Arabic/English homepage captures at 375/1440px, no document overflow or required-font failure; visually inspected Arabic mobile capture |

Only `dist` was uploaded. `_headers` retains noindex, nosniff, referrer policy, native form-action protection and revalidation. `_redirects` sends `/` to `/ar/` and preserves the old English/Arabic Privacy URLs. Source masters, build scripts, QA records and hosting configuration files are not served; exposure probes return 404. Unknown routes return a real 404.

This replaces the old public URL with the accepted **noindex concept preview**. It does not approve production artwork, remove concept qualifications, create a receiving enquiry backend or close native Arabic, actual assistive-technology/device, micro favicon, rights or supplier gates. No claim of unrestricted/indexable public-release readiness is made.

Wrangler 4.34.0 was already installed and authenticated with account/user/zone read and Pages write scopes. The MCP connection remains a separate read-only connection. No local tools were installed or upgraded. The hosting account reports deployment success for the exact source commit.

Files: `candidate.json`, `rollback.json`, `old-home.html`, `preview-browser.json`, `live-browser.json`, `live-browser-retry.json`, `live-http.json`, `live-captures/` and final `deployment.json`. The immutable M6 handoff package and historical website copies remain unchanged. This dated record supersedes earlier “not deployed” statements for the replacement URL only.

Rollback, if required: use the retained previous production deployment above through Pages' rollback action, or the exact POST endpoint recorded in `rollback.json`. Do not delete the project, change DNS or rewrite Git/release history. Rollback was prepared but not invoked.
