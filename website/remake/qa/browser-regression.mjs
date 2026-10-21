// Requires an existing Playwright installation. No packages are installed by this script.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import net from 'node:net';

const require = createRequire(import.meta.url);
const engines = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const engine = process.env.BROWSER_TYPE || 'chromium';
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const socket = net.createServer();
await new Promise(resolve => socket.listen(0, '127.0.0.1', resolve));
const port = socket.address().port;
await new Promise(resolve => socket.close(resolve));
const base = `http://127.0.0.1:${port}`;
const server = spawn('python3', [path.join(root, 'serve.py'), '--port', String(port)], {stdio: 'pipe'});
let browser;
const results = [];
try {
  for (let attempt = 0; ; attempt++) {
    try { await fetch(base); break; }
    catch (error) {
      if (attempt === 49) throw error;
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  browser = await engines[engine].launch({headless: true,
    ...(process.env.BROWSER_EXECUTABLE || process.env.CHROMIUM_EXECUTABLE ? {executablePath: process.env.BROWSER_EXECUTABLE || process.env.CHROMIUM_EXECUTABLE} : {})});
  async function test(name, run) {
    const context = await browser.newContext();
    context.setDefaultTimeout(2500);
    try { await run(context); results.push({name, status: 'PASS'}); }
    catch (error) { results.push({name, status: 'FAIL', error: error.message}); }
    finally { await context.close(); }
  }
  for (const lang of ['ar', 'en']) {
    await test(`${lang}: mobile menu keyboard and escape focus`, async context => {
      const page = await context.newPage();
      await page.setViewportSize({width: 320, height: 900});
      await page.goto(`${base}/${lang}/`);
      const toggle = page.locator('.menu-toggle');
      await toggle.focus();
      await page.keyboard.press('Enter');
      assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
      await page.keyboard.press('Tab');
      assert.equal(await page.locator('#navigation a').first().evaluate(el => el === document.activeElement), true);
      await page.keyboard.press('Escape');
      assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
      assert.equal(await toggle.evaluate(el => el === document.activeElement), true);
    });
    await test(`${lang}: forced colours and reduced motion controls`, async context => {
      const page = await context.newPage();
      await page.emulateMedia({forcedColors: 'active', reducedMotion: 'reduce'});
      await page.goto(`${base}/${lang}/amenities-packaging/`);
      await page.locator('[data-product="3"]').focus();
      await page.keyboard.press('Space');
      assert.equal(await page.locator('[data-product="3"]').getAttribute('aria-pressed'), 'true');
      const outline = await page.locator('[data-product="3"]').evaluate(el => getComputedStyle(el).outlineStyle);
      assert.notEqual(outline, 'none');
      for (const img of await page.locator('.format-art img').all()) {
        await img.scrollIntoViewIfNeeded();
        await img.evaluate(el => el.decode());
      }
      assert.equal(await page.locator('.format-art').count(), 3);
    });
    await test(`${lang}: blocked script cannot submit brief`, async context => {
      const page = await context.newPage();
      await page.route('**/app.js', route => route.abort());
      const navigation = [];
      page.on('request', request => { if (request.isNavigationRequest()) navigation.push(request.url()); });
      await page.goto(`${base}/${lang}/contact/`);
      assert.equal(await page.locator('button[type=submit]').isDisabled(), true,
        'Prepare must be disabled until the local handler is installed');
      // A direct native submit must also be blocked by the document policy.
      await page.evaluate(() => {
        window.blockedDirectives = [];
        document.addEventListener('securitypolicyviolation', event => window.blockedDirectives.push(event.effectiveDirective));
        try { document.querySelector('form').submit(); }
        catch { /* Firefox also throws an unnamed exception; verify the policy event below. */ }
      });
      await page.waitForFunction(() => window.blockedDirectives.includes('form-action'));
      await page.waitForTimeout(150);
      assert.equal(navigation.length, 1, 'A native submit caused a network navigation');
    });
    for (const font of ['arabic', 'jost', 'inter']) {
      await test(`${lang}: missing ${font} font fails visibly`, async context => {
        const page = await context.newPage();
        await page.route(`**/${font}.woff2`, route => route.abort());
        await page.goto(`${base}/${lang}/`);
        await page.evaluate(() => document.fonts.ready);
        assert.equal(await page.locator('html').evaluate(el => el.classList.contains('font-error')),
          true, 'Missing font was silently replaced');
        assert.equal(await page.locator('.font-failure').isVisible(), true);
      });
    }
    await test(`${lang}: local brief, validation, edit, reset and download`, async context => {
      const page = await context.newPage();
      await page.goto(`${base}/${lang}/contact/`);
      const sent = [];
      page.on('request', request => {
        if (request.method() !== 'GET' || ['document', 'xhr', 'fetch'].includes(request.resourceType())) {
          sent.push(request.url());
        }
      });
      await page.locator('button[type=submit]').click();
      assert.equal(await page.locator('#brief-result').isVisible(), false);
      for (const [id, value] of Object.entries({name: 'اختبار QA <&>', company: 'Demo',
        email: 'qa@example.test', market: 'الرياض', message: 'موجز اختبار <&> فقط'})) {
        await page.locator(`#${id}`).fill(value);
      }
      await page.locator('#interest').selectOption('1');
      await page.locator('button[type=submit]').click();
      assert.equal(await page.locator('#brief-result').isVisible(), true);
      assert.match(await page.locator('#brief-text').inputValue(), /اختبار QA <&>/);
      const download = page.waitForEvent('download');
      await page.locator('#download-brief').click();
      assert.equal((await download).suggestedFilename(), `GEM-project-brief-${lang}.txt`);
      await page.locator('#name').fill('Changed');
      assert.equal(await page.locator('#brief-result').isVisible(), false);
      await page.locator('button[type=reset]').click();
      assert.equal(await page.locator('#name').inputValue(), '');
      assert.equal(await page.locator('#brief-text').inputValue(), '');
      assert.deepEqual(sent, [], 'Brief operation caused a network request');
    });
    await test(`${lang}: clipboard denial leaves a selectable local brief`, async context => {
      await context.addInitScript(() => Object.defineProperty(navigator, 'clipboard', {
        value: {writeText: async () => { throw new Error('Clipboard denied for test'); }}
      }));
      const page = await context.newPage();
      await page.goto(`${base}/${lang}/contact/`);
      for (const [id, value] of Object.entries({name:'QA',company:'Demo',email:'qa@example.test',market:'Riyadh',message:'Local test'})) await page.locator('#'+id).fill(value);
      await page.locator('#interest').selectOption('1');
      await page.locator('[type=submit]').click();
      await page.locator('#copy-brief').click();
      const state=await page.locator('#brief-text').evaluate(el => ({focused:document.activeElement===el,selected:el.selectionEnd-el.selectionStart,length:el.value.length}));
      assert.equal(state.focused,true);
      assert.equal(state.selected,state.length);
      const labels=await page.locator('#page-data').evaluate(el=>JSON.parse(el.textContent).form);
      assert.equal(await page.locator('#form-status').textContent(),labels.copyFailed);
    });
  }
  for (const lang of ['ar', 'en']) {
    await test(`${lang}: pilot foundation corrections`, async context => {
      const page = await context.newPage();
      await page.setViewportSize({width: 375, height: 1000});
      await page.goto(`${base}/${lang}/amenities-packaging/#concept-formats`);
      assert.ok(await page.locator('.logo img').evaluate(el => el.getBoundingClientRect().width) >= 120,
        'Mobile lockup is below the documented minimum');
      const target = lang === 'ar' ? 'en' : 'ar';
      assert.equal(await page.locator('.site-footer .language').evaluate(el => new URL(el.href).pathname + new URL(el.href).hash),
        `/${target}/amenities-packaging/#concept-formats`);
      for (const selector of ['.logo', '.site-footer .footer-logo']) {
        assert.ok(await page.locator(selector).evaluate(el => el.getBoundingClientRect().height) >= 44,
          `${selector} target is too short`);
      }
      await page.goto(`${base}/${lang}/contact/`);
      const contrast = await page.locator('#name').evaluate(el => {
        const values = getComputedStyle(el).borderTopColor.match(/[\d.]+/g).map(Number);
        const alpha = values[3] ?? 1;
        const c = values.slice(0, 3).map(v => (v * alpha + 255 * (1 - alpha)) / 255)
          .map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
        return 1.05 / (c.reduce((sum, v, i) => sum + v * [.2126, .7152, .0722][i], 0) + .05);
      });
      assert.ok(contrast >= 3, `Essential border contrast is ${contrast}`);
    });
    await test(`${lang}: pilot product image and mobile state agree`, async context => {
      const page = await context.newPage();
      await page.setViewportSize({width: 375, height: 1000});
      await page.goto(`${base}/${lang}/amenities-packaging/`);
      const names = await page.locator('#page-data').evaluate(el => JSON.parse(el.textContent).products);
      for (const [index, filename] of ['shampoo', 'conditioner', 'body-wash', 'body-lotion', 'hand-wash'].map((name, i) => [i, name + '-source.webp'])) {
        await page.locator(`[data-product="${index}"]`).click();
        assert.equal(await page.locator('#product-image').isVisible(), true);
        assert.ok((await page.locator('#product-image').getAttribute('src')).endsWith(filename));
        assert.equal(await page.locator('#pilot-selected-name').textContent(), names[index]);
        await page.locator('#product-image').evaluate(img => img.decode());
        assert.ok(await page.locator('#product-image').evaluate(img => img.naturalWidth > 0));
      }
      const buttons = page.locator('[data-product]');
      await buttons.nth(2).focus();
      await page.keyboard.press('Enter');
      assert.equal(await buttons.nth(2).getAttribute('aria-pressed'), 'true');
      assert.equal(await page.locator('#product-name').textContent(), names[2]);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    });
    await test(`${lang}: responsive hero artwork loads`, async context => {
      const page = await context.newPage();
      for (const width of [375, 1440]) {
        await page.setViewportSize({width, height: 1000});
        await page.goto(`${base}/${lang}/`);
        const picture = page.locator('.hero picture img');
        await picture.evaluate(img => img.decode());
        assert.match(await picture.evaluate(img => img.currentSrc),
          width < 761 ? /hero-mobile/ : /hero-desktop/);
        assert.equal(await picture.evaluate(img => img.naturalWidth > 0), true);
      }
    });
  }
  await test('all routes and three widths', async context => {
    const page = await context.newPage();
    for (const lang of ['ar', 'en']) for (const slug of ['', 'about/', 'amenities-packaging/', 'contact/', 'privacy/']) {
      for (const width of [320, 375, 1440]) {
        await page.setViewportSize({width, height: 900});
        const response = await page.goto(`${base}/${lang}/${slug}`);
        await page.evaluate(() => document.fonts.ready);
        assert.ok([200, 304].includes(response.status()), `Unexpected route status: ${response.status()}`);
        assert.equal(await page.locator('main h1').count(), 1);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false,
          `Overflow: ${lang}/${slug} at ${width}`);
        assert.equal(await page.locator('.font-failure').isVisible(), false);
      }
    }
  });
} finally {
  if (browser) await browser.close();
  server.kill();
}
console.log(JSON.stringify(results, null, 2));
if (results.some(result => result.status === 'FAIL')) process.exitCode = 1;
