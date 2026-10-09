#!/usr/bin/env python3
"""RP01 promotion engine: anchored, count-checked, run-level OOXML edits with byte-copy of every untouched member.

A rule is (member_regex, old, new, expected_count, where). `where`:
  "text"  - inside <a:t>/<w:t>/<dc:*>/<cp:*> element text (old/new are plain text, XML-escaped here)
  "attr"  - inside name="..." attributes of <p:cNvPr>
  "xml"   - raw XML substring (metadata parts)
Every rule must match exactly its expected_count times across all matching members, otherwise the engine raises.
No member is rewritten unless a rule changed it; untouched members are copied with their original ZipInfo.
"""
import hashlib
import re
import zipfile
from xml.sax.saxutils import escape

TEXT_EL = re.compile(r"(<(?:a:t|w:t|dc:title|dc:subject|dc:description|cp:keywords)(?: [^>]*)?>)([^<]*)(</(?:a:t|w:t|dc:title|dc:subject|dc:description|cp:keywords)>)")
ATTR_NAME = re.compile(r'(<p:cNvPr [^>]*?name=")([^"]*)(")')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def apply_rules(src_path, dst_path, rules, dry=False):
    """Return (change_log, member_report). change_log rows: (rule_idx, member, old, new, n)."""
    zin = zipfile.ZipFile(src_path)
    infos = zin.infolist()
    data = {i.filename: zin.read(i.filename) for i in infos}
    changed = {}
    log = []
    counts = [0] * len(rules)
    for name in [i.filename for i in infos]:
        raw = data[name]
        if not name.endswith((".xml", ".rels")):
            continue
        text = raw.decode("utf-8")
        orig = text
        for ri, (mre, old, new, expect, where, *_meta) in enumerate(rules):
            if not re.fullmatch(mre, name):
                continue
            n_here = 0
            if where == "text":
                exact = old.startswith("=")
                eo, en = escape(old[1:] if exact else old), escape(new)

                def sub_text(m):
                    nonlocal n_here
                    if exact:
                        if m.group(2) == eo:
                            n_here += 1
                            return m.group(1) + en + m.group(3)
                        return m.group(0)
                    c = m.group(2).count(eo)
                    if c:
                        n_here += c
                        return m.group(1) + m.group(2).replace(eo, en) + m.group(3)
                    return m.group(0)
                text = TEXT_EL.sub(sub_text, text)
            elif where == "attr":
                eo, en = escape(old, {'"': "&quot;"}), escape(new, {'"': "&quot;"})

                def sub_attr(m):
                    nonlocal n_here
                    c = m.group(2).count(eo)
                    if c:
                        n_here += c
                        return m.group(1) + m.group(2).replace(eo, en) + m.group(3)
                    return m.group(0)
                text = ATTR_NAME.sub(sub_attr, text)
            elif where == "re":
                text, c = re.subn(old, new, text, flags=re.S)
                n_here += c
            elif where == "xml":
                c = text.count(old)
                if c:
                    n_here += c
                    text = text.replace(old, new)
            else:
                raise ValueError(where)
            if n_here:
                counts[ri] += n_here
                log.append((ri, name, old, new, n_here))
        if text != orig:
            changed[name] = text.encode("utf-8")
    bad = [(i, rules[i][1][:60], counts[i], rules[i][3]) for i in range(len(rules)) if counts[i] != rules[i][3]]
    if dry:
        return log, counts
    if bad:
        raise RuntimeError("rule count mismatch (index, old, got, expected): %r" % bad)
    with zipfile.ZipFile(dst_path, "w") as zout:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            zi.create_system = i.create_system
            zi.comment = i.comment
            zout.writestr(zi, changed.get(i.filename, data[i.filename]))
    report = [(i.filename, "CHANGED" if i.filename in changed else "IDENTICAL",
               sha(data[i.filename]), sha(changed.get(i.filename, data[i.filename]))) for i in infos]
    return log, report
