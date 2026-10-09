#!/usr/bin/env python3
"""RP01 manifest builder (not the VAL-16 release manifest). Run from the repository root:
  python3 -I GEM_V3.0_RP01_Release_Artifact_Promotion/15_scripts/rp01_manifest.py"""
import csv
import hashlib
import json
from pathlib import Path

RP = Path("GEM_V3.0_RP01_Release_Artifact_Promotion")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
skip = {"MANIFEST.json", "SHA256SUMS.txt", ".DS_Store"}
files = sorted(p for p in RP.rglob("*") if p.is_file() and p.name not in skip and "__pycache__" not in p.parts and not p.name.startswith("~$"))
entries = [{"path": p.relative_to(RP).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files]
base = list(csv.DictReader(open(RP / "02_RP01_Authorized_Baseline.csv", encoding="utf-8")))
m = {
    "package": RP.name,
    "purpose": "GEM V3.0 release-artifact promotion record and promoted artifacts (not the VAL-16 release manifest)",
    "status": "GEM™ V3.0 — OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE — FORMAL DEFERRALS RECORDED — ARTIFACT-SPECIFIC EXTERNAL-ISSUE RESTRICTIONS APPLY",
    "created": "2026-10-09",
    "branch": "claude/gem-worktree-safety-30b559",
    "based_on_head": "a8ebc8da1f5cb66f4ab369c90dcf5844a17e18ed",
    "gates_closed_by_this_package": 0,
    "pdfs_generated": 0,
    "tags_or_releases_created": 0,
    "confidential_documents_included": False,
    "self_hash_policy": "MANIFEST.json and SHA256SUMS.txt do not hash themselves; SHA256SUMS.txt also covers MANIFEST.json.",
    "baseline_sources": [{"id": r["Artifact ID"], "path": r["Source path"], "fa01_sha256": r["FA01 SHA256"], "current_sha256": r["Current SHA256"]} for r in base],
    "files": entries,
}
(RP / "MANIFEST.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
lines = [e["sha256"] + "  " + e["path"] for e in entries] + [sha(RP / "MANIFEST.json") + "  MANIFEST.json"]
(RP / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("manifest: %d files" % len(entries))
