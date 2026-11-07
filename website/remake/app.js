(()=>{
 'use strict';
 const data=JSON.parse(document.getElementById('page-data').textContent);
 const lang=document.body.dataset.lang;
 const menu=document.querySelector('.menu-toggle');
 const nav=document.getElementById('navigation');
 const setMenu=open=>{menu.setAttribute('aria-expanded',String(open));menu.firstChild.textContent=open?data.close:data.menu;nav.classList.toggle('open',open);};
 menu.addEventListener('click',()=>setMenu(menu.getAttribute('aria-expanded')!=='true'));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){setMenu(false);menu.focus();}});
 document.querySelectorAll('.language').forEach(a=>{if(location.hash)a.hash=location.hash;});
 document.querySelectorAll('[data-product]').forEach(button=>button.addEventListener('click',()=>{
  const i=Number(button.dataset.product);
  document.querySelectorAll('[data-product]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  const numStr='0'+(i+1);
  document.getElementById('product-name').textContent=data.products[i];
  document.getElementById('product-detail').textContent=data.details[i];
  const activeIdx=document.getElementById('product-active-index');
  if(activeIdx)activeIdx.textContent=numStr;
  const subEl=document.getElementById('product-subtitle');
  if(subEl&&data.subtitles&&data.subtitles[i])subEl.textContent=data.subtitles[i];
  const counterEl=document.getElementById('collection-counter');
  if(counterEl)counterEl.textContent=numStr+' / 05';
  const stageCap=document.getElementById('stage-bottle-caption');
  if(stageCap){
   stageCap.textContent='';
   stageCap.append(document.createTextNode(data.products[i]+' · '));
   const numSpan=document.createElement('span');
   numSpan.className='num';numSpan.lang='en';numSpan.dir='ltr';
   numSpan.textContent=numStr+' / 05';
   stageCap.append(numSpan);
  }
  const image=document.getElementById('product-image');
  if(image){
   const file=['shampoo','conditioner','body-wash','body-lotion','hand-wash'][i]+'-source.webp';
   if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches){const cap=document.querySelector('.product-caption');image.classList.add('is-switching');if(cap)cap.classList.add('is-switching');setTimeout(()=>{image.classList.remove('is-switching');if(cap)cap.classList.remove('is-switching');},120);}
   image.src='/assets/'+file;
   image.alt=data.concept?data.products[i]+'. '+data.concept:data.products[i];
   document.querySelector('.product-visual')?.setAttribute('aria-label',(lang==='ar'?'تكبير صورة ':'Enlarge image of ')+data.products[i]);
   document.getElementById('pilot-selected-name').textContent=data.products[i];
  }
  if(window.GEMCollectionStage&&window.GEMCollectionStage.selectProduct)window.GEMCollectionStage.selectProduct(i,true);
 }));
 const form=document.getElementById('brief-form');
 if(form){
  const status=document.getElementById('form-status');
  const result=document.getElementById('brief-result');
  const output=document.getElementById('brief-text');
  form.addEventListener('submit',e=>{
   e.preventDefault();
   for(const el of form.querySelectorAll('input[required],textarea[required]')){el.setCustomValidity(el.value.trim()?'':data.form.error);}
   if(!form.reportValidity()){status.textContent=data.form.error;return;}
   const values=new FormData(form);
   const keys=['name','company','email','market'];
   const fields=keys.map(k=>data.form[k]+': '+String(values.get(k)).trim());
   fields.push(data.form.interest+': '+data.form.interestOptions[Number(values.get('interest'))]);
   fields.push('\n'+data.form.message+':\n'+String(values.get('message')).trim());
   output.value='GEM — '+data.form.output+'\n\n'+fields.join('\n');
   result.hidden=false;status.textContent=data.form.prepared;
   document.getElementById('brief-heading').focus();
  });
  form.addEventListener('input',e=>{if(e.target.setCustomValidity)e.target.setCustomValidity('');if(!result.hidden){result.hidden=true;output.value='';status.textContent='';}});
  form.addEventListener('reset',()=>{result.hidden=true;output.value='';status.textContent=data.form.cleared;form.querySelectorAll('input,textarea').forEach(el=>el.setCustomValidity(''));});
  document.getElementById('copy-brief').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(output.value);status.textContent=data.form.copied;}catch{output.focus();output.select();status.textContent=data.form.copyFailed;}});
  document.getElementById('download-brief').addEventListener('click',()=>{const blob=new Blob(['\ufeff'+output.value],{type:'text/plain;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='GEM-project-brief-'+lang+'.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent=data.form.downloaded;});
  // Enable preparation only after every local form handler is installed.
  form.querySelector('[type="submit"]').disabled=false;
  document.getElementById('brief-init').hidden=true;
  form.removeAttribute('aria-describedby');
 }
 // Both languages use all three fonts, including the language switch and signature.
 // A font that fails once is not refetched by the browser, so retry by loading a fresh FontFace; only a persistent failure shows the error.
 const requireFont=async(family,file,sample)=>{
  for(let attempt=0;attempt<3;attempt++){
   try{
    if(attempt===0){if((await document.fonts.load('16px '+family,sample)).length)return;}
    else{document.fonts.add(await new FontFace(family,"url('/assets/"+file+"') format('woff2')",{weight:'400',display:'block'}).load());return;}
   }catch{}
   if(attempt<2)await new Promise(resolve=>setTimeout(resolve,300*(attempt+1)));
  }
  throw Error('Required font missing: '+family);
 };
 Promise.all([requireFont('Arabic','arabic.woff2','العربية'),requireFont('Jost','jost.woff2','GEM'),requireFont('Inter','inter.woff2','GEM')]).catch(()=>{document.documentElement.classList.add('font-error');document.querySelector('.font-failure').hidden=false;});
 // Motion preview: smart header, scroll parallax, curtain reveals, zoom lightbox.
 // Every effect is skipped when the visitor prefers reduced motion.
 const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 const header=document.querySelector('.site-header');
 if(header){const bar=document.createElement('div');bar.className='scroll-horizon';bar.setAttribute('aria-hidden','true');header.appendChild(bar);}
 const visual=document.querySelector('.product-visual');
 if(visual){
  visual.setAttribute('data-zoom-hint',lang==='ar'?'اضغط للتكبير':'Click to inspect');
  visual.setAttribute('aria-label',(lang==='ar'?'تكبير صورة ':'Enlarge image of ')+data.products[0]);
 }
 if(!reducedMotion&&'IntersectionObserver' in window){
  document.documentElement.classList.add('js-motion');
  const targets=[...document.querySelectorAll('main section:not(.hero) .copy, .card, .principles > div, .audiences > div, .programmes > div, .formats > article, main section:not(.hero) figure')];
  targets.forEach((el,i)=>{el.setAttribute('data-reveal',el.tagName==='FIGURE'?'image':'text');el.style.setProperty('--reveal-delay',`${(i%3)*70}ms`);});
  const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target);}}),{threshold:.12,rootMargin:'0px 0px -40px 0px'});
  targets.forEach(el=>{if(el.getBoundingClientRect().top<innerHeight*.92)el.classList.add('is-visible');else io.observe(el);});
 }
 let lastY=scrollY,ticking=false;
 const hero=document.querySelector('.hero');
 const textures=[...document.querySelectorAll('.arc-banner img, .on-texture > .bg img')];
 const onScroll=()=>{
  const y=scrollY,max=Math.max(1,document.documentElement.scrollHeight-innerHeight);
  if(header){
   header.style.setProperty('--scroll-progress',(y/max).toFixed(4));
   header.classList.toggle('is-scrolled',y>36);
   const open=menu&&menu.getAttribute('aria-expanded')==='true';
   if(!reducedMotion&&!open&&y>220&&y>lastY+6)header.classList.add('is-hidden');
   if(reducedMotion||open||y<lastY-4||y<=220)header.classList.remove('is-hidden');
  }
  if(!reducedMotion){
   if(hero&&y<innerHeight*1.2){
    const p=Math.min(1,y/innerHeight);
    hero.style.setProperty('--hero-parallax',`${(y*.22).toFixed(1)}px`);
    hero.style.setProperty('--hero-scale',(1.03+p*.05).toFixed(4));
    hero.style.setProperty('--hero-copy-y',`${(y*-.08).toFixed(1)}px`);
   }
   textures.forEach(img=>{const r=img.parentElement.getBoundingClientRect();if(r.bottom>-100&&r.top<innerHeight+100)img.style.setProperty('--bg-parallax',`${(((r.top+r.height/2-innerHeight/2)/innerHeight)*-42).toFixed(1)}px`);});
  }
  lastY=y;ticking=false;
 };
 addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(onScroll);ticking=true;}},{passive:true});
 onScroll();
 const zoomables=[...document.querySelectorAll('#product-image, .format-art img, .split figure img')];
 if(zoomables.length){
  const lb=document.createElement('div');
  lb.className='gem-lightbox';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-hidden','true');
  lb.setAttribute('aria-label',lang==='ar'?'عرض الصورة':'Image preview');
  lb.setAttribute('aria-describedby','gem-lightbox-caption');
  lb.hidden=true;
  lb.innerHTML=`<button type="button" class="gem-lightbox-close">${lang==='ar'?'إغلاق ✕':'Close ✕'}</button><div class="gem-lightbox-inner"><p id="gem-lightbox-caption" class="gem-lightbox-caption"></p></div>`;
  document.body.appendChild(lb);
  const lbCap=lb.querySelector('.gem-lightbox-caption'),lbClose=lb.querySelector('.gem-lightbox-close');
  let lbImg=null;
  let trigger=null;
  const close=()=>{lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');lb.hidden=true;if(trigger)trigger.focus();};
  lbClose.addEventListener('click',close);
  lb.addEventListener('click',e=>{if(e.target===lb)close();});
  document.addEventListener('keydown',e=>{
   if(!lb.classList.contains('is-open'))return;
   if(e.key==='Escape')close();
   if(e.key==='Tab'){e.preventDefault();lbClose.focus();}
  });
  zoomables.forEach(img=>{
   let target=img.closest('.product-visual');
   if(!target){
    const media=img.closest('picture')||img;
    target=document.createElement('button');target.type='button';target.className='zoom-trigger';
    target.setAttribute('aria-label',(lang==='ar'?'تكبير الصورة: ':'Enlarge image: ')+(img.alt||''));
    media.replaceWith(target);target.appendChild(media);
   }
   const open=e=>{if(target===visual&&window.GEMCollectionStage&&window.GEMCollectionStage.wasDragged&&window.GEMCollectionStage.wasDragged()){e.preventDefault();return;}trigger=target;if(!lbImg)lbImg=document.createElement('img');lbImg.src=img.currentSrc||img.src;lbImg.alt=img.alt||'';lbCap.before(lbImg);lbCap.textContent=img.closest('figure')?.querySelector('figcaption')?.textContent||document.getElementById('product-name')?.textContent||img.alt||'';lb.hidden=false;lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');lbClose.focus();};
   target.addEventListener('click',open);
   if(target===visual)target.disabled=false;
  });
 }
})();

// Cookie notice strip: informational only, it does not gate the provider's security cookie. Closing is remembered for the browser session only.
(()=>{const n=document.querySelector('.cookie-notice');if(!n)return;try{if(sessionStorage.getItem('gem-cookie-notice')==='1'){n.hidden=true;return;}}catch(e){}const b=n.querySelector('.cookie-close');if(b)b.addEventListener('click',()=>{n.hidden=true;try{sessionStorage.setItem('gem-cookie-notice','1');}catch(e){}});})();

// ============================================================================
// W3: GSAP-Compatible Editorial Motion & Quarter-Arc Choreography Engine
// Self-hosted, zero-CDN, RTL-aware, strict prefers-reduced-motion compliance.
// ============================================================================
(()=>{
 'use strict';
 const isReduced=()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 const eases={
  'power3.out':t=>1-Math.pow(1-t,3),
  'power2.inOut':t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2,
  'linear':t=>t
 };
 function applyVars(target,vars){
  if(!target)return;
  const isEl=typeof Element!=='undefined'&&target instanceof Element;
  for(const [k,v] of Object.entries(vars)){
   if(['duration','delay','ease','onUpdate','onComplete','stagger','scrollTrigger'].includes(k))continue;
   if(isEl&&k.startsWith('--'))target.style.setProperty(k,String(v));
   else if(isEl&&k in target.style)target.style[k]=typeof v==='number'&&k!=='opacity'?`${v}px`:String(v);
   else target[k]=v;
  }
 }
 function tween(target,fromVars,toVars){
  const targets=typeof target==='string'?[...document.querySelectorAll(target)]:Array.isArray(target)?target:[target];
  const dur=isReduced()?0:((toVars.duration??0.75)*1000);
  const easeFn=eases[toVars.ease||'power3.out']||eases['power3.out'];
  if(fromVars)targets.forEach(t=>applyVars(t,fromVars));
  if(dur<=0){
   targets.forEach(t=>applyVars(t,toVars));
   if(toVars.onUpdate)toVars.onUpdate(1);
   if(toVars.onComplete)toVars.onComplete();
   return {kill(){},progress:()=>1};
  }
  let rafId=0,killed=false;
  const start=performance.now()+((toVars.delay||0)*1000);
  const initial=targets.map(t=>{
   const snap={};
   const isEl=typeof Element!=='undefined'&&t instanceof Element;
   for(const [k,v] of Object.entries(toVars)){
    if(typeof v==='number'&&!['duration','delay','stagger'].includes(k)){
     if(fromVars&&typeof fromVars[k]==='number')snap[k]=fromVars[k];
     else if(isEl&&k.startsWith('--'))snap[k]=parseFloat(getComputedStyle(t).getPropertyValue(k))||0;
     else if(!isEl&&typeof t[k]==='number')snap[k]=t[k];
     else snap[k]=0;
    }
   }
   return snap;
  });
  const tick=now=>{
   if(killed)return;
   if(now<start){rafId=requestAnimationFrame(tick);return;}
   const raw=Math.min(1,(now-start)/dur);
   const p=easeFn(raw);
   targets.forEach((t,idx)=>{
    const cur={};
    for(const [k,endVal] of Object.entries(toVars)){
     if(typeof endVal==='number'&&!['duration','delay','stagger'].includes(k)){
      const s=initial[idx][k]??0;
      cur[k]=s+(endVal-s)*p;
     }
    }
    applyVars(t,cur);
   });
   if(toVars.onUpdate)toVars.onUpdate(p);
   if(raw<1)rafId=requestAnimationFrame(tick);
   else if(toVars.onComplete)toVars.onComplete();
  };
  rafId=requestAnimationFrame(tick);
  return {kill(){killed=true;cancelAnimationFrame(rafId);},progress:()=>isReduced()?1:0.5};
 }
 const gsap={
  version:'3.12.5-gem-selfhosted',
  isReducedMotion:isReduced,
  set:(t,v)=>tween(t,null,{...v,duration:0}),
  to:(t,v)=>tween(t,null,v),
  fromTo:(t,f,v)=>tween(t,f,v),
  timeline(opts={}){
   const queue=[];
   const tl={
    to(t,v){queue.push(()=>tween(t,null,v));return tl;},
    fromTo(t,f,v){queue.push(()=>tween(t,f,v));return tl;},
    play(){queue.forEach(fn=>fn());if(opts.onComplete)opts.onComplete();return tl;}
   };
   setTimeout(()=>tl.play(),0);
   return tl;
  },
  registerPlugin(){return true;}
 };
 window.gsap=gsap;

 // Quarter-arc draw-in choreography on hero load
 const arcs=[...document.querySelectorAll('.gem-quarter-arc')];
 if(arcs.length){
  if(isReduced()){
   arcs.forEach(a=>a.style.setProperty('--arc-offset','0'));
  }else{
   arcs.forEach(a=>gsap.fromTo(a,{'--arc-offset':126},{'--arc-offset':0,duration:1.1,ease:'power3.out'}));
  }
 }
})();

// ============================================================================
// R2.4: Unobtrusive Collection Stage Motion & Three.js/WebGL Vessel Controller
// - Scroll-linked rotation (-16° to +14° across #pilot-products)
// - Damped pointer drag (±30° yaw, ±6° pitch) on #gem-collection-stage
// - Transparent alpha:true glTF 2.0 optical highlight/refraction layer
// - Zero technical HUD, zero lighting/mode widgets, full reduced-motion safety
// ============================================================================
(()=>{
 'use strict';
 const section=document.getElementById('pilot-products');
 const stage=document.getElementById('gem-collection-stage');
 if(!section||!stage)return;
 const canvas=document.getElementById('gem-stage-3d-canvas');
 const productImg=document.getElementById('product-image');
 const shadowEl=document.getElementById('stage-contact-shadow');
 const arcDot=document.getElementById('stage-arc-dot');
 const isReduced=()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches;

 const PRODUCTS=[
  {key:'shampoo',glb:'/assets/gem_shampoo.glb'},
  {key:'conditioner',glb:'/assets/gem_conditioner.glb'},
  {key:'body_wash',glb:'/assets/gem_body_wash.glb'},
  {key:'body_lotion',glb:'/assets/gem_body_lotion.glb'},
  {key:'hand_wash',glb:'/assets/gem_hand_wash.glb'}
 ];

 const state={
  productIndex:0,
  scrollYawDeg:0,
  dragYawDeg:0,
  dragPitchDeg:0,
  totalYawDeg:0,
  webglActive:false,
  contextLost:false,
  loadedProduct:null,
  loadedNodes:0,
  disposedCount:0,
  glbBytes:0
 };

 let gl=null,prog=null,meshes=[],labelTex=null,labelImgEl=null;
 let dragging=false,dragMoved=false,startX=0,startY=0,lastX=0,lastY=0;

 function disposeGPU(){
  if(gl){
   meshes.forEach(m=>{
    if(m.posBuf)gl.deleteBuffer(m.posBuf);
    if(m.normBuf)gl.deleteBuffer(m.normBuf);
    if(m.uvBuf)gl.deleteBuffer(m.uvBuf);
    if(m.idxBuf)gl.deleteBuffer(m.idxBuf);
   });
   if(labelTex){gl.deleteTexture(labelTex);labelTex=null;}
  }
  meshes=[];
  labelImgEl=null;
  state.disposedCount++;
 }

 function initGL(){
  if(!canvas||state.contextLost||isReduced())return false;
  if(gl)return true;
  try{
   gl=canvas.getContext('webgl2',{alpha:true,antialias:true,premultipliedAlpha:false})
    ||canvas.getContext('webgl',{alpha:true,antialias:true,premultipliedAlpha:false});
  }catch{}
  if(!gl)return false;
  const vsSrc=`
   precision highp float;
   attribute vec3 aPos;
   attribute vec3 aNorm;
   attribute vec2 aUV;
   uniform vec3 uTrans;
   uniform vec4 uQuat;
   uniform vec3 uScale;
   uniform float uYaw;
   uniform float uPitch;
   uniform float uAspect;
   varying vec3 vNorm;
   varying vec2 vUV;
   vec3 qrot(vec4 q, vec3 v){
    return v + 2.0 * cross(q.xyz, cross(q.xyz, v) + q.w * v);
   }
   void main(){
    vec3 p = qrot(uQuat, aPos * uScale) + uTrans;
    vec3 n = normalize(qrot(uQuat, aNorm));
    p.y -= 0.098;
    float cy = cos(uYaw), sy = sin(uYaw);
    vec3 py = vec3(p.x*cy + p.z*sy, p.y, -p.x*sy + p.z*cy);
    vec3 ny = vec3(n.x*cy + n.z*sy, n.y, -n.x*sy + n.z*cy);
    float cp = cos(uPitch), sp = sin(uPitch);
    vec3 pr = vec3(py.x, py.y*cp - py.z*sp, py.y*sp + py.z*cp);
    vec3 nr = vec3(ny.x, ny.y*cp - ny.z*sp, ny.y*sp + ny.z*cp);
    vNorm = normalize(nr);
    vUV = aUV;
    float zDist = 0.34 - pr.z;
    float fov = 2.42;
    gl_Position = vec4((pr.x * fov) / max(0.2, uAspect), pr.y * fov, (zDist - 0.34)*0.5, max(0.05, zDist));
   }
  `;
  const fsSrc=`
   precision mediump float;
   varying vec3 vNorm;
   varying vec2 vUV;
   uniform int uMatType;
   uniform sampler2D uLabelTex;
   uniform int uHasTex;
   void main(){
    vec3 N = normalize(vNorm);
    vec3 V = vec3(0.0, 0.0, 1.0);
    vec3 L = normalize(vec3(0.55, 0.58, 0.60));
    vec3 H = normalize(L + V);
    float diff = max(dot(N, L), 0.0);
    float fresnel = pow(1.0 - max(dot(N, V), 0.0), 3.0);
    float spec = pow(max(dot(N, H), 0.0), 84.0);
    vec3 col = vec3(0.18, 0.11, 0.05);
    float alpha = 0.0;
    if(uMatType == 1){
     col = mix(vec3(0.58, 0.26, 0.05), vec3(0.96, 0.84, 0.64), fresnel * 0.65 + spec * 0.85);
     alpha = clamp(fresnel * 0.42 + spec * 0.65, 0.0, 0.72);
    } else if(uMatType == 3 && uHasTex == 1){
     vec4 tex = texture2D(uLabelTex, vUV);
     col = tex.rgb * (0.35 + diff * 0.65);
     alpha = 0.28;
    } else if(uMatType == 0){
     col = vec3(0.10, 0.11, 0.13) + vec3(spec * 0.45);
     alpha = clamp(spec * 0.55, 0.0, 0.48);
    }
    gl_FragColor = vec4(col, alpha);
   }
  `;
  const compile=(type,src)=>{
   const s=gl.createShader(type);
   gl.shaderSource(s,src);
   gl.compileShader(s);
   return gl.getShaderParameter(s,gl.COMPILE_STATUS)?s:null;
  };
  const vs=compile(gl.VERTEX_SHADER,vsSrc);
  const fs=compile(gl.FRAGMENT_SHADER,fsSrc);
  if(!vs||!fs)return false;
  prog=gl.createProgram();
  gl.attachShader(prog,vs);
  gl.attachShader(prog,fs);
  gl.linkProgram(prog);
  if(!gl.getProgramParameter(prog,gl.LINK_STATUS))return false;
  state.webglActive=true;
  return true;
 }

 async function loadGLB(prodInfo){
  if(isReduced()||state.contextLost)return;
  disposeGPU();
  const res=await fetch(prodInfo.glb);
  if(!res.ok)throw new Error('GLB fetch failed');
  const buf=await res.arrayBuffer();
  state.glbBytes=buf.byteLength;
  const dv=new DataView(buf);
  if(dv.getUint32(0,true)!==0x46546C67)throw new Error('Invalid GLB');
  const jsonLen=dv.getUint32(12,true);
  const gltf=JSON.parse(new TextDecoder().decode(new Uint8Array(buf,20,jsonLen)));
  const binOffset=20+jsonLen+8;
  state.loadedProduct=prodInfo.key;
  state.loadedNodes=(gltf.nodes||[]).length;

  if(gltf.images&&gltf.images.length>0){
   const im=gltf.images[0];
   const bv=gltf.bufferViews[im.bufferView];
   const pngBytes=new Uint8Array(buf,binOffset+(bv.byteOffset||0),bv.byteLength);
   const blob=new Blob([pngBytes],{type:im.mimeType||'image/png'});
   const imgUrl=URL.createObjectURL(blob);
   const imgEl=new Image();
   await new Promise(r=>{imgEl.onload=r;imgEl.onerror=r;imgEl.src=imgUrl;});
   URL.revokeObjectURL(imgUrl);
   if(imgEl.naturalWidth>0)labelImgEl=imgEl;
  }

  if(!initGL())return;

  if(labelImgEl&&gl){
   labelTex=gl.createTexture();
   gl.bindTexture(gl.TEXTURE_2D,labelTex);
   gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,labelImgEl);
   gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
   gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
   gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);
   gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
  }

  const getAccessorArray=accIdx=>{
   const acc=gltf.accessors[accIdx];
   const bv=gltf.bufferViews[acc.bufferView];
   const offset=binOffset+(bv.byteOffset||0)+(acc.byteOffset||0);
   const comps={SCALAR:1,VEC2:2,VEC3:3,VEC4:4}[acc.type]||1;
   const len=acc.count*comps;
   if(acc.componentType===5123)return new Uint16Array(buf,offset,len);
   if(acc.componentType===5125)return new Uint32Array(buf,offset,len);
   return new Float32Array(buf,offset,len);
  };

  meshes=(gltf.nodes||[]).map(node=>{
   if(node.mesh===undefined)return null;
   const prim=gltf.meshes[node.mesh].primitives[0];
   const pos=getAccessorArray(prim.attributes.POSITION);
   const norm=prim.attributes.NORMAL!==undefined?getAccessorArray(prim.attributes.NORMAL):new Float32Array(pos.length);
   const uv=prim.attributes.TEXCOORD_0!==undefined?getAccessorArray(prim.attributes.TEXCOORD_0):null;
   const idx=getAccessorArray(prim.indices);
   const name=(node.name||'').toLowerCase();
   let matType=0,order=2;
   if(name.includes('liquid')){matType=2;order=1;}
   else if(name.includes('dip_tube')){matType=0;order=0;}
   else if(name.includes('glass')){matType=1;order=3;}
   else if(name.includes('label')){matType=3;order=4;}
   const posBuf=gl.createBuffer();
   gl.bindBuffer(gl.ARRAY_BUFFER,posBuf);
   gl.bufferData(gl.ARRAY_BUFFER,pos,gl.STATIC_DRAW);
   const normBuf=gl.createBuffer();
   gl.bindBuffer(gl.ARRAY_BUFFER,normBuf);
   gl.bufferData(gl.ARRAY_BUFFER,norm,gl.STATIC_DRAW);
   let uvBuf=null;
   if(uv){
    uvBuf=gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER,uvBuf);
    gl.bufferData(gl.ARRAY_BUFFER,uv,gl.STATIC_DRAW);
   }
   const idxBuf=gl.createBuffer();
   gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,idxBuf);
   gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,idx,gl.STATIC_DRAW);
   return {
    posBuf,normBuf,uvBuf,idxBuf,
    idxCount:idx.length,
    trans:node.translation||[0,0,0],
    quat:node.rotation||[0,0,0,1],
    scale:node.scale||[0.001,0.001,0.001],
    matType,order
   };
  }).filter(Boolean).sort((a,b)=>a.order-b.order);

  state.loadedProduct=prodInfo.key;
  state.loadedNodes=meshes.length;
  drawFrame();
 }

 function drawGL(){
  if(!canvas||!gl||!prog||!meshes.length||state.contextLost||isReduced()){
   if(canvas)canvas.style.setProperty('--stage-3d-opacity','0');
   return;
  }
  const rect=canvas.getBoundingClientRect();
  const dpr=Math.min(window.devicePixelRatio||1,2);
  const w=Math.max(240,Math.round((rect.width||420)*dpr));
  const h=Math.max(240,Math.round((rect.height||480)*dpr));
  if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}
  gl.viewport(0,0,w,h);
  gl.clearColor(0,0,0,0);
  gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
  gl.enable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);
  gl.useProgram(prog);

  const yawRad=(state.totalYawDeg*Math.PI)/180;
  const pitchRad=(state.dragPitchDeg*Math.PI)/180;
  gl.uniform1f(gl.getUniformLocation(prog,'uYaw'),yawRad);
  gl.uniform1f(gl.getUniformLocation(prog,'uPitch'),pitchRad);
  gl.uniform1f(gl.getUniformLocation(prog,'uAspect'),w/h);

  const aPos=gl.getAttribLocation(prog,'aPos');
  const aNorm=gl.getAttribLocation(prog,'aNorm');
  const aUV=gl.getAttribLocation(prog,'aUV');

  for(const m of meshes){
   gl.uniform3fv(gl.getUniformLocation(prog,'uTrans'),m.trans);
   gl.uniform4fv(gl.getUniformLocation(prog,'uQuat'),m.quat);
   gl.uniform3fv(gl.getUniformLocation(prog,'uScale'),m.scale);
   gl.uniform1i(gl.getUniformLocation(prog,'uMatType'),m.matType);
   if(m.matType===3&&labelTex&&m.uvBuf){
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D,labelTex);
    gl.uniform1i(gl.getUniformLocation(prog,'uLabelTex'),0);
    gl.uniform1i(gl.getUniformLocation(prog,'uHasTex'),1);
   }else{
    gl.uniform1i(gl.getUniformLocation(prog,'uHasTex'),0);
   }
   gl.bindBuffer(gl.ARRAY_BUFFER,m.posBuf);
   gl.enableVertexAttribArray(aPos);
   gl.vertexAttribPointer(aPos,3,gl.FLOAT,false,0,0);
   gl.bindBuffer(gl.ARRAY_BUFFER,m.normBuf);
   gl.enableVertexAttribArray(aNorm);
   gl.vertexAttribPointer(aNorm,3,gl.FLOAT,false,0,0);
   if(aUV>=0){
    if(m.uvBuf){
     gl.bindBuffer(gl.ARRAY_BUFFER,m.uvBuf);
     gl.enableVertexAttribArray(aUV);
     gl.vertexAttribPointer(aUV,2,gl.FLOAT,false,0,0);
    }else{
     gl.disableVertexAttribArray(aUV);
     gl.vertexAttrib2f(aUV,0,0);
    }
   }
   gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,m.idxBuf);
   gl.drawElements(gl.TRIANGLES,m.idxCount,gl.UNSIGNED_SHORT,0);
  }
  const activeOpacity=Math.min(0.28,0.08+Math.abs(state.totalYawDeg)*0.006);
  canvas.style.setProperty('--stage-3d-opacity',activeOpacity.toFixed(3));
 }

 function drawFrame(){
  if(isReduced()){
   state.scrollYawDeg=0;
   state.dragYawDeg=0;
   state.dragPitchDeg=0;
   state.totalYawDeg=0;
  }else{
   state.totalYawDeg=Math.max(-36,Math.min(36,state.scrollYawDeg+state.dragYawDeg));
  }
  const yaw=state.totalYawDeg;
  const pitch=state.dragPitchDeg;
  if(productImg){
   productImg.style.setProperty('--vessel-yaw-deg',`${(yaw*0.42).toFixed(2)}deg`);
   productImg.style.setProperty('--vessel-pitch-deg',`${(pitch*0.35).toFixed(2)}deg`);
   productImg.style.setProperty('--vessel-shift-x',`${(yaw*0.38).toFixed(2)}px`);
  }
  if(shadowEl){
   shadowEl.style.setProperty('--shadow-shift-x',`${(-yaw*0.52).toFixed(2)}px`);
   shadowEl.style.setProperty('--shadow-scale-x',(1+Math.abs(yaw)*0.0025).toFixed(4));
  }
  if(arcDot){
   const cx=Math.max(4,Math.min(40,22+(yaw/30)*16));
   arcDot.setAttribute('cx',cx.toFixed(2));
  }
  drawGL();
 }

 function updateScrollRotation(){
  if(isReduced()){
   state.scrollYawDeg=0;
   drawFrame();
   return;
  }
  const rect=section.getBoundingClientRect();
  const vh=Math.max(1,window.innerHeight);
  // Progress 0 when section top enters bottom of viewport, 0.5 when centered, 1 when bottom exits top
  const totalSpan=vh+rect.height;
  const raw=(vh-rect.top)/Math.max(1,totalSpan);
  const clamped=Math.max(0,Math.min(1,raw));
  // Maps [0, 0.5, 1] -> [-16°, 0°, +14°]
  const deg=clamped<0.5?(-16+(clamped/0.5)*16):(((clamped-0.5)/0.5)*14);
  state.scrollYawDeg=Number(deg.toFixed(2));
  drawFrame();
 }

 async function selectProduct(idx,fromClick=false){
  const i=Math.max(0,Math.min(PRODUCTS.length-1,Number(idx)||0));
  if(!fromClick){
   const btn=document.querySelector(`[data-product="${i}"]`);
   if(btn&&btn.getAttribute('aria-pressed')!=='true'){
    btn.click();
    return;
   }
  }
  state.productIndex=i;
  if(!isReduced()&&window.gsap){
   window.gsap.to(state,{dragYawDeg:0,dragPitchDeg:0,duration:0.42,ease:'power3.out',onUpdate:()=>drawFrame()});
  }else{
   state.dragYawDeg=0;
   state.dragPitchDeg=0;
   drawFrame();
  }
  try{
   await loadGLB(PRODUCTS[i]);
  }catch{
   if(canvas)canvas.style.setProperty('--stage-3d-opacity','0');
  }
 }

 function setDragYaw(deg){
  if(isReduced())return;
  state.dragYawDeg=Math.max(-30,Math.min(30,Number(deg)||0));
  drawFrame();
 }

 stage.addEventListener('dragstart',e=>e.preventDefault());
 stage.addEventListener('pointerdown',e=>{
  if(isReduced())return;
  dragging=true;
  dragMoved=false;
  startX=lastX=e.clientX;
  startY=lastY=e.clientY;
 });
 addEventListener('pointermove',e=>{
  if(!dragging||isReduced())return;
  const dx=e.clientX-lastX;
  const dy=e.clientY-lastY;
  if(Math.hypot(e.clientX-startX,e.clientY-startY)>6)dragMoved=true;
  lastX=e.clientX;
  lastY=e.clientY;
  state.dragYawDeg=Math.max(-30,Math.min(30,state.dragYawDeg+dx*0.22));
  state.dragPitchDeg=Math.max(-6,Math.min(6,state.dragPitchDeg+dy*0.06));
  drawFrame();
 });
 const endDrag=()=>{
  if(!dragging)return;
  dragging=false;
  if(dragMoved){
   setTimeout(()=>{dragMoved=false;},80);
  }
 };
 addEventListener('pointerup',endDrag);
 addEventListener('pointercancel',endDrag);

 stage.addEventListener('keydown',e=>{
  if(isReduced())return;
  if(e.key==='ArrowLeft'){e.preventDefault();setDragYaw(state.dragYawDeg-8);}
  if(e.key==='ArrowRight'){e.preventDefault();setDragYaw(state.dragYawDeg+8);}
  if(e.key==='Home'){e.preventDefault();setDragYaw(0);}
 });

 if(canvas){
  canvas.addEventListener('webglcontextlost',e=>{
   e.preventDefault();
   state.webglActive=false;
   state.contextLost=true;
   canvas.style.setProperty('--stage-3d-opacity','0');
   canvas.hidden=true;
  });
 }

 addEventListener('scroll',()=>requestAnimationFrame(updateScrollRotation),{passive:true});
 addEventListener('resize',()=>requestAnimationFrame(drawFrame),{passive:true});

 const api={
  state,
  selectProduct,
  setDragYaw,
  getTotalYawDeg:()=>state.totalYawDeg,
  wasDragged:()=>dragMoved,
  dispose:disposeGPU,
  redraw:drawFrame
 };
 window.GEMCollectionStage=api;
 window.GEM3DStudio=api;

 updateScrollRotation();
 selectProduct(0,true);
})();
