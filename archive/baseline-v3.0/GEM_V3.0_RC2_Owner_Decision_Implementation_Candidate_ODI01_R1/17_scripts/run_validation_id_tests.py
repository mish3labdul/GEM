"""Runs the regression fixture for validation_id_checker. Usage: run_validation_id_tests.py <fixture.json> <results.json>. Exit 1 on any failure."""
import sys,json,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from validation_id_checker import scan_text
fx=json.load(open(sys.argv[1]));res=[];bad=0
for grp in ('positive','negative'):
    for c in fx[grp]:
        f=scan_text(c['text']);verdict='FAIL' if any(x['verdict']=='FAIL' for x in f) else 'ALLOW'
        want='ALLOW' if grp=='positive' else 'FAIL';ok=verdict==want;bad+=not ok
        res.append(dict(group=grp,text=c['text'],expected=want,actual=verdict,result='PASS' if ok else 'FAIL',classes=[x['kind'] for x in f if x['id']==18 or x['kind']=='UNKNOWN_ID']))
out=dict(total=len(res),passed=len(res)-bad,failed=bad,results=res);json.dump(out,open(sys.argv[2],'w'),indent=1,ensure_ascii=False)
for r in res: print(r['result'],r['group'],'|',r['text'],'->',r['actual'],r['classes'])
print(f"{out['passed']}/{out['total']} PASS");sys.exit(1 if bad else 0)
