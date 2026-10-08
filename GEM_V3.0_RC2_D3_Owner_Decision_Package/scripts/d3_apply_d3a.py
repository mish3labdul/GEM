"""D3A implementation: C1–C4 as controlled CANDIDATE copies. Authoritative originals are never opened for writing.
Base for decks = current ODI01-R1 candidates (so accepted D4/D5/D6 work is kept); base for notes = current originals (Final Release Notes: the ODI01-R1 D6 candidate, so D6 + C4 are combined).
Zip-level exact text replacement: every other zip member is copied byte-for-byte.
Usage: d3_apply_d3a.py <repo_root> <out_dir> <log_json>"""
import sys,os,re,json,glob,zipfile,hashlib
root,out,logp=sys.argv[1:4]
sha=lambda b:hashlib.sha256(b).hexdigest()
R1=root+'/GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/'
LOG=[]
def edit_deck(src,dst,edits,tag):
    zin=zipfile.ZipFile(src);data={i.filename:zin.read(i.filename) for i in zin.infolist()};new=dict(data)
    for cid,part,old,newt,slide,auth in edits:
        x=new[part].decode('utf-8');assert x.count(old)==1,(cid,part,x.count(old))
        new[part]=x.replace(old,newt).encode('utf-8')
        LOG.append(dict(id=cid,document=tag,slide=slide,part=part,before=old,after=newt,authority=auth,part_sha256_before=sha(data[part]),part_sha256_after=sha(new[part])))
    with zipfile.ZipFile(dst,'w') as zo:
        for i in zin.infolist():
            zi=zipfile.ZipInfo(i.filename,i.date_time);zi.compress_type=i.compress_type;zi.external_attr=i.external_attr;zo.writestr(zi,new[i.filename])
    z2=zipfile.ZipFile(dst);ch=[n for n in data if z2.read(n)!=data[n]]
    return dict(src=src,dst=dst,src_sha256=sha(open(src,'rb').read()),dst_sha256=sha(open(dst,'rb').read()),parts_changed=ch)
A=[p for p in glob.glob(R1+'deck_candidates/*Part A*.pptx')][0];C=[p for p in glob.glob(R1+'deck_candidates/*Part C*.pptx')][0]
D={}
D['A']=edit_deck(A,os.path.join(out,'deck_candidates','GEM Brand Guidelines V3.0 — Part A — RC2 — D3 CANDIDATE (UNAPPROVED).pptx'),[
 ('C1','ppt/notesSlides/notesSlide80.xml',"Part B's document ID is applied through its patch specification until its source is regenerated.","Part B is issued as its own RC2 deck with a token package (PartB_RC2/05_release); its component bundle does not yet exist (VAL-13, VAL-20).",79,'Part B RC2 deck, PDF and token package exist (PartB_RC2/05_release); Part B cover and slide 34 carry document ID GEM-DDS-V3.0-RC2; component bundle absent (open evidence register VAL-13, VAL-20, OD-SRC)'),
 ('C1','ppt/notesSlides/notesSlide79.xml',"Part B is the Digital Design System V3.0 (RC2 patch specification issued; PDF regeneration pending its source).","Part B is the Digital Design System V3.0, issued as Release Candidate 2 with a token package; its component bundle is pending (VAL-13, VAL-20).",80,'same as above')],'Part A')
D['C']=edit_deck(C,os.path.join(out,'deck_candidates','GEM Production Standards V3.0 — Part C — RC2 — D3 CANDIDATE (UNAPPROVED).pptx'),[
 ('C2','ppt/slides/slide44.xml',"Layout follows Part A. Print process and stock follow the print and materials standards. Templates are an OPEN DELIVERABLE (AB10, AB11, W01–W10): none exists yet.","Layout follows Part A. Print process and stock follow the print and materials standards. Templates are an OPEN DELIVERABLE (AB10, AB11, W01–W10): a Letterhead Set (Application Revision 03) exists as a WORKING APPLICATION / PENDING VALIDATION; no template is accepted.",44,'GEM_Letterhead_Set_v1.1_Application_Revision_03 exists in main; its 8 templates carry "WORKING APPLICATION / PENDING VALIDATION"; no acceptance recorded (Register AB10/AB11/W-rows are scope decisions, OD-TPL open); slide 44 table already shows Letterhead [PENDING PRODUCTION MASTER]')],'Part C')
# ---- C4 notes
SR=[('qa','GEM_V3_RC2_Release_Notes.md',root+'/qa/GEM_V3_RC2_Release_Notes.md'),('03_qa','GEM_V3_RC2_Release_Notes.md',root+'/GEM_V3_RC2/03_qa/GEM_V3_RC2_Release_Notes.md'),('qa','GEM_V3_RC2_Final_Release_Notes.md',R1+'partd/qa__GEM_V3_RC2_Final_Release_Notes.ODI01-R1-D6-CANDIDATE.md')]
NOTES=[]
for folder,name,src in SR:
    t=open(src,encoding='utf-8').read();n=t.count('SYSTEM READY — EVIDENCE GATES REMAIN');assert n>=1,src
    t2=t.replace('SYNCHRONIZED · SYSTEM READY — EVIDENCE GATES REMAIN','SYNCHRONIZED · NOT RELEASED · EVIDENCE GATES REMAIN')
    assert 'SYSTEM READY' not in t2,src
    dn=f"{folder}__{name[:-3]}.D3-CANDIDATE.md";dst=os.path.join(out,'notes_candidates',dn);open(dst,'w',encoding='utf-8').write(t2)
    NOTES.append(dict(id='C4',source=os.path.relpath(src,root),candidate=dn,occurrences_replaced=n,src_sha256=sha(open(src,'rb').read()),dst_sha256=sha(open(dst,'rb').read()),base='ODI01-R1 D6 candidate (D6 + C4 combined)' if 'D6' in src else 'current original'))
# ---- C3
pd=root+'/Amenities_Portfolio_PartD_RC2/04_release/SHA256SUMS.txt'
lines=open(pd,encoding='utf-8').read().splitlines();keep=[l for l in lines if not l.endswith('  SHA256SUMS.txt')];assert len(lines)==3 and len(keep)==2
dst=os.path.join(out,'checksum_candidates','PartD_04_release_SHA256SUMS.D3-CANDIDATE.txt');open(dst,'w',encoding='utf-8').write('\n'.join(keep)+'\n')
C3=dict(id='C3',source=os.path.relpath(pd,root),candidate=os.path.basename(dst),removed_line=[l for l in lines if l.endswith('  SHA256SUMS.txt')][0],src_sha256=sha(open(pd,'rb').read()),dst_sha256=sha(open(dst,'rb').read()))
json.dump(dict(edits=LOG,decks=D,notes=NOTES,c3=C3),open(logp,'w'),indent=1,ensure_ascii=False)
print({k:v['parts_changed'] for k,v in D.items()},[n['occurrences_replaced'] for n in NOTES])
