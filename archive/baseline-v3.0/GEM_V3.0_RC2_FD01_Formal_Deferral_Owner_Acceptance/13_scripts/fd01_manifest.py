#!/usr/bin/env python3
"""FD01 manifest builder. Run from the repository root: python3 -I GEM_V3.0_RC2_FD01_Formal_Deferral_Owner_Acceptance/13_scripts/fd01_manifest.py
Writes MANIFEST.json and SHA256SUMS.txt for the package. Relative paths only."""
import hashlib
import json
from pathlib import Path

PKG = Path("GEM_V3.0_RC2_FD01_Formal_Deferral_Owner_Acceptance")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
skip = {"MANIFEST.json", "SHA256SUMS.txt", ".DS_Store"}
files = sorted(p for p in PKG.rglob("*") if p.is_file() and p.name not in skip and "__pycache__" not in p.parts and not p.name.startswith("~$"))
entries = [{"path": p.relative_to(PKG).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files]
m = {
    "package": PKG.name,
    "purpose": "Formal deferrals and owner acceptance of RC2 as-is (governance documentation only)",
    "status": "GEM™ V3.0 RC2 — OWNER ACCEPTED WITH FORMAL DEFERRALS; SYNCHRONIZED; NOT YET FINAL-RELEASE AUTHORIZED; AC20 OPEN",
    "created": "2026-10-09",
    "branch": "claude/gem-worktree-safety-30b559",
    "based_on_head": "617456255231a6b36ca5eb688451f8a72eef0eb7",
    "gates_closed_by_this_package": 0,
    "confidential_documents_requested_or_included": False,
    "remote_operations_authorized": False,
    "self_hash_policy": "MANIFEST.json and SHA256SUMS.txt do not hash themselves; SHA256SUMS.txt also covers MANIFEST.json.",
    "files": entries,
}
(PKG / "MANIFEST.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
lines = [e["sha256"] + "  " + e["path"] for e in entries] + [sha(PKG / "MANIFEST.json") + "  MANIFEST.json"]
(PKG / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("manifest: %d files" % len(entries))
