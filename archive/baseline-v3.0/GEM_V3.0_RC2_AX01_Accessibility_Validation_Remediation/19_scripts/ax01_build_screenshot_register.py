"""AX01 local screenshot register (metadata only): repo-relative filename, document, slide, purpose, SHA-256, Local-only = YES, D7 restriction = PENDING. Usage: ax01_build_screenshot_register.py <repo_root> <package_dir_name>"""
import os, re, csv, sys, hashlib
root, pk = sys.argv[1:3]; D = f"{root}/{pk}/local_only/screenshots"; sh = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); rows = []
KEY = {'A': 'Part A', 'B': 'Part B', 'C': 'Part C', 'D': 'Part D', 'Drest': 'Part D'}
for f in sorted(os.listdir(D)):
    if not f.endswith('.png'): continue
    m = re.match(r'(Drest|[ABCD])_(before|after)_slide(\d+)\.png', f)
    if m: doc, slide, pur = KEY[m.group(1)] + (' (source candidate)' if m.group(2) == 'before' else ' (AX01 candidate)'), str(int(m.group(3))), 'Native PowerPoint slide capture (' + m.group(2) + ' remediation; pixel-compare pair)'
    elif f.startswith('pilot') or f.startswith('decpilot'): doc, slide, pur = 'Part A pilot', re.sub(r'\D', '', f.split('slide')[-1]) if 'slide' in f else '', 'Native capture for a remediation pilot (title mapping / decorative marking)'
    elif f.startswith('var_'): doc, slide, pur = 'Part A slide 1 title-mapping XML variant', '1', 'Native capture of an XML variant used to diagnose a heading shift'
    else: doc, slide, pur = 'AX01 comparison sheet', '', 'Before/after/difference visual (' + f + ')'
    rows.append([f"{pk}/local_only/screenshots/{f}", doc, slide, pur, sh(f"{D}/{f}"), 'YES', 'PENDING'])
csv.writer(open(f"{root}/{pk}/18_AX01_Local_Screenshot_Register.csv", 'w', newline='', encoding='utf8')).writerows([["Screenshot filename (repo-relative path)", "Document", "Slide / page", "Purpose", "SHA-256", "Local-only?", "D7 restriction"]] + rows)
print(len(rows), 'screenshots registered')
