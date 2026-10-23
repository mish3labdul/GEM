# Cloudflare Pages — manual deployment

The current accepted preview is https://gem.mish3l.com, served by the existing direct-upload Pages project `gem-website-v01`, production branch `main`. The hosting branch name does not merge the GitHub PR. DNS remains the existing proxied CNAME to `gem-website-v01.pages.dev`.

The build copies `_headers` and `_redirects` from this directory into `dist`, including on a clean rebuild. They preserve noindex, native form-submission protection, nosniff, referrer policy, cache revalidation, the Arabic root redirect and legacy Privacy URLs. Application layout, copy, artwork and local-only brief behaviour are unchanged.

## Deploy with the script

`hosting/cloudflare/deploy.sh` runs the steps below with guards and live verification: it needs a clean committed tree, rebuilds, runs the checks, deploys to the `remake-review` preview branch by default (`--branch NAME` for another alias), and verifies the routes, the noindex header and the fingerprinted CSS/JS against `dist`. `--production` deploys to `main` after you type `deploy`, then verifies `gem.mish3l.com` as well. Assets are served with a four-hour browser cache set at the Cloudflare zone, so CSS and JS URLs carry a content hash from the build. See the [M9 record](../../../records/m9-release-confidence-20261023/README.md) for the cache finding, the rollback rehearsal and recovery steps.

## Review and deploy manually

From a clean reviewed commit in `website/remake`, with the existing Wrangler CLI authenticated:

```sh
env -u SITE_ORIGIN node build.mjs
python3 check.py
python3 qa/production-check.test.py
wrangler whoami
wrangler pages deploy dist --project-name gem-website-v01 --branch remake-review --commit-hash "$(git rev-parse HEAD)" --commit-dirty=false
```

Verify the returned immutable preview URL: ten routes, assets/fonts, equivalent-language navigation, all five product states, local brief/download, root redirect, real 404s and noindex/form protection. Record the current production deployment ID and rollback URL before replacing the custom-domain version. Deploy **the same validated directory** to the production hosting slot only with authorization:

```sh
wrangler pages deploy dist --project-name gem-website-v01 --branch main --commit-hash "$(git rev-parse HEAD)" --commit-dirty=false
```

Verify `gem.mish3l.com` directly after deployment and save the deployment ID, source commit, artifact hashes and test results. Roll back through Pages to the recorded previous successful production deployment if necessary. Do not delete the project, alter unrelated DNS or rewrite release history.

Only `dist` is uploaded. Source masters, records, QA files and the repository root are not serving roots. Pages parses `_headers`/`_redirects` as configuration; they are not public source downloads. No Worker, receiving backend or new Cloudflare resource is required.

## Authorization and indexing

CI validates builds and loopback interactions only. It has read-only repository permissions, no Cloudflare credentials and no deployment step. A green check is not a deployment or merge decision.

Pages headers deliberately retain noindex even when a separately isolated build uses `SITE_ORIGIN` to test production metadata. That variable alone does not authorize indexing. Native Arabic, actual assistive-technology/device, micro favicon, rights and production/supplier decisions remain open. Changing indexing/privacy/contact behaviour requires its own review; do not silently remove the policy to make a deployment appear launched.

The [dated deployment record](../../../records/deployment-2026-10-21/REPORT.md) identifies the live and retained rollback deployments. Historical records remain bounded to their capture time.
