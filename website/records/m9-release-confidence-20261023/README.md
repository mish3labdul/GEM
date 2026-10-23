# M9 — operational reliability and release confidence, 23 October 2026

**Status: engineering work done on branch `m9/release-confidence`; not yet deployed to production.** M9's goal (from the roadmap) is that the public site can be maintained and recovered without undocumented session knowledge. This record covers what was found, what changed, what was rehearsed and what still needs an owner decision. It adds no product facts and changes no artwork or copy.

## 1. Cache finding and fix

**Finding.** HTML is served with `Cache-Control: no-cache` (correct, from `_headers`). CSS, JS, fonts and images are served with `max-age=14400`, four hours, although `_headers` asks for `no-cache` on every path. Cause, read from the Cloudflare API: the zone `mish3l.com` has **Browser Cache TTL = 14400 seconds**, which raises the lifetime of cached static files. Effect: after a deploy, a visitor who loaded the site in the previous four hours can receive new HTML with an old `style.css`, `integration.css` or `app.js`. We saw a mild version of this on 23 Oct when the dark favicon appeared late on the custom domain.

**Fix in the repository (done).** `build.mjs` now appends a content hash to every stylesheet and script URL (`/app.js?v=fa08b93bcd`). A changed file gets a new URL, so a deploy takes effect at once regardless of the four-hour cache. The hash is the first 10 hex characters of the file's SHA-256. The 404 page uses the same scheme. A new build test (`test_script_and_style_urls_carry_the_content_hash`) checks every CSS and JS reference on all ten pages and the 404 page against the file in `dist`. The font-error regression test now matches `**/app.js*`.

**Not fixed, needs the owner.** Fonts and images keep the same file names, so they can still be up to four hours stale after a replacement (the share image is the main example; link-preview scrapers cache it anyway). Two ways to remove the remaining lag, both outside the repository:
- Set the zone's Browser Cache TTL to "Respect Existing Headers". This is a **zone-wide setting that also affects every other subdomain on `mish3l.com`** (for example the assets hub), so it was **not changed**.
- Fingerprint images and fonts as well (a larger build change; only worth doing if they change often).

## 2. Rollback and recovery, rehearsed without touching production

Pages can roll back only production deployments, and a production rollback briefly changes the live site, so it was not invoked. What was proved instead:

| Check | Result |
|---|---|
| Production deployments retained and restorable | The Pages API lists **15 successful production deployments**, newest `718a9a58`, back to 12 Oct 2026. Every one is a rollback candidate |
| An old commit can be rebuilt exactly | Commit `2552dc8` (font retry) was checked out in a throwaway worktree and rebuilt with `node build.mjs`: **0 of 63 files differed** from the committed `dist` |
| That rebuild equals what was deployed | It was deployed to a temporary preview branch (`rollback-rehearsal`). **61 of 61 files** served matched the original production deployment `52dd8d17` byte for byte, and the preview kept `X-Robots-Tag: noindex, nofollow` |
| Cleanup | The temporary preview deployment was deleted through the API and the throwaway worktree was removed |

**Recovery procedures** (also in `hosting/cloudflare/README.md`):
1. *Fastest, live site is wrong:* Cloudflare dashboard → Workers & Pages → `gem-website-v01` → Deployments → pick the last good production deployment → "Rollback to this deployment". Or the API call `POST /accounts/{account}/pages/projects/gem-website-v01/deployments/{deployment}/rollback`. Do not delete the project, change DNS, or rewrite git history.
2. *No suitable earlier deployment:* check out the known-good commit, run `hosting/cloudflare/deploy.sh --production` from it. The rehearsal shows the rebuild is byte-identical.

**Not rehearsed:** an actual production rollback and roll-forward. It would put an older version live for about a minute. If you want it exercised, approve a window and it can be done and timed.

## 3. One-command deploy

`website/remake/hosting/cloudflare/deploy.sh` replaces the multi-step manual procedure:
- Refuses to run with uncommitted changes under `website/remake` or a `dist` that differs from the commit.
- Builds, runs `check.py` and the build tests.
- Deploys to a preview branch by default (`remake-review`, or `--branch NAME`). Production needs `--production` and typing `deploy`.
- Verifies the new deployment URL (and, for production, `gem.mish3l.com`): all ten routes return 200, `X-Robots-Tag` contains noindex, and every fingerprinted CSS and JS file served equals the local `dist` file.

## 4. Access and ownership (facts as found, no secrets)

| Item | Finding |
|---|---|
| Cloudflare account | One account, `4a9100b16a188b4ac23765431fe8ac8e`, in the owner's name |
| Wrangler on this Mac | Signed in with an OAuth token for the owner's email; scopes: user read, account read, **pages write**, zone read. Wrangler is 4.58.0 (4.152.0 available); update not applied |
| Cloudflare connector in Claude Code | Authorized with Pages edit and zone read. Revoke: dashboard → My Profile → Access management → Authorized apps |
| GitHub `mish3labdul/GEM` | Public repository. The owner account is admin; one other collaborator has write access |
| CI | GitHub Actions, read-only; **no secrets**, no Cloudflare credentials, no deploy step |
| `main` branch protection | **None.** Required reviews and required CI checks are not enforced, so a push or a red PR can still reach `main` |
| Repository webhooks | Not checked (the CLI token lacks the permission) |

Recommended, needs the owner: enable branch protection on `main` requiring the four CI jobs; decide who else may hold Cloudflare access (a second account holder avoids a single point of failure); decide whether to refresh the Wrangler login.

## 5. Not done in M9 so far

- WebKit check of the font retry (needs the iOS Simulator or Safari again).
- Production deploy of the fingerprinting change (pending owner approval; see the PR).

## Verification

`node build.mjs`, `check.py`, the six build tests, and the Chromium regression suite (29 of 29) pass on this branch. CI results are recorded on the pull request.
