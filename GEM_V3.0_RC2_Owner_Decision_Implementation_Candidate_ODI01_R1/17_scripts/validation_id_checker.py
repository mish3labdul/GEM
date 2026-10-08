"""ODI01-R1 structured validation-ID checker.
Rules
 * Allocated IDs are VAL-01..VAL-21 except VAL-18. Any other VAL-nn is an UNKNOWN ID -> FAIL.
 * VAL-18 is INTENTIONALLY UNALLOCATED. A sentence that mentions it is classified:
     EXPLANATORY  (says it is unallocated / not allocated / absent / an ID gap)  -> allowed
     ACTIVE       (gives it an owner, status, evidence, dependency, closure, release condition, approval, gate or pass/fail state) -> FAIL
     UNCLASSIFIED (neither)                                                      -> FAIL (conservative)
   A sentence is split at . ; ! ? and at brackets; each piece that names VAL-18 is judged on its own.
   Negated phrases ("no owner", "carries no release condition") are removed before the ACTIVE test, but only when the sentence is also EXPLANATORY.
Public API: scan_text(text) -> list of findings; check_files(paths) -> (ids_seen, findings)."""
import re
ALLOCATED=set(range(1,22))-{18}
EXPLAIN=re.compile(r'(?ix)\b(?:un-?allocated|not\ allocated|not\ an\ allocated|intentionally\ (?:un)?allocated|(?:is|remains|stays|are)\ (?:intentionally\ )?(?:un)?allocated|no\ VAL-18|ID\ 18\b|numbering\ gap|does\ not\ exist|not\ used|never\ allocated|except\ VAL-18|excluding\ VAL-18|other\ than\ VAL-18|not\ (?:been\ )?(?:created|assigned|issued)|is\ absent)')
NEG=re.compile(r'(?i)\b(?:no|not|without|never|nor|neither|has\ no|carries\ no)\s+(?:an?\s+)?(?:\w+\s+){0,2}?(?:owners?|status|evidence|dependenc\w+|closure|release|approval|gate|pass|fail|condition)\b')
ACTIVE=re.compile(r'(?i)\b(?:owners?|status|evidence|depends?|depend\w+|dependency|clos(?:e|es|ed|ure)|release|approv\w+|gate|gates|implement\w*|pass(?:es|ed)?|fail(?:s|ed)?|open|blocked|blocks|required|requires|must|before|deadline|due|assigned|sign-?off|accepted|complete[sd]?)\b')
def sentences(line):
    """Sentences, then parenthetical segments: text inside / outside brackets is judged separately, so an unrelated word in a parenthesis cannot taint (or excuse) the clause that names the ID."""
    out=[]
    for s in re.split(r'(?<=[.;!?])\s+',line):
        out+=[x for x in re.split(r'[()]',s) if x.strip()]
    return out
def classify(sentence):
    s=sentence
    exp=bool(EXPLAIN.search(s));rest=NEG.sub(' ',s) if exp else s
    # remove the explanatory phrase itself before the active test
    rest=EXPLAIN.sub(' ',rest)
    act=bool(ACTIVE.search(re.sub(r'VAL-\d+','',rest)))
    if act: return 'ACTIVE'
    return 'EXPLANATORY' if exp else 'UNCLASSIFIED'
def scan_text(text,source=''):
    out=[]
    for ln,line in enumerate(text.splitlines(),1):
        ids=[int(x) for x in re.findall(r'VAL-(\d+)',line)]
        if not ids: continue
        for i in ids:
            if i!=18 and i not in ALLOCATED: out.append(dict(source=source,line=ln,id=i,kind='UNKNOWN_ID',verdict='FAIL',text=line.strip()[:160]))
        if 18 in ids:
            for s in sentences(line):
                if 'VAL-18' not in s and 'ID 18' not in s: continue
                k=classify(s);out.append(dict(source=source,line=ln,id=18,kind=k,verdict='ALLOW' if k=='EXPLANATORY' else 'FAIL',text=s.strip()[:160]))
        for i in set(ids):
            if i in ALLOCATED: out.append(dict(source=source,line=ln,id=i,kind='ALLOCATED',verdict='ALLOW',text=''))
    return out
def check_files(paths):
    seen=set();bad=[];expl=[]
    for p in paths:
        for f in scan_text(open(p,encoding='utf-8').read(),p.split('/')[-1]):
            seen.add(f['id'])
            if f['verdict']=='FAIL': bad.append(f)
            elif f['id']==18: expl.append(f)
    return sorted(seen),bad,expl
