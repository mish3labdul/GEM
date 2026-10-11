#!/usr/bin/env python3
"""HR01 manifest builder. Run from the repository root: python3 -I GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/16_scripts/hr01_manifest.py
Writes MANIFEST.json and SHA256SUMS.txt for every committable file of the package (local_only/ and temp files excluded). Relative paths only."""
import hashlib
import json
from pathlib import Path

PKG = Path("GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
skip_names = {"MANIFEST.json", "SHA256SUMS.txt", ".DS_Store"}
files = sorted(p for p in PKG.rglob("*") if p.is_file() and p.name not in skip_names and "local_only" not in p.parts
               and "__pycache__" not in p.parts and not p.name.startswith("~$"))
entries = [{"path": p.relative_to(PKG).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files]
m = {
    "package": PKG.name,
    "purpose": "Human review queue closure: dispositions of the Arabic, accessibility-content, assistive-technology and Legal/IP review queues (documentation + unapproved candidates)",
    "status": "Queues dispositioned; 0 gates closed; Legal/IP gates OPEN; AC19 OPEN / HOLDER CONDITION INCOMPLETE; AC20 OPEN / FINAL RELEASE AUTHORIZATION PENDING; D8 OPEN",
    "release_label": "GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE",
    "created": "2026-10-09",
    "branch": "claude/gem-worktree-safety-30b559",
    "based_on_head": "c4671ecfed5f6eec1833b8fe3aabc63f8f4004c1",
    "gates_closed_by_this_package": 0,
    "publication": "Version-control publication of the branch is authorized for one controlled push; it is not release authorization.",
    "self_hash_policy": "MANIFEST.json and SHA256SUMS.txt do not hash themselves; SHA256SUMS.txt also covers MANIFEST.json.",
    "files": entries,
}
(PKG / "MANIFEST.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
lines = [e["sha256"] + "  " + e["path"] for e in entries] + [sha(PKG / "MANIFEST.json") + "  MANIFEST.json"]
(PKG / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("manifest: %d files" % len(entries))
