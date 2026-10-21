"""Retrieve byte-exact brand assets; never imports previous website content."""
import base64
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).parent
REVISION = '5a9ab1e887300063f23c2d5bd884f4ac486ce80d'
ASSETS = {
    'brand/working-kit/logo/horizontal/svg/gem-horizontal-ink.svg': 'logo-ink.svg',
    'brand/working-kit/logo/horizontal/svg/gem-horizontal-white.svg': 'logo-white.svg',
    'website/site/assets/fonts/jost-latin-400-normal.woff2': 'jost.woff2',
    'website/site/assets/fonts/inter-latin-400-normal.woff2': 'inter.woff2',
    'website/site/assets/fonts/noto-sans-arabic-400.woff2': 'arabic.woff2',
    'website/site/assets/fonts/OFL-Jost.txt': 'OFL-Jost.txt',
    'website/site/assets/fonts/OFL-Inter.txt': 'OFL-Inter.txt',
    'website/site/assets/fonts/OFL-NotoSansArabic.txt': 'OFL-NotoSansArabic.txt',
}
for source, name in ASSETS.items():
    response = subprocess.check_output(['gh', 'api', f'repos/mish3labdul/GEM/contents/{source}?ref={REVISION}'])
    data = base64.b64decode(json.loads(response)['content'])
    destination = ROOT / 'assets' / 'static' / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    print(f'{name}: {len(data)} bytes')
