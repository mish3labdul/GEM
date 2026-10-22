"""Select and label stakeholder derivatives without changing source documents.

Run after export comparison. Only the seven Arabic-bearing A/B pages use the
explicit-font-config LibreOffice fallback. Other pages retain native PowerPoint
rendering; the complete LibreOffice exports were rejected for artwork drift.
"""
from pathlib import Path
import hashlib
import shutil
from pypdf import PdfReader, PdfWriter

root=Path(__file__).resolve().parent
for letter,name in [('a','BrandGuidelines'),('b','DigitalDesignSystem'),('c','ProductionStandards'),('d','AmenitiesPackagingConcept')]:
    target=root/f'reading-copies/part-{letter}.pdf'
    native=root/f'native-exports/part-{letter}.pdf'
    native.parent.mkdir(exist_ok=True)
    if not native.exists():shutil.copyfile(target,native)
    reader=PdfReader(native)
    writer=PdfWriter()
    arabic_pages={'a':[37,38,39,65,66,68],'b':[9]}.get(letter,[])
    fallback=PdfReader(root/f'lo-fonts-trial/GEM_BRAND_{name}_Part{letter.upper()}_v3.0_20261009.pdf') if arabic_pages else None
    for index,page in enumerate(reader.pages,1):
        writer.add_page(fallback.pages[index-1] if index in arabic_pages else page)
    writer.add_metadata({'/Title':f'GEM Part {letter.upper()} V3.0 — Stakeholder reading copy — 2026-10-22','/Subject':'Complete stakeholder reading derivative; not an original V3.0 release artifact. Source qualifications retained. No production approval.','/Author':'GEM','/Keywords':'Stakeholder reading copy, source V3.0, export 2026-10-22'})
    with target.open('wb') as stream:writer.write(stream)
    print(letter,len(reader.pages),hashlib.sha256(target.read_bytes()).hexdigest())
