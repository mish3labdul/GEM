import fs from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const origin=process.env.HUB_URL;
assert.ok(origin?.startsWith('https://'),'Set HUB_URL to an HTTPS deployment');
const manifest=JSON.parse(fs.readFileSync('dist/manifest.json'));
const artifact=JSON.parse(fs.readFileSync('dist/artifact-hashes.json'));
const failures=[];let checked=0;
// Pages canonicalizes /index.html to /, then applies the Arabic redirect.
const queue=artifact.files.filter(f=>!['_headers','_redirects','index.html'].includes(f.path));
async function checkFile(file){
 const r=await fetch(new URL(file.path,origin));assert.equal(r.status,200,file.path);
 assert.match(r.headers.get('x-robots-tag')||'',/noindex/,file.path);
 const bytes=Buffer.from(await r.arrayBuffer());
 assert.equal(createHash('sha256').update(bytes).digest('hex'),file.sha256,file.path);
 checked++;
}
await Promise.all(Array.from({length:6},async()=>{while(queue.length){const file=queue.shift();try{await checkFile(file);}catch(e){failures.push({path:file.path,error:e.message});}}}));
const root=await fetch(origin,{redirect:'manual'});
assert.equal(root.status,302);assert.equal(new URL(root.headers.get('location'),origin).pathname,'/ar/');
assert.match(root.headers.get('x-robots-tag')||'',/noindex/);
let originals=0;
for(const d of manifest.documents){
 const r=await fetch(d.originalUrl);assert.equal(r.status,200);
 assert.equal(createHash('sha256').update(Buffer.from(await r.arrayBuffer())).digest('hex'),d.originalSha256);
 originals++;
}
console.log(JSON.stringify({origin,hostedFilesChecked:checked,originalDownloadsChecked:originals,rootArabicRedirect:true,failures,artifactManifestSha256:createHash('sha256').update(fs.readFileSync('dist/artifact-hashes.json')).digest('hex')},null,2));
if(failures.length)process.exitCode=1;
