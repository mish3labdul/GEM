#!/usr/bin/env python3
"""OD01 manifest builder.

Run from the repository root:  python3 -I GEM_V3.0_RC2_OD01_Owner_Decision_Formalization/11_scripts/od01_manifest.py [--d7] [--od01]

--d7    re-hash ONLY 09_D7_Owner_Decision_Record.md inside the D7 package manifest and
        checksum file, and add a supersession pointer to the manifest (other entries and
        the as-created 'status' string are left untouched).
--od01  write MANIFEST.json and SHA256SUMS.txt for the OD01 package.
Relative paths only.
"""
import hashlib
import json
import sys
from pathlib import Path

D7 = Path("GEM_V3.0_RC2_D7_Repository_Visibility_Decision_Package")
OD = Path("GEM_V3.0_RC2_OD01_Owner_Decision_Formalization")
RELEASE_LABEL = ("GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / "
                 "UNAPPROVED IMPLEMENTATION CANDIDATE")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def d7_update():
    rec = D7 / "09_D7_Owner_Decision_Record.md"
    manifest_path = D7 / "MANIFEST.json"
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in m["files"]:
        if entry["path"] == "09_D7_Owner_Decision_Record.md":
            entry["bytes"] = rec.stat().st_size
            entry["sha256"] = sha(rec)
    m["superseded_status_note"] = (
        "The 'status' value above is the as-created (2026-10-09, commit ab6d886) state. "
        "09_D7_Owner_Decision_Record.md was later populated with the Brand Owner's OD-G11 decision "
        "(current public repository approved; Legal/IP evidence open where required; AC20 open). "
        "See GEM_V3.0_RC2_OD01_Owner_Decision_Formalization/06_OD01_D7_Repository_Visibility_Decision.md. "
        "The pushed/merged/published flags describe the as-created state.")
    manifest_path.write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    sums_path = D7 / "SHA256SUMS.txt"
    out = []
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        if name in ("09_D7_Owner_Decision_Record.md", "MANIFEST.json"):
            digest = sha(D7 / name)
        out.append(digest + "  " + name)
    sums_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("D7 manifest and checksums updated for 09 and MANIFEST.json")


def od01_manifest():
    skip = {"MANIFEST.json", "SHA256SUMS.txt", ".DS_Store"}
    files = sorted(p for p in OD.rglob("*")
                   if p.is_file() and p.name not in skip and "__pycache__" not in p.parts)
    entries = [{"path": p.relative_to(OD).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)}
               for p in files]
    m = {
        "package": OD.name,
        "purpose": "Formalization of Brand Owner decisions OD-G01 to OD-G12; governance synchronization (documentation only)",
        "status": ("OD-G01..OD-G08 APPROVED; OD-G09 and OD-G10 ASSIGNED (Mashal); OD-G11 OWNER REPOSITORY VISIBILITY DECISION "
                   "RESOLVED (current public repository approved); LEGAL/IP EVIDENCE OPEN WHERE REQUIRED; OD-G12 AC20 OPEN"),
        "release_label": RELEASE_LABEL,
        "created": "2026-10-09",
        "branch": "claude/gem-worktree-safety-30b559",
        "based_on_head": "f550ddc901c012f0f0c3acfa4893f91569e87384",
        "gates_closed_by_this_package": 0,
        "ac20": "OPEN / FINAL RELEASE AUTHORIZATION PENDING",
        "val_18": "NOT ALLOCATED",
        "remote_authorization": "ONE controlled push of the existing branch to origin after QA (task-specific). No merge, PR, tag, release, force-push or visibility change.",
        "self_hash_policy": "MANIFEST.json and SHA256SUMS.txt do not hash themselves; SHA256SUMS.txt also covers MANIFEST.json.",
        "files": entries,
    }
    (OD / "MANIFEST.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [e["sha256"] + "  " + e["path"] for e in entries]
    lines.append(sha(OD / "MANIFEST.json") + "  MANIFEST.json")
    (OD / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("OD01 manifest: %d files" % len(entries))


if __name__ == "__main__":
    if "--d7" in sys.argv:
        d7_update()
    if "--od01" in sys.argv:
        od01_manifest()
