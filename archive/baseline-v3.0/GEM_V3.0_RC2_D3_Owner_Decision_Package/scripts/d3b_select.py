"""D3B owner decision (STREAM = BRAND): promote the BRAND mapping to SELECTED, mark the Logo mapping NOT SELECTED, add the final disposition to the semantic test.
Idempotent. No source file is touched; no asset-ID or checksum rule is created. Usage: d3b_select.py <pkg_dir>"""
import sys,os,csv,re
P=sys.argv[1]
def rd(f): return list(csv.reader(open(os.path.join(P,f),encoding='utf-8')))
def wr(f,rows): csv.writer(open(os.path.join(P,f),'w',newline='',encoding='utf-8')).writerows(rows)
SEL='D3B_X12_Selected_BRAND_Mapping.csv'
# ---- status columns on the two comparison mappings
for f,status in (('05_D3B_X12_BRAND_Mapping.csv','COMPARISON STAGE — superseded by '+SEL+' (same names; BRAND is the SELECTED controlled stream)'),('06_D3B_X12_Logo_Mapping.csv','NOT SELECTED — historical comparison evidence only; not a valid controlled mapping')):
    r=rd(f)
    if r[0][-1]!='Selection status':
        r[0].append('Selection status');[x.append(status) for x in r[1:]];wr(f,r)
# ---- selected mapping
r=rd('05_D3B_X12_BRAND_Mapping.csv');h=r[0];ix={k:i for i,k in enumerate(h)}
ATTEST_ASSET={'Horizontal'};GOV_COL={'Black','Ink','Beige','White'}
out=[['Current source filename','Controlled X12 filename','STREAM','ASSET','VARIANT','Version','Date','Source rename required?','Manifest-only?','Taxonomy confidence','Notes','Source path (unchanged)','SHA-256 of source']]
for x in r[1:]:
    if x[ix['STREAM']]=='': continue   # metrics.json row: not a mapped asset
    asset,var=x[ix['ASSET']],x[ix['VARIANT']]
    col_only=var in GOV_COL;asset_ok=asset in ATTEST_ASSET
    notes=[]
    notes.append('ASSET "Horizontal" is attested only by the Part A slide 75 example; no enumerated ASSET list exists (REQUIRES TAXONOMY CONFIRMATION)' if asset_ok else f'ASSET "{asset}" is the kit\'s shape word, not an enumerated governed ASSET value — REQUIRES TAXONOMY CONFIRMATION')
    notes.append(f'VARIANT "{var}" is a governed palette colour name; the variant list is not enumerated' if col_only else f'VARIANT "{var}" combines the colour with the kit\'s own qualifier (clearspace 2u / pixel size) — REQUIRES TAXONOMY CONFIRMATION')
    conf='MODERATE — tokens attested by the Part A example / governed palette names' if (asset_ok and col_only) else 'LOW — REQUIRES TAXONOMY CONFIRMATION'
    out.append([x[ix['Source filename (unchanged)']],x[ix['Controlled name — exact X12 pattern']],'BRAND',asset,var,'X.Y (placeholder; version undecided)','YYYYMMDD (placeholder; manifest issue date undecided)','NO','YES',conf,'; '.join(notes)+'. Controlled-name mapping for the manifest (VAL-16); the source file keeps its name.',x[ix['Source path (unchanged)']],x[ix['SHA-256 of source']]])
wr(SEL,out);print('selected rows',len(out)-1)
# ---- semantic test final disposition
s=rd('07_D3B_X12_Semantic_Test.csv')
if not any(x[0].startswith('FINAL DISPOSITION') for x in s):
    s.append(['FINAL DISPOSITION (owner decision 2026-10-09)','BRAND — SELECTED','Logo — NOT SELECTED','OWNER DECISION informed by the governing taxonomy (Part A slide 75 folder rule; Register X02 "01 Brand Masters") and semantic consistency (no STREAM/ASSET duplication). The criteria above are the prior state and are preserved unchanged.','BRAND (owner decision)','Owner decision — not an evidence tally'])
    s.append(['DECISION BASIS AND REMAINING CONFLICT','The Part A slide 75 example using Logo is treated as a synchronization defect in the example (corrected in a controlled candidate: STREAM only).','Logo remains part of the decision history; it is not the governing STREAM token.','Criteria 2, 3 and 13 (example vs rule, internal contradiction) are retained as the documented conflict; the owner resolved it in favour of the rule. No authoritative enumeration of STREAM or ASSET tokens exists; ASSET taxonomy confirmation remains open.','BRAND (owner decision)','Owner decision — conflict stays documented'])
    wr('07_D3B_X12_Semantic_Test.csv',s)
