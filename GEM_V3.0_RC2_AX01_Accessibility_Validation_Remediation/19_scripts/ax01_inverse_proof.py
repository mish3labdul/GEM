"""AX01 proof that the Part A/B/C candidates differ from their sources ONLY by the decorative flag and the table header flag: undo exactly those two edits in every changed member and compare byte-for-byte with the source.
(Part D additionally carries title placeholders with pinned line spacing; covered by static content verification and native pixel comparison.) Usage: ax01_inverse_proof.py <repo_root> <package_dir>"""
import sys, os, re, json, zipfile
sys.path.insert(0, os.path.dirname(__file__)); from ax01_common import *
root, pkg = sys.argv[1:3]
EXT = r'<a:extLst><a:ext uri="\{C183D7F6-B498-43B3-948B-1728B52AA6E4\}"><adec:decorative xmlns:adec="http://schemas.microsoft.com/office/drawing/2017/decorative" val="1"/></a:ext></a:extLst>'
inv = lambda x: re.sub(r'(<p:cNvPr id="\d+" name="[^"]*")>' + EXT + '</p:cNvPr>', r'\1/>', x).replace('<a:tblPr firstRow="1"/>', '<a:tblPr/>')
res = {}
for key in 'ABC':
    label, path, _ = DECKS[key]; cand = [f for f in os.listdir(f"{pkg}/21_candidate_corrections") if f"Part {key} " in f and f.endswith('.pptx')][0]
    zs, zd = zipfile.ZipFile(f"{root}/{path}"), zipfile.ZipFile(f"{pkg}/21_candidate_corrections/{cand}"); ok, bad, n = 0, [], 0
    for m in zs.namelist():
        a, b = zs.read(m), zd.read(m)
        if a == b: continue
        n += 1
        if inv(b.decode()) == a.decode(): ok += 1
        else: bad.append(m)
    res[label] = dict(members_changed=n, reproduced_by_inverse_transform=ok, not_reproduced=bad)
json.dump(res, open(f"{pkg}/20_qa/ax01_inverse_proof.json", 'w'), indent=1); print(res)
