#!/usr/bin/env python3
"""OD01 pre-publication content scan of a Git revision range.

Run from the repository root:  python3 -I GEM_V3.0_RC2_OD01_Owner_Decision_Formalization/11_scripts/od01_prepublication_scan.py <base-rev> [<head-rev>]

Reads every file added or modified in <base>..<head> from the head revision (not the working tree) and scans:
  * text files line by line;
  * Office containers (pptx/docx/xlsx/zip): every member, including docProps/*.xml and all *.rels;
  * PDF and image files: raw bytes (info dictionary, XMP, text chunks).
Also lists files removed in the range, prohibited path names, and creator metadata values.
Self-tests prove each pattern matches a known sample before the scan runs. Read-only. Prints a summary.
Patterns are assembled from fragments so this file does not contain the strings it searches for.
"""
import io
import re
import subprocess
import sys
import zipfile
from collections import Counter

BASE = sys.argv[1]
HEAD = sys.argv[2] if len(sys.argv) > 2 else "HEAD"

LOCAL = re.compile("/Us" + "ers/|media" + "center1|claude-" + "501|/pri" + "vate/(tmp|var)|file:" + "///|\\.claude/work" + "trees|[A-Z]:\\\\Us" + "ers\\\\")
SECRET = re.compile(
    "gh[opsu]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|"
    "-----BEGIN [A-Z ]*PRIVATE KEY|xox[baprs]-[A-Za-z0-9-]{10,}|eyJ[A-Za-z0-9_-]{20,}\\.[A-Za-z0-9_-]{10,}\\.[A-Za-z0-9_-]{5,}|"
    "(?i:(password|passwd|api[_-]?key|secret|bearer|authorization)\\s*[:=]\\s*['\"]?[A-Za-z0-9_\\-./+]{12,})")
CLAIM = re.compile(
    "APPROVED V3\\.0|Approved V3\\.0|PRODUCTION READY|Production Ready|SYSTEM READY|\\bRELEASED\\b|AC20 (is )?closed|"
    "Legal/IP cleared|legally cleared|WCAG 2\\.2 AA (conform|compliant|fully)|screen-reader validation (is )?complete|"
    "linguistic(ally)? approv(ed|al) (is )?complete", re.I)
NEGATION = re.compile(r"\bnot\b|\bno\b|\bnever\b|prohibit|do not|does not|nothing|without|unless|may not|NOT RELEASED|fixture|checker|\bcheck", re.I)
BAD_NAMES = re.compile(
    "local_only|\\.DS_Store|CLAUDE\\.local|settings\\.local|(^|/)\\.claude/|~\\$|\\.lock$|\\.env$|\\.pem$|\\.key$|id_rsa|\\.p12$|\\.mov$|\\.mp4$|\\.tsv$|raw_native_sweeps/Part_")
ZIP_EXT = (".pptx", ".docx", ".xlsx", ".zip")


def self_test():
    assert LOCAL.search("/Us" + "ers/someone/x")
    assert LOCAL.search("target=file:" + "///x")
    assert SECRET.search("gh" + "p_" + "a" * 36)
    assert SECRET.search("pass" + "word: Abcdefghijklmnop1")
    assert SECRET.search("-----BEGIN RSA PRIV" + "ATE KEY-----")
    assert CLAIM.search("status: SYSTEM " + "READY")
    assert not LOCAL.search("relative/path/file.md")
    assert not SECRET.search("normal prose without secrets")


def git(*args, text=True):
    r = subprocess.run(["git", *args], capture_output=True, check=True)
    return r.stdout.decode("utf-8", "replace") if text else r.stdout


def blob(path):
    return subprocess.run(["git", "show", "%s:%s" % (HEAD, path)], capture_output=True, check=True).stdout


hits = {"local_path": [], "secret": [], "claim_positive": [], "claim_negated": []}
creators = Counter()
inventory = Counter()


def scan_text(label, text):
    for n, line in enumerate(text.splitlines(), 1):
        if LOCAL.search(line):
            hits["local_path"].append("%s:%d" % (label, n))
        if SECRET.search(line):
            hits["secret"].append("%s:%d" % (label, n))
        if CLAIM.search(line):
            (hits["claim_negated"] if NEGATION.search(line) else hits["claim_positive"]).append("%s:%d" % (label, n))


def scan_bytes(label, data):
    text = data.decode("latin-1")
    if LOCAL.search(text):
        hits["local_path"].append(label + " (binary content)")
    if SECRET.search(text):
        hits["secret"].append(label + " (binary content)")


def scan_zip(label, data):
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        hits["local_path"].append(label + " (unreadable zip)")
        return
    for name in z.namelist():
        raw = z.read(name)
        if name.endswith((".xml", ".rels", ".txt", ".json", ".csv", ".md")) or "docProps" in name:
            text = raw.decode("utf-8", "replace")
            scan_text("%s!%s" % (label, name), text)
            if name.startswith("docProps/"):
                for tag in ("dc:creator", "cp:lastModifiedBy", "Application", "Company", "Manager"):
                    for m in re.finditer("<%s>([^<]*)</%s>" % (tag, tag), text):
                        creators["%s=%s" % (tag, m.group(1))] += 1
        else:
            scan_bytes("%s!%s" % (label, name), raw)


def main():
    self_test()
    changed = [p for p in git("diff", "--name-only", "--diff-filter=ACMR", "-z", "%s..%s" % (BASE, HEAD)).split("\0") if p]
    removed = [p for p in git("diff", "--name-only", "--diff-filter=D", "-z", "%s..%s" % (BASE, HEAD)).split("\0") if p]
    commits = git("rev-list", "--count", "%s..%s" % (BASE, HEAD)).strip()
    touched = set()
    for c in git("rev-list", "%s..%s" % (BASE, HEAD)).split():
        touched.update(p for p in git("diff-tree", "--no-commit-id", "--name-only", "-r", "--root", "-z", c).split("\0") if p)
    bad_names = sorted(p for p in touched if BAD_NAMES.search(p))
    for p in changed:
        data = blob(p)
        ext = p.lower().rsplit(".", 1)[-1] if "." in p else ""
        inventory[ext or "(none)"] += 1
        if p.lower().endswith(ZIP_EXT):
            scan_zip(p, data)
        elif ext in ("pdf", "png", "jpg", "jpeg", "gif", "svg", "eps") and ext != "svg":
            scan_bytes(p, data)
            if ext == "pdf":
                for m in re.finditer(rb"/(Creator|Producer|Author)\s*\(([^)]{0,80})\)", data):
                    creators["pdf:%s=%s" % (m.group(1).decode(), m.group(2).decode("latin-1"))] += 1
        else:
            try:
                scan_text(p, data.decode("utf-8"))
            except UnicodeDecodeError:
                scan_bytes(p, data)
    print("range: %s..%s  commits=%s  files_changed=%d  removed_in_range_end_state=%d" % (BASE[:12], HEAD, commits, len(changed), len(removed)))
    print("file types:", dict(inventory.most_common(12)))
    print("prohibited path names touched by ANY commit in range:", bad_names if bad_names else "none")
    print("secret pattern hits:", len(hits["secret"]), hits["secret"][:10])
    print("local-path hits:", len(hits["local_path"]))
    by_file = Counter(h.split(":")[0] for h in hits["local_path"])
    for f, n in sorted(by_file.items()):
        print("   %3d  %s" % (n, f))
    print("overclaim phrase lines: positive-looking=%d negated/explanatory=%d" % (len(hits["claim_positive"]), len(hits["claim_negated"])))
    for h in hits["claim_positive"][:60]:
        print("   POS?", h)
    print("creator/producer metadata values:", dict(creators.most_common(15)))


if __name__ == "__main__":
    main()
