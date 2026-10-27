// Regenerates the raster favicon fallbacks and the branded share image from the supplied logo files.
// The share image is written as assets/static/social-rgb.png; reduce it to a 256-colour PNG (Pillow quantize) and save it as social.png,
// which matches the original's palette format and size, then delete social-rgb.png.
// Optional maintenance tool (needs an existing Playwright module via PLAYWRIGHT_MODULE); the build never runs it.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
const {chromium} = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || 'playwright');
const read = file => fs.readFileSync(path.join(root, file));
const uri = (file, type) => `data:${type};base64,${read(file).toString('base64')}`;
const symbol = uri('assets/static/favicon.svg', 'image/svg+xml');
const logo = uri('assets/static/logo-ink.svg', 'image/svg+xml');
const photo = uri('assets/source/social-photo-original.png', 'image/png');
const browser = await chromium.launch();
async function render(width, height, html, file, transparent = false) {
  const page = await browser.newPage({viewport: {width, height}, deviceScaleFactor: 1});
  await page.setContent(`<body style="margin:0">${html}</body>`);
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode())));
  fs.writeFileSync(path.join(root, file), await page.screenshot({omitBackground: transparent}));
  await page.close();
}
await render(32, 32, `<img src="${symbol}" width="32" height="32" style="display:block">`, 'assets/static/favicon-32.png', true);
await render(180, 180, `<div style="width:180px;height:180px;background:#F8F3EA;display:grid;place-items:center"><img src="${symbol}" width="116" height="116"></div>`, 'assets/static/apple-touch-icon.png');
await render(1200, 630, `<div style="position:relative;width:1200px;height:630px"><img src="${photo}" width="1200" height="630" style="display:block"><div style="position:absolute;left:0;right:0;bottom:0;height:92px;background:rgba(248,243,234,.92);display:flex;align-items:center;justify-content:center"><img src="${logo}" height="58"></div></div>`, 'assets/static/social-rgb.png');
await browser.close();
