"""Static content/link assertions plus optional local HTTP smoke check."""
from html.parser import HTMLParser
from pathlib import Path
import argparse
import json
import urllib.request
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent / 'dist'
parser = argparse.ArgumentParser()
parser.add_argument('--http', action='store_true', help='Smoke-test the noindex preview server')
parser.add_argument('--base-url', default='http://127.0.0.1:4173')
parser.add_argument('--origin', default='', help='Expected HTTPS origin for production output')
args = parser.parse_args()
origin = args.origin.rstrip('/')
if origin:
    parsed = urlsplit(origin)
    assert parsed.scheme == 'https' and parsed.netloc and not parsed.path and not parsed.query and not parsed.fragment
assert not (origin and args.http), '--http checks preview headers; use separately from production --origin'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.h1 = 0
        self.descriptions = []
        self.social = []
        self.canonical = []
        self.alternates = []
        self.robots = []
        self.og_url = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'a':
            self.links.append(a.get('href', ''))
        if tag == 'h1':
            self.h1 += 1
        if tag == 'meta' and a.get('name') == 'description':
            self.descriptions.append(a.get('content', ''))
        if tag == 'meta' and a.get('property') == 'og:image':
            self.social.append(a.get('content', ''))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a.get('href', ''))
        if tag == 'link' and a.get('rel') == 'alternate':
            self.alternates.append((a.get('hreflang'), a.get('href')))
        if tag == 'meta' and a.get('name') == 'robots':
            self.robots.append(a.get('content', ''))
        if tag == 'meta' and a.get('property') == 'og:url':
            self.og_url.append(a.get('content', ''))

pages = {}
for file in ROOT.rglob('index.html'):
    relative = file.parent.relative_to(ROOT).as_posix()
    route = '/' if relative == '.' else '/' + relative + '/'
    pages[route] = Page(file.read_text())
localized = {r: p for r, p in pages.items() if r != '/'}
assert len(localized) == 10
for route, page in localized.items():
    assert page.h1 == 1, route
    assert len(page.descriptions) == 1 and page.descriptions[0], route
    assert page.social == [origin + '/assets/social.png'], (route, 'og:image')
    assert page.robots == ['index,follow' if origin else 'noindex,nofollow'], (route, 'robots')
    if origin:
        slug = route.split('/', 2)[2]
        expected = [('ar', origin + '/ar/' + slug), ('en', origin + '/en/' + slug),
                    ('x-default', origin + '/ar/' + slug)]
        assert page.canonical == [origin + route], (route, 'canonical')
        assert sorted(page.alternates) == sorted(expected), (route, 'hreflang')
        assert page.og_url == [origin + route], (route, 'og:url')
    else:
        assert not page.canonical and not page.alternates and not page.og_url, route
    for href in page.links:
        target, _, fragment = href.partition('#')
        target = target or route
        if target.startswith('/'):
            assert target in pages, (route, target)
            assert not fragment or fragment in pages[target].ids, (route, href)
assert len({p.descriptions[0] for p in localized.values()}) == 10
assert (ROOT / 'assets/social.png').read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'
robots = (ROOT / 'robots.txt').read_text()
if origin:
    assert robots == f'User-agent: *\nAllow: /\nSitemap: {origin}/sitemap.xml\n'
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9',
          'x': 'http://www.w3.org/1999/xhtml'}
    entries = ET.parse(ROOT / 'sitemap.xml').getroot().findall('s:url', ns)
    assert len(entries) == 10
    assert {entry.findtext('s:loc', namespaces=ns) for entry in entries} == {origin + r for r in localized}
    for entry in entries:
        route = entry.findtext('s:loc', namespaces=ns)[len(origin):]
        assert sorted((a.get('hreflang'), a.get('href')) for a in entry.findall('x:link', ns)) == sorted(pages[route].alternates)
else:
    assert robots == 'User-agent: *\nDisallow: /\n'
    assert not (ROOT / 'sitemap.xml').exists()
if args.http:
    for route in localized:
        response = urllib.request.urlopen(args.base_url.rstrip('/') + route, timeout=5)
        assert response.status == 200, route
        assert response.headers.get('X-Robots-Tag') == 'noindex, nofollow'
    response = urllib.request.urlopen(args.base_url.rstrip('/') + '/', timeout=5)
    assert response.url.endswith('/ar/')
    assert urllib.request.urlopen(args.base_url.rstrip('/') + '/assets/social.png').status == 200
print(json.dumps({'mode': 'production' if origin else 'preview', 'localized_pages': 10, 'headings_metadata_links': 'PASS', 'social_png': 'PASS', 'robots_sitemap': 'PASS', 'http_preview': 'PASS' if args.http else 'not requested'}))
