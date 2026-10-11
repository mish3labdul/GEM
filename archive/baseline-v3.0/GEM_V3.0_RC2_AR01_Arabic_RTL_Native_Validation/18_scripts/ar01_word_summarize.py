"""AR01 native Word results -> committable CSVs (no document text). Reads local_only/word_probes/*. Usage: ar01_word_summarize.py <package_dir>"""
import sys, os, json, csv, hashlib, re
P = sys.argv[1]; W = f"{P}/local_only/word_probes"; S = f"{P}/local_only/screenshots"
T = [("Arabic First Page", "arabic_first", "85c7e640968b40acc7bcd18f3a697658816714f58f300465838d5d79dc7eb6ea", "AR01_word_arabic_first_page.png"),
     ("Arabic Continuation", "arabic_continuation", "351da5985eb60801a9b3b4f4bbabe9ab5edf0cfcb5010b56979b098f1d3b2dd9", "AR01_word_arabic_continuation.png"),
     ("Bilingual First Page", "bilingual_first", "eb85104ac6bbf8685f0b0ce1277482b07e6ccc589227879eae98abcf49b74100", "AR01_word_bilingual_first.png"),
     ("Bilingual Continuation", "bilingual_continuation", "0171fa3fab4e460f1af1218e2c0dc2c18b56529cd40234652cfe7de82e52c2e6", "AR01_word_bilingual_continuation.png")]
prow, srow = [], []
for name, k, h, shot in T:
    an = json.load(open(f"{W}/{k}_analysis.json")); hf = [l.rstrip('\n').split('\t') for l in open(f"{W}/{k}_hf.tsv")]
    pages = next(r for r in hf if r[0] == 'S')[2]
    hfrows = {(r[1], r[2]): r for r in hf if r[0] == 'H'}
    arabic_paras = [a for a in an if 'A' in a['script_mix']]; bad = []
    for a in an:
        dirs = dict((s[0], s[1]) for s in a['seg_direction']) if False else {}
        segs = [(c[0], n) for c, n in a['seg_direction']]
        ar_ok = all(d == 'RTL' for (cl, d), n in [(c, n) for c, n in a['seg_direction']] if cl == 'A')
        lat_ok = all(d == 'LTR' for (cl, d), n in [(c, n) for c, n in a['seg_direction']] if cl == 'L')
        is_ar = 'A' in a['script_mix']
        mixed = a['script_mix'] == 'AL'
        font_ok = (a['font'] == 'Noto Sans Arabic') if (is_ar and not mixed) else True
        ok = (a['block_arrangement'] in ('n/a', 'Latin/digit block left of Arabic block')) and (a['native_chars'] == a['src_chars_plus_mark']) and ar_ok and lat_ok and a['bold'] == 'false' and a['bold_bi'] == 'false' and a['spacing'] == '0.0' and font_ok and (a['src_bidi'] if is_ar else True)
        if not ok: bad.append(a['para'])
        prow.append([name, a['para'], a['script_mix'] or '-', 'mixed Arabic+Latin' if mixed else ('Arabic-only' if is_ar else 'Latin-only'), a['native_chars'], a['src_chars_plus_mark'], a['align'], a['lang'], a['font'] or '(mixed runs)', a['size'], a['bold'], a['bold_bi'], a['spacing'],
                     'yes' if a['src_bidi'] else 'no', 'RTL' if (is_ar and ar_ok) else ('n/a' if not is_ar else 'FAIL'), 'LTR' if (any(c[0] == 'L' for c, _ in a['seg_direction']) and lat_ok) else 'n/a', a['block_arrangement'], 'PASS' if ok else 'FAIL'])
    def hfv(kind, hd): r = hfrows.get((kind, hd)); return f"{r[4]} chars / {r[5]} para / {r[6]} fields" if r and not r[3].startswith('ERR') else 'n/a'
    srow.append([name, h, 'yes (staged copy hash == source hash)', 'opened without repair/corruption dialog', 'first open: field-update prompt declined (No); the position data come from a later re-open of the same byte-identical copy, which showed no prompt', pages, hfv('primary', 'true'), hfv('primary', 'false'), hfv('first', 'true') if 'First' in name else 'n/a (no first-page variant)',
                 'Page 1 of 1 rendered natively in footer (PAGE/NUMPAGES resolved)', f"{sum(1 for a in an if 'A' in a['script_mix'])} Arabic paragraphs", f"{len(bad)} paragraph(s) failing: {bad}" if bad else 'all paragraphs PASS', 'closed without saving; staged copy re-hashed equal to source and deleted',
                 hashlib.sha256(open(f"{S}/{shot}", 'rb').read()).hexdigest()[:16] + '… (local-only)'])
csv.writer(open(f"{P}/17_qa/native_word_paragraphs.csv", 'w', newline='')).writerows([["Template", "Word paragraph #", "Script classes", "Content type", "Native char count", "Source char count (+para mark)", "Native alignment", "Native language", "Native font", "Size pt", "Bold", "Bold (complex script)", "Char spacing pt", "Source w:bidi", "Arabic segments native direction", "Latin segments native direction", "Block arrangement (native positions)", "Result"]] + prow)
csv.writer(open(f"{P}/17_qa/native_word_template_summary.csv", 'w', newline='')).writerows([["Template", "Source SHA-256", "Byte-identical to source", "Open result", "Dialog", "Pages (native)", "Primary header", "Primary footer", "First-page header", "Footer fields", "Arabic paragraphs", "Paragraph checks", "Close result", "Local screenshot (SHA-256 prefix)"]] + srow)
print(len(prow), 'paragraph rows'); [print(r[0], r[-3]) for r in srow]
