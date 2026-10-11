#!/bin/zsh
# AR01: stage a scratch variant in PowerPoint's container, open it, probe slide 39 shapes natively (read-only), leave it open for a screenshot.
# usage: ar01_probe_variant.sh <variant_pptx_in_local_only/scratch/variants> <outdir>
V="$1"; OUT="$2"; T=~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/GEM_AR01_NATIVE_TEST; HERE="${0:A:h}"; N="${V:t}"
mkdir -p "$T" "$OUT"; cp "$V" "$T/$N"; echo "staged $N sha $(shasum -a 256 "$T/$N" | cut -c1-12)"
perl -e 'alarm 60; exec @ARGV' osascript -e 'on run argv
 with timeout of 50 seconds
  tell application "Microsoft PowerPoint" to open (POSIX file (item 1 of argv))
 end timeout
end run' "$T/$N"; sleep 2
osascript -e 'tell application "Microsoft PowerPoint" to return (name of presentation 1) & " slides=" & (count of slides of presentation 1) & " saved=" & (saved of presentation 1 as string)'
osascript -e "tell application \"Microsoft PowerPoint\" to go to slide (view of active window) number 39" >/dev/null 2>&1
for sh in "Text 8" "Text 4"; do perl -e 'alarm 100; exec @ARGV' osascript "$HERE/ar01_native_char_bounds.applescript" "$N" 39 "$sh" > "$OUT/probe_${N%.pptx}_${sh// /_}.tsv" 2>&1; done
echo "probes written: $(ls $OUT | grep -c "${N%.pptx}")"
