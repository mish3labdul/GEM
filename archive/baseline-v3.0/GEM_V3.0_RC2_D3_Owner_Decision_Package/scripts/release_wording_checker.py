"""Context-aware release-wording checker (D3 QA). FAILS only on wording that claims the current GEM system / edition / package IS
APPROVED, RELEASED, FINAL, SYSTEM READY or PRODUCTION READY without qualifying context. Markdown emphasis is stripped first;
PowerPoint text is taken per paragraph (python-pptx joins split runs), so run splitting cannot hide or fake a match.
Allowed: negated or pending uses ("NOT RELEASED", "RELEASED is not permitted"), the word as a concept/field label ("RELEASE STATUS: HOLD · CONDITIONAL RELEASE · RELEASED",
"A RELEASED state is blocked while…"), release authorization/sequence, "no item is released", "released assets must…"."""
import re
BAN_ALWAYS=re.compile(r'\b(SYSTEM READY|PRODUCTION READY)\b')
CLAIM_WORD=r'(APPROVED|RELEASED|FINAL|SYSTEM READY|PRODUCTION READY)'
SUBJ=r'(GEM|V3\.0|RC2|[Ee]cosystem|[Ss]ystem|[Ee]dition|[Pp]ackage|[Cc]andidate|[Bb]rand [Gg]uidelines)'   # system-level subjects only; per-item status labels (e.g. "PART A · APPROVED") are not system claims
CLAIM=re.compile(rf'\b{SUBJ}\b[^.;|]{{0,60}}?(\bis\b|\bare\b|\bnow\b|—|:|=|·)\s*{CLAIM_WORD}\b')   # case-sensitive: status tokens are upper-case; "Final Release Notes" is a title
NEG=re.compile(r'\b(not|no|never|nor|none|without|until|cannot|pending|blocked|unless|before|while|prohibited|forbidden|banned|must not|until|if)\b|\bun(?:released|approved)\b',re.I)
CONCEPT=re.compile(r'RELEASE STATUS:|CONDITIONAL RELEASE|A RELEASED state|RELEASED state|release authori[sz]ation|Release form|released assets?|APPROVED / CONDITIONAL|status vocabulary|status classes|Approved V3\.0',re.I)
def strip_md(t): return re.sub(r'[*_`]+','',t)
def violations(text):
    out=[]
    for ln,line in enumerate(strip_md(text).splitlines(),1):
        for seg in re.split(r'(?<=[.;!?])\s+',line):
            if BAN_ALWAYS.search(seg) and not NEG.search(seg): out.append((ln,seg.strip()[:160],'unqualified SYSTEM/PRODUCTION READY'))
            elif CLAIM.search(seg) and not NEG.search(seg) and not CONCEPT.search(seg):
                m=CLAIM.search(seg)
                if re.fullmatch(r'(?i)not\s*',seg[max(0,m.start()-4):m.start()]): continue
                out.append((ln,seg.strip()[:160],'claims current state'))
    return out
