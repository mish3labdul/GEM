#!/bin/zsh
# NP01 native table-cell sweep driver (read-only). Usage: np01_run_table_sweep.sh <outdir> <Part_X> <slideCount>
OUT="$1"; part="$2"; n="$3"; HERE="${0:A:h}"; mkdir -p "$OUT"
name="NP01_${part}_test_copy.pptx"; f="$OUT/${part}_tables.tsv"; : > "$f"; : > "$OUT/${part}_tables.fail"
for s in $(seq 1 $n); do
  ok=0
  for try in 1 2; do
    res=$(perl -e 'alarm 200; exec @ARGV' osascript "$HERE/np01_native_table_sweep_slide.applescript" "$name" $s 2>&1)
    if [[ $? -eq 0 && "$res" != *"script error"* && "$res" != *"execution error"* ]]; then ok=1; break; fi
    sleep 3
  done
  if [[ $ok -eq 1 ]]; then printf '%s\n' "$res" | sed '/^$/d' >> "$f"; else echo "slide $s: $res" >> "$OUT/${part}_tables.fail"; fi
  echo "$part tables $s/$n ok=$ok" >> "$OUT/progress_tables.log"
done
echo "DONE $part" >> "$OUT/progress_tables.log"
