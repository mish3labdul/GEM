#!/usr/bin/env bash
# Manual Pages deploy with checks and live verification. See README.md in this directory.
#   deploy.sh                  preview deploy to branch "remake-review" (safe, own URL)
#   deploy.sh --branch NAME    preview deploy to another branch alias
#   deploy.sh --production     deploy to the live site (branch main); asks you to type "deploy"
set -euo pipefail

PROJECT=gem-website-v01
LIVE_URL=https://gem.mish3l.com
BRANCH=remake-review
PRODUCTION=0

while [ $# -gt 0 ]; do
  case "$1" in
    --production) PRODUCTION=1; BRANCH=main ;;
    --branch) BRANCH="${2:?--branch needs a name}"; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

cd "$(dirname "$0")/../.."          # website/remake
ROOT=$(git rev-parse --show-toplevel)
COMMIT=$(git rev-parse HEAD)

# 1. Source must be a committed, clean tree; dist must match what is committed.
if [ -n "$(git status --porcelain --untracked-files=no -- . ':!../assets-hub')" ]; then
  echo "Uncommitted changes under website/remake. Commit them first." >&2; exit 1
fi
env -u SITE_ORIGIN node build.mjs
if ! git diff --quiet -- dist; then
  echo "dist differs from the committed copy. Commit the rebuilt dist first." >&2; exit 1
fi

# 2. Local checks.
python3 check.py >/dev/null
python3 qa/production-check.test.py 2>&1 | tail -2

# 3. Deploy.
if [ "$PRODUCTION" = 1 ]; then
  echo "About to replace the LIVE site at $LIVE_URL with commit ${COMMIT:0:7}."
  read -r -p 'Type "deploy" to continue: ' ANSWER
  [ "$ANSWER" = deploy ] || { echo "Cancelled."; exit 1; }
fi
LOG=$(mktemp)
npx wrangler pages deploy dist --project-name "$PROJECT" --branch "$BRANCH" \
  --commit-hash "$COMMIT" --commit-dirty=false | tee "$LOG"
DEPLOY_URL=$(grep -Eo 'https://[a-z0-9.-]+\.pages\.dev' "$LOG" | head -1)
[ -n "$DEPLOY_URL" ] || { echo "Could not read the deployment URL." >&2; exit 1; }
rm -f "$LOG"

# 4. Verify the deployment URL, then the custom domain for production.
verify() {
  local base=$1 fail=0 route code header ref want got
  for route in ar en ar/about en/about ar/amenities-packaging en/amenities-packaging ar/contact en/contact ar/privacy en/privacy; do
    code=$(curl -s -o /dev/null -w '%{http_code}' "$base/$route/")
    [ "$code" = 200 ] || { echo "FAIL $base/$route/ -> $code"; fail=1; }
  done
  header=$(curl -sI "$base/en/" | tr -d '\r' | grep -i '^x-robots-tag' || true)
  case "$header" in *noindex*) ;; *) echo "FAIL noindex header missing on $base/en/"; fail=1 ;; esac
  # Every fingerprinted CSS/JS the page links must be served and equal the local file.
  for ref in $(curl -s "$base/en/" | grep -Eo '(href|src)="/[A-Za-z0-9._-]+\.(css|js)\?v=[0-9a-f]{10}"' | sed -E 's/^[a-z]+="//; s/"$//'); do
    want=$(shasum -a 256 "dist/${ref%%\?*}" | cut -d' ' -f1)
    got=$(curl -s "$base$ref" | shasum -a 256 | cut -d' ' -f1)
    [ "$want" = "$got" ] || { echo "FAIL $base$ref differs from dist"; fail=1; }
  done
  [ "$fail" = 0 ] && echo "OK $base" || return 1
}
verify "$DEPLOY_URL"
if [ "$PRODUCTION" = 1 ]; then
  sleep 5; verify "$LIVE_URL"
fi
echo "Source $COMMIT deployed to $PROJECT ($BRANCH): $DEPLOY_URL"
echo "Record the deployment ID and the previous production ID before relying on rollback."
