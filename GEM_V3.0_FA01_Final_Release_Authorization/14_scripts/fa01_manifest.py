#!/usr/bin/env python3
"""FA01 manifest builder. Run from the repository root: python3 -I GEM_V3.0_FA01_Final_Release_Authorization/14_scripts/fa01_manifest.py
Writes MANIFEST.json and SHA256SUMS.txt. Relative paths only. This manifest is not the VAL-16 release manifest."""
import hashlib
import json
from pathlib import Path

PKG = Path("GEM_V3.0_FA01_Final_Release_Authorization")
HR = Path("GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/18_candidate_corrections")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
skip = {"MANIFEST.json", "SHA256SUMS.txt", ".DS_Store"}
files = sorted(p for p in PKG.rglob("*") if p.is_file() and p.name not in skip and "__pycache__" not in p.parts and not p.name.startswith("~$"))
entries = [{"path": p.relative_to(PKG).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files]
lh = Path("GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates")
tok = Path("PartB_RC2/05_release/tokens")
outside = sorted(list(HR.iterdir()) + [lh / ("GEM_Letterhead_%s.docx" % n) for n in ("English_First_Page", "English_Continuation", "Executive", "Minimal")]
                 + [tok / "gem-tokens.v3.0-rc2.json", tok / "gem-tokens.v3.0-rc2.css", Path("GEM_Brand_Assets_v1.0/04_official_kit/SHA256SUMS.txt")])
m = {
    "package": PKG.name,
    "purpose": "AC20 final Brand Owner release authorization record (governance documentation only; not the VAL-16 release manifest)",
    "status": "GEM™ V3.0 — OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE — FORMAL DEFERRALS RECORDED — ARTIFACT-SPECIFIC EXTERNAL-ISSUE RESTRICTIONS APPLY",
    "ac20": "AUTHORIZED WITH FORMAL DEFERRALS AND RELEASE-SCOPE EXCLUSIONS",
    "created": "2026-10-09",
    "branch": "claude/gem-worktree-safety-30b559",
    "based_on_head": "e99c4100eef6e547105be1c1563653d9a7aed109",
    "gates_closed_by_this_package": 0,
    "confidential_documents_requested_or_included": False,
    "remote_operations_authorized": False,
    "self_hash_policy": "MANIFEST.json and SHA256SUMS.txt do not hash themselves; SHA256SUMS.txt also covers MANIFEST.json.",
    "files": entries,
    "baseline_files_outside_package": [{"path": p.as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in outside],
}
(PKG / "MANIFEST.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
lines = [e["sha256"] + "  " + e["path"] for e in entries] + [sha(PKG / "MANIFEST.json") + "  MANIFEST.json"]
(PKG / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("manifest: %d files, %d baseline files outside" % (len(entries), len(outside)))
