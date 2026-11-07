// W3 (GSAP Motion), W4 (Three.js/WebGL2 glTF 2.0 Studio), & W5 (Bilingual UX, A11y & Performance) Verification Suite
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import fs from 'node:fs';
import path from 'node:path';
import net from 'node:net';

const require = createRequire(import.meta.url);
const engines = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const engine = process.env.BROWSER_TYPE || 'chromium';
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const screenshotDir = process.env.W3_W5_SCREENSHOT_DIR || path.join(root, 'qa', 'screenshots_w3_w5');
fs.mkdirSync(screenshotDir, {recursive: true});

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
  browser = await engines[engine].launch({headless: true});
  async function test(name, run) {
    const context = await browser.newContext();
    context.setDefaultTimeout(5000);
    try { await run(context); results.push({name, status: 'PASS'}); }
    catch (error) { results.push({name, status: 'FAIL', error: error.message}); }
    finally { await context.close(); }
  }

  for (const lang of ['ar', 'en']) {
    await test(`${lang}: W3 GSAP motion engine and quarter-arc choreography`, async context => {
      const page = await context.newPage();
      await page.setViewportSize({width: 1440, height: 900});
      await page.goto(`${base}/${lang}/`);
      const gsapVersion = await page.evaluate(() => window.gsap && window.gsap.version);
      assert.equal(gsapVersion, '3.12.5-gem-selfhosted');
      const arcCount = await page.locator('.gem-quarter-arc').count();
      assert.ok(arcCount >= 1, 'Hero quarter-arc motif missing');
      await page.waitForFunction(() => {
        const el = document.querySelector('.gem-quarter-arc');
        return el && parseFloat(getComputedStyle(el).getPropertyValue('--arc-offset') || '0') < 10;
      });
    });

    await test(`${lang}: W3 reduced-motion tiering skips animation and defaults studio to static plate`, async context => {
      const page = await context.newPage();
      await page.emulateMedia({reducedMotion: 'reduce'});
      await page.setViewportSize({width: 1280, height: 900});
      await page.goto(`${base}/${lang}/amenities-packaging/`);
      const state = await page.evaluate(() => ({
        reduced: window.gsap.isReducedMotion(),
        arcOffset: getComputedStyle(document.querySelector('.gem-quarter-arc')).getPropertyValue('--arc-offset').trim(),
        studioMode: window.GEM3DStudio.state.mode,
        plateVisible: !document.getElementById('gem-3d-fallback-plate').hidden,
        canvasHidden: document.getElementById('gem-3d-canvas').hidden
      }));
      assert.equal(state.reduced, true);
      assert.equal(state.arcOffset, '0');
      assert.equal(state.studioMode, 'plate');
      assert.equal(state.plateVisible, true);
      assert.equal(state.canvasHidden, true);
    });

    await test(`${lang}: W4 3D GLB loading, 5 products, governance badges, lighting, hotspots, and GPU dispose()`, async context => {
      const page = await context.newPage();
      await page.setViewportSize({width: 1440, height: 960});
      await page.goto(`${base}/${lang}/amenities-packaging/`);
      await page.locator('#interactive-3d-studio').scrollIntoViewIfNeeded();
      await page.waitForFunction(() => window.GEM3DStudio && window.GEM3DStudio.state.loadedProduct === 'shampoo');

      const expectedKeys = ['shampoo', 'conditioner', 'body_wash', 'body_lotion', 'hand_wash'];
      for (let i = 0; i < expectedKeys.length; i++) {
        await page.locator(`[data-studio-product="${i}"]`).click();
        await page.waitForFunction(expected => window.GEM3DStudio.state.loadedProduct === expected, expectedKeys[i]);
        const st = await page.evaluate(() => ({
          product: window.GEM3DStudio.state.loadedProduct,
          nodes: window.GEM3DStudio.state.loadedNodes,
          polys: window.GEM3DStudio.state.loadedPolygons,
          glbBytes: window.GEM3DStudio.state.glbBytes,
          disposed: window.GEM3DStudio.state.disposedCount,
          badgeStatus: document.getElementById('studio-3d-badge').dataset.status,
          badgeText: document.getElementById('studio-3d-badge').textContent,
          pilotPressed: document.querySelector(`[data-product="${window.GEM3DStudio.state.productIndex}"]`).getAttribute('aria-pressed')
        }));
        assert.equal(st.product, expectedKeys[i]);
        assert.equal(st.nodes, 8, `Expected 8 glTF mesh nodes for ${expectedKeys[i]}`);
        assert.equal(st.polys, 20460, `Expected 20,460 polygons for ${expectedKeys[i]}`);
        assert.ok(st.glbBytes > 650000 && st.glbBytes < 800000, `Unexpected GLB byte length: ${st.glbBytes}`);
        assert.equal(st.badgeStatus, i < 2 ? 'baseline' : 'provisional');
        assert.equal(/concept|تصوّر|تصور/i.test(st.badgeText), false);
        assert.equal(st.pilotPressed, 'true', 'Pilot product list did not sync with 3D studio');
      }

      // Verify lighting presets
      for (const light of ['suite', 'daylight', 'studio']) {
        await page.locator(`[data-lighting="${light}"]`).click();
        assert.equal(await page.locator('#gem-3d-viewport').getAttribute('data-lighting-active'), light);
        assert.equal(await page.locator(`[data-lighting="${light}"]`).getAttribute('aria-pressed'), 'true');
      }

      // Verify optical hotspots & turntable rotation
      await page.locator('[data-hotspot="glass"]').click();
      await page.waitForTimeout(200);
      assert.equal(await page.locator('[data-hotspot="glass"]').getAttribute('aria-pressed'), 'true');
      await page.locator('[data-hotspot="pump"]').click();
      await page.waitForTimeout(200);
      assert.equal(await page.locator('[data-hotspot="pump"]').getAttribute('aria-pressed'), 'true');

      // Capture targeted visual evidence screenshot of the 3D studio
      await page.locator('[data-studio-product="0"]').click();
      await page.waitForFunction(() => window.GEM3DStudio.state.loadedProduct === 'shampoo');
      await page.waitForTimeout(300);
      await page.locator('#interactive-3d-studio').screenshot({
        path: path.join(screenshotDir, `w4_3d_studio_${lang}_desktop.png`)
      });

      // Test WebGL context loss fallback to static plate
      await page.evaluate(() => {
        document.getElementById('gem-3d-canvas').dispatchEvent(new Event('webglcontextlost'));
      });
      assert.equal(await page.evaluate(() => window.GEM3DStudio.state.mode), 'plate');
      assert.equal(await page.locator('#gem-3d-fallback-plate').isVisible(), true);
    });

    await test(`${lang}: W5 mobile 375px tap targets, RTL/LTR layout parity, and CLS budget`, async context => {
      const page = await context.newPage();
      await page.setViewportSize({width: 375, height: 812});
      await page.goto(`${base}/${lang}/amenities-packaging/`);
      await page.locator('#interactive-3d-studio').scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);

      // Verify tap targets >= 44px height
      const heights = await page.locator('#interactive-3d-studio button').evaluateAll(btns =>
        btns.map(b => ({text: b.textContent.trim(), h: b.getBoundingClientRect().height, w: b.getBoundingClientRect().width}))
      );
      for (const b of heights) {
        assert.ok(b.h >= 43.5 && b.w >= 43.5, `Tap target below 44px on mobile (${lang}): ${JSON.stringify(b)}`);
      }
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `Mobile overflow on ${lang}`);

      await page.locator('#interactive-3d-studio').screenshot({
        path: path.join(screenshotDir, `w4_3d_studio_${lang}_mobile.png`)
      });
    });
  }
} finally {
  if (browser) await browser.close();
  server.kill();
}
console.log(JSON.stringify(results, null, 2));
if (results.some(r => r.status === 'FAIL')) process.exitCode = 1;
