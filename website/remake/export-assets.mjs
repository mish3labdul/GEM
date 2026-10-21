import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const require = createRequire(import.meta.url);
const sharp = require(process.env.SHARP_MODULE || 'sharp');
const root = path.join(path.dirname(fileURLToPath(import.meta.url)), 'assets');
const source = path.join(root, 'source');
const out = path.join(root, 'exports');
fs.mkdirSync(out, {recursive: true});
const hash = buffer => crypto.createHash('sha256').update(buffer).digest('hex');
const records = [];
for (const [kind, widths] of [['desktop', [640, 960, 1280]], ['mobile', [640, 960]]]) {
  const input = path.join(source, `hero-${kind}-source.png`);
  for (const width of widths) {
    const name = `hero-${kind}-${width}.webp`;
    await sharp(input).resize({width, withoutEnlargement: true}).webp({quality: 86, effort: 6}).toFile(path.join(out, name));
    const data = fs.readFileSync(path.join(out, name));
    records.push({file: name, classification: 'AI-generated concept render; not production photography',
      source: path.relative(root, input), sourceSha256: hash(fs.readFileSync(input)),
      sha256: hash(data), bytes: data.length, width, height: (await sharp(data).metadata()).height});
  }
}
for (const product of ['shampoo', 'conditioner', 'body-wash', 'body-lotion', 'hand-wash']) {
  const input = path.join(source, product + '-source.png');
  const name = product + '-source.webp';
  await sharp(input).webp({lossless: true, effort: 6}).toFile(path.join(out, name));
  const data = fs.readFileSync(path.join(out, name));
  const original = await sharp(input).ensureAlpha().raw().toBuffer();
  const encoded = await sharp(data).ensureAlpha().raw().toBuffer();
  if (original.length !== encoded.length) throw Error('Pixel dimensions changed: ' + product);
  let changedVisiblePixels = 0;
  for (let i = 0; i < original.length; i += 4) {
    if (original[i + 3] && (original[i] !== encoded[i] || original[i+1] !== encoded[i+1] ||
      original[i+2] !== encoded[i+2] || original[i+3] !== encoded[i+3])) changedVisiblePixels++;
  }
  if (changedVisiblePixels) throw Error('Source artwork changed: ' + product);
  const metadata = await sharp(data).metadata();
  records.push({file: name, width: metadata.width, height: metadata.height, classification: 'Original Part D slide 4 concept study in lossless web encoding; not production artwork',
    source: path.relative(root, input), sourceSha256: hash(fs.readFileSync(input)),
    sha256: hash(data), bytes: data.length, changedVisiblePixels});
}
for (const format of ['room', 'wall', 'travel']) {
  const input = path.join(source, `format-${format}-source.png`);
  for (const width of [480, 960]) {
    const name = `format-${format}-${width}.webp`;
    await sharp(input).resize({width}).webp({quality: 86, effort: 6}).toFile(path.join(out, name));
    const data = fs.readFileSync(path.join(out, name));
    records.push({file: name, width, height: Math.round(width * 2 / 3),
      classification: 'AI-generated unlabelled concept render; counts, hardware, materials and compatibility unapproved',
      source: path.relative(root, input), sourceSha256: hash(fs.readFileSync(input)), sha256: hash(data), bytes: data.length});
  }
}
const staticFiles = fs.readdirSync(path.join(root,'static')).map(file => {
  const data = fs.readFileSync(path.join(root,'static',file));
  return {file, sha256: hash(data), bytes: data.length, classification: 'Pinned original identity/font/license/social resource; artwork and rights gates unchanged'};
});
for (const record of records) {
  const max = record.file.includes('-source.webp') ? 1600000 : 200000;
  if(record.bytes > max) throw Error('Asset exceeds documented byte budget: '+record.file);
}
fs.writeFileSync(path.join(root, 'manifest.json'), JSON.stringify({revision: 'M3-R1',
  sourceRevision: '5a9ab1e887300063f23c2d5bd884f4ac486ce80d',
  budget: {heroExportMaxBytes: 200000, productLosslessMaxBytes: 1600000,
    formatExportMaxBytes: 200000,
    scope: 'M2 measured budgets retained; original labelled artwork uses lossless encoding to preserve visible pixels.'},
  staticFiles, files: records}, null, 2) + '\n');
console.log(JSON.stringify(records.map(({file, bytes, changedVisiblePixels}) => ({file, bytes, changedVisiblePixels})), null, 2));
