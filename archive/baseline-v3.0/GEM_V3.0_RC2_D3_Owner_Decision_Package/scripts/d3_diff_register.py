"""Writes 11_QA_Evidence/d3a_diff_register.csv from the apply log (candidate diff control). Usage: d3_diff_register.py <pkg_dir>"""
import sys,json,csv
P=sys.argv[1];L=json.load(open(P+'/11_QA_Evidence/d3a_apply_log.json'))
with open(P+'/11_QA_Evidence/d3a_diff_register.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['ID','Document','Slide/page','Shape','XML part','Before','After','Authority','Visible change?','Notes-only?','Original (base) hash','Candidate hash'])
    for e in L['edits']:
        d=L['decks']['A' if e['document']=='Part A' else 'C'];vis='Yes' if (e['document']=='Part C' or e['id']=='D3B') else 'No'
        w.writerow([e['id'],e['document'],f"slide {e['slide']}",e['shape'],e['part'],e['before'],e['after'],e['authority'],vis,'Yes' if vis=='No' else 'No',d['src_sha256'],d['dst_sha256']])
    c=L['c3'];w.writerow(['C3','Part D checksum list','3-line list','n/a','n/a (text file)',c['removed_line'][:12]+'…  SHA256SUMS.txt (self-entry)','removed (2 lines remain)','only 1 of 10 repository checksum lists self-lists','No','n/a',c['src_sha256'],c['dst_sha256']])
    for n in L['notes']: w.writerow(['C4',n['source'],'line 3'+(' and 48' if n['occurrences_replaced']==2 else ''),'n/a','n/a (Markdown)','SYNCHRONIZED · SYSTEM READY — EVIDENCE GATES REMAIN','SYNCHRONIZED · NOT RELEASED · EVIDENCE GATES REMAIN',"no deck uses SYSTEM READY; NOT RELEASED is the decks' edition-state wording",'No','n/a',n['src_sha256'],n['dst_sha256']])
print('diff register rows written')
