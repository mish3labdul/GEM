"""Native Microsoft Word (Mac) test harness: open -> edit -> save as -> close -> reopen -> export PDF -> close.
Usage: python wtest.py <template_dir> <out_dir> [jobs-filter]"""
import subprocess, sys, time, json
from pathlib import Path

STORIES = '{main text story, primary header story, first page header story, primary footer story, first page footer story}'

LAT = [
    ('[DATE]', '8 October 2026'),
    ('[REFERENCE NUMBER]', 'GEM/QA-2026/0001-ABCDEFGHIJ-LONG-REFERENCE'),
    ('[RECIPIENT NAME]', 'Dr Alexandra Example-Longname'),
    ('[RECIPIENT ORGANIZATION]', 'Example Hospitality Procurement and Administrative Review Organisation (QA ONLY)'),
    ('[ORGANIZATION]', 'Example Hospitality Procurement and Administrative Review Organisation (QA ONLY)'),
    ('[ADDRESS]', 'Building 0, Example Street, Example District'),
    ('[CITY]', 'Example City'), ('[COUNTRY]', 'Example Country'), ('[POSTAL CODE]', '00000'),
    ('[T]', 'T +000 00 000 0000'), ('[E]', 'E qa@example.invalid'), ('[W]', 'W https://example.invalid'),
    ('[SIGNATORY NAME]', 'Alexandra Example-Signatory'), ('[TITLE]', 'Head of Example Procurement (QA ONLY)'),
    ('Request for supplier information and product documentation',
     'Request for supplier information and product documentation and clarification of supporting evidence for procurement review and subsequent internal assessment (QA ONLY)'),
    ('Formal correspondence regarding the proposed review',
     'Formal correspondence regarding the proposed review of supporting evidence, procurement documentation and subsequent internal assessment (QA ONLY)'),
]
AR = [
    ('«اسم المستلم»', 'السيد مثال الاختبار'),
    ('«اسم الجهة»', 'شركة مثال للضيافة والمشتريات والمراجعة الإدارية (للاختبار فقط)'),
    ('«العنوان»', 'العنوان: مبنى 0 · البريد qa@example.invalid · الهاتف +000 00 000 0000 · https://example.invalid'),
    ('«اسم الموقّع»', 'مثال الموقّع'), ('«المسمى الوظيفي»', 'مدير المشتريات (للاختبار فقط)'),
]
EN_P = 'QA ONLY flow paragraph. Please identify verified information and any documents requiring further review. This paragraph tests automatic pagination and signature-block stability.'
AR_P = 'فقرة للاختبار فقط. يرجى تحديد المعلومات المؤكدة والوثائق التي تحتاج إلى مراجعة إضافية، وتختبر هذه الفقرة تدفق الصفحات وثبات كتلة التوقيع.'

TEMPLATES = {
    'English_First_Page': dict(repl=LAT, anchor='confirm a supplier relationship.', para=EN_P, n2=9, n3=22),
    'Executive': dict(repl=LAT, anchor='contractual commitment.', para=EN_P, n2=9, n3=22),
    'Minimal': dict(repl=LAT, anchor='confirm a supplier relationship.', para=EN_P, n2=9, n3=22),
    'Arabic_First_Page': dict(repl=LAT + AR, anchor='التزاماً تعاقدياً.', para=AR_P, n2=12, n3=30),
    'Bilingual_First_Page': dict(repl=LAT + AR, anchor='requiring further validation.', para=EN_P, n2=9, n3=24),
    'English_Continuation': dict(repl=LAT, anchor=None),
    'Arabic_Continuation': dict(repl=LAT + AR, anchor=None),
    'Bilingual_Continuation': dict(repl=LAT + AR, anchor=None),
}


def q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


GETDOC = '''set {v} to missing value
repeat 90 times
  try
    set {v} to active document
    set nm_ to name of {v}
    exit repeat
  end try
  delay 1
end repeat'''


HF = [('primary header story', '[REFERENCE NUMBER]', 'GEM/QA-2026/0001-ABCDEFGHIJ-LONG-REFERENCE'),
      ('primary footer story', '[E]', 'E qa@example.invalid'), ('first page footer story', '[E]', 'E qa@example.invalid'),
      ('primary footer story', '[W]', 'W https://example.invalid'), ('first page footer story', '[W]', 'W https://example.invalid')]


def script(src, out, pdf, repl=(), flow=None, explicit=None):
    L = ['with timeout of 900 seconds', 'tell application "Microsoft Word"', 'open POSIX file ' + q(str(src)), GETDOC.format(v='d')]
    for f, r in repl:
        L.append('execute find (find object of (text object of d)) find text %s replace with %s replace replace all' % (q(f), q(r)))
    if repl:
        for story, f, r in HF:
            L += ['try', 'set rr to get story range d story type ' + story,
                  'execute find (find object of rr) find text %s replace with %s replace replace all' % (q(f), q(r)), 'end try']
    if flow or explicit:
        anchor, para, n = flow or explicit
        L += ['set fo to find object of selection',
              'execute find fo find text %s wrap find find stop' % q(anchor),
              'collapse range (text object of selection) direction collapse end']
        if flow:
            L.append('type text selection text (' + ' & '.join(['return & ' + q(para)] * n) + ')')
        else:
            for _ in range(n):
                L += ['type text selection text (character id 12)', 'type text selection text ' + q(para)]
    L += ['save as d file name %s file format format document' % q(str(out)), 'close d saving no',
          'open POSIX file ' + q(str(out)), GETDOC.format(v='d2'),
          'save as d2 file name %s file format format PDF' % q(str(pdf)), 'close d2 saving no', 'end tell', 'end timeout']
    return '\n'.join(L)


def run(src, out, pdf, **kw):
    p = Path(out).with_suffix('.applescript')
    p.write_text(script(src, out, pdf, **kw), encoding='utf-8')
    t = time.time()
    r = subprocess.run(['osascript', str(p)], capture_output=True, text=True, timeout=1200)
    return {'rc': r.returncode, 'err': (r.stderr or '').strip()[:300], 'seconds': round(time.time() - t)}


def jobs(tdir, odir):
    for name, cfg in TEMPLATES.items():
        src = Path(tdir) / f'GEM_Letterhead_{name}.docx'
        yield f'{name}__open', src, dict()
        yield f'{name}__fields', src, dict(repl=cfg['repl'])
        if cfg.get('anchor'):
            a, p = cfg['anchor'], cfg['para']
            yield f'{name}__flow2', src, dict(repl=cfg['repl'], flow=(a, p, cfg['n2']))
            yield f'{name}__flow3', src, dict(repl=cfg['repl'], flow=(a, p, cfg['n3']))
            yield f'{name}__explicit3', src, dict(repl=cfg['repl'], explicit=(a, p, 2))


if __name__ == '__main__':
    tdir, odir = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    flt = sys.argv[3] if len(sys.argv) > 3 else ''
    odir.mkdir(parents=True, exist_ok=True)
    log = odir / 'word_jobs.json'
    res = json.loads(log.read_text()) if log.exists() else {}
    for jid, src, kw in jobs(tdir, odir):
        if flt not in jid or res.get(jid, {}).get('rc') == 0:
            continue
        res[jid] = run(src, odir / f'{jid}.docx', odir / f'{jid}.pdf', **kw)
        print(jid, res[jid], flush=True)
        log.write_text(json.dumps(res, indent=1, ensure_ascii=False))
