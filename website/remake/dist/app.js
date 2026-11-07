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
  document.getElementById('product-name').textContent=data.products[i];
  document.getElementById('product-detail').textContent=data.details[i];
  const image=document.getElementById('product-image');
  if(image){
   const file=['shampoo','conditioner','body-wash','body-lotion','hand-wash'][i]+'-source.webp';
   if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches){const cap=document.querySelector('.product-caption');image.classList.add('is-switching');if(cap)cap.classList.add('is-switching');setTimeout(()=>{image.classList.remove('is-switching');if(cap)cap.classList.remove('is-switching');},120);}
   image.src='/assets/'+file;
   image.alt=data.concept?data.products[i]+'. '+data.concept:data.products[i];
   document.querySelector('.product-visual')?.setAttribute('aria-label',(lang==='ar'?'تكبير صورة ':'Enlarge image of ')+data.products[i]);
   document.getElementById('pilot-selected-name').textContent=data.products[i];
  }
  if(window.GEM3DStudio&&window.GEM3DStudio.selectProduct)window.GEM3DStudio.selectProduct(i,true);
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
   const open=()=>{trigger=target;if(!lbImg)lbImg=document.createElement('img');lbImg.src=img.currentSrc||img.src;lbImg.alt=img.alt||'';lbCap.before(lbImg);lbCap.textContent=img.closest('figure')?.querySelector('figcaption')?.textContent||document.getElementById('product-name')?.textContent||img.alt||'';lb.hidden=false;lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');lbClose.focus();};
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
// W4: Interactive 3D Product System (WebGL2/WebGL1 glTF 2.0 + Turntable Fallback)
// Supports all 5 GEM products, 3 lighting rigs, 3 optical hotspots, & full dispose().
// ============================================================================
(()=>{
 'use strict';
 const section=document.getElementById('interactive-3d-studio');
 if(!section)return;
 const lang=document.body.dataset.lang||'en';
 const ar=lang==='ar';
 const data=JSON.parse(document.getElementById('page-data').textContent);
 const canvas=document.getElementById('gem-3d-canvas');
 const plateImg=document.getElementById('gem-3d-fallback-plate');
 const viewport=document.getElementById('gem-3d-viewport');
 const badge=document.getElementById('studio-3d-badge');
 const readout=document.getElementById('gem-3d-readout');
 const hotspotNote=document.getElementById('gem-3d-hotspot-note');

 const PRODUCTS=[
  {key:'shampoo',glb:'/assets/gem_shampoo.glb',plate:'/assets/gem_shampoo_hero.webp',baseline:true,polys:20460},
  {key:'conditioner',glb:'/assets/gem_conditioner.glb',plate:'/assets/gem_conditioner_hero.webp',baseline:true,polys:20460},
  {key:'body_wash',glb:'/assets/gem_body_wash.glb',plate:'/assets/gem_body_wash_hero.webp',baseline:false,polys:20460},
  {key:'body_lotion',glb:'/assets/gem_body_lotion.glb',plate:'/assets/gem_body_lotion_hero.webp',baseline:false,polys:20460},
  {key:'hand_wash',glb:'/assets/gem_hand_wash.glb',plate:'/assets/gem_hand_wash_hero.webp',baseline:false,polys:20460}
 ];

 const LIGHT_RIGS={
  studio:{
   label:ar?'إضاءة استوديو 85 مم':'85mm Studio Lookdev',
   keyDir:[0.58,0.52,0.62],
   keyColor:[1.08,0.98,0.90],
   fillColor:[0.36,0.38,0.42],
   rimColor:[0.95,0.72,0.42],
   ambient:[0.16,0.15,0.14],
   exposure:1.15
  },
  suite:{
   label:ar?'إضاءة جناح دافئة':'Warm Suite Evening',
   keyDir:[0.68,0.42,0.58],
   keyColor:[1.22,0.86,0.58],
   fillColor:[0.28,0.22,0.18],
   rimColor:[1.05,0.64,0.28],
   ambient:[0.14,0.11,0.09],
   exposure:1.08
  },
  daylight:{
   label:ar?'ضوء نهاري معماري':'Architectural Daylight',
   keyDir:[0.45,0.68,0.57],
   keyColor:[1.05,1.04,1.02],
   fillColor:[0.52,0.54,0.58],
   rimColor:[0.88,0.84,0.78],
   ambient:[0.24,0.24,0.25],
   exposure:1.25
  }
 };

 const HOTSPOTS={
  front:{
   yaw:0,pitch:0.06,zoom:1.0,
   note:ar
    ?'الملصق ثنائي اللغة: خلفية حبرية #12171D مع طباعة عربية وإنجليزية متوازنة وقوس ربع دائري.'
    :'Bilingual Ink Label: #12171D matte ink field with balanced Arabic/English typography and architectural quarter-arc.'
  },
  glass:{
   yaw:0.68,pitch:0.10,zoom:1.08,
   note:ar
    ?'بصريات الزجاج الكهرماني: معامل انكسار 1.520 مع امتصاص ضوئي دافئ يحمي التركيبة ويبرز عمق السائل.'
    :'Amber Glass Optics: IOR 1.520 optical glass with warm spectral transmission and subtle basal wall thickness.'
  },
  pump:{
   yaw:-0.52,pitch:0.22,zoom:1.12,
   note:ar
    ?'مضخة الساتان الهندسية: طوق ومشغّل وفوهة بلمسة ساتان داكنة مصممة لسهولة الاستخدام في غرف الضيوف.'
    :'Satin Pump Profile: Precision collar, actuator, and horizontal spout finished in low-sheen architectural black.'
  }
 };

 const state={
  productIndex:0,
  mode:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'plate':'3d',
  lighting:'studio',
  hotspot:'front',
  yaw:0,
  pitch:0.06,
  zoom:1.0,
  webglActive:false,
  loadedProduct:null,
  loadedPolygons:0,
  loadedNodes:0,
  disposedCount:0,
  glbBytes:0
 };

 let gl=null,prog=null,ctx2d=null,meshes=[],labelTex=null,labelImgEl=null,plateImgEl=null,rafId=0,dragging=false,lastX=0,lastY=0,loadToken=0;

 function disposeGPU(){
  if(rafId){cancelAnimationFrame(rafId);rafId=0;}
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
  if(gl)return true;
  if(ctx2d)return false;
  try{
   gl=canvas.getContext('webgl2',{alpha:true,antialias:true,preserveDrawingBuffer:true})
    ||canvas.getContext('webgl',{alpha:true,antialias:true,preserveDrawingBuffer:true});
  }catch{}
  if(!gl){
   try{ctx2d=canvas.getContext('2d');}catch{}
   return false;
  }
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
   uniform float uZoom;
   uniform float uAspect;
   varying vec3 vNorm;
   varying vec3 vPos;
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
    vPos = pr;
    vNorm = normalize(nr);
    vUV = aUV;
    float zDist = 0.34 - pr.z * uZoom;
    float fov = 2.45 * uZoom;
    gl_Position = vec4((pr.x * fov) / max(0.2, uAspect), pr.y * fov, (zDist - 0.34)*0.5, max(0.05, zDist));
   }
  `;
  const fsSrc=`
   precision mediump float;
   varying vec3 vNorm;
   varying vec3 vPos;
   varying vec2 vUV;
   uniform int uMatType;
   uniform sampler2D uLabelTex;
   uniform int uHasTex;
   uniform vec3 uKeyDir;
   uniform vec3 uKeyCol;
   uniform vec3 uFillCol;
   uniform vec3 uRimCol;
   uniform vec3 uAmbCol;
   uniform float uExposure;
   void main(){
    vec3 N = normalize(vNorm);
    vec3 V = normalize(vec3(0.0, 0.0, 1.0));
    vec3 L = normalize(uKeyDir);
    vec3 H = normalize(L + V);
    float diff = max(dot(N, L), 0.0);
    float fill = max(dot(N, normalize(vec3(-0.6, 0.25, 0.5))), 0.0);
    float fresnel = pow(1.0 - max(dot(N, V), 0.0), 3.0);
    vec3 col = vec3(0.1);
    float alpha = 1.0;
    if(uMatType == 1){
     // Optical Amber Glass (Beer-Lambert + Fresnel)
     vec3 amberCore = vec3(0.54, 0.23, 0.04);
     vec3 amberEdge = vec3(0.16, 0.06, 0.01);
     float spec = pow(max(dot(N, H), 0.0), 96.0) * 1.35;
     col = mix(amberCore, amberEdge, fresnel * 0.72) * (uAmbCol * 1.8 + diff * uKeyCol * 0.95 + fill * uFillCol * 0.6)
           + fresnel * uRimCol * 0.85 + spec * uKeyCol;
     alpha = 0.86;
    } else if(uMatType == 2){
     // Internal Amber Liquid
     vec3 liq = vec3(0.66, 0.31, 0.06);
     col = liq * (uAmbCol * 1.5 + diff * uKeyCol * 0.85 + fill * uFillCol * 0.5);
     alpha = 0.92;
    } else if(uMatType == 3){
     // Bilingual Ink Label (#12171D + M15 Texture)
     vec3 base = vec3(0.071, 0.090, 0.114);
     if(uHasTex == 1){
      vec4 tex = texture2D(uLabelTex, vUV);
      base = tex.rgb;
     }
     float spec = pow(max(dot(N, H), 0.0), 28.0) * 0.18;
     col = base * (uAmbCol * 2.2 + diff * uKeyCol * 0.92 + fill * uFillCol * 0.65) + spec * uKeyCol;
    } else {
     // Satin Black Pump (Collar, Actuator, Spout, Stem)
     vec3 pumpBase = vec3(0.08, 0.085, 0.095);
     float spec = pow(max(dot(N, H), 0.0), 42.0) * 0.55;
     col = pumpBase * (uAmbCol * 2.0 + diff * uKeyCol * 0.9 + fill * uFillCol * 0.6) + fresnel * uRimCol * 0.32 + spec * uKeyCol;
    }
    col = vec3(1.0) - exp(-col * uExposure);
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
  disposeGPU();
  const res=await fetch(prodInfo.glb);
  if(!res.ok)throw new Error('GLB fetch failed: '+res.status);
  const buf=await res.arrayBuffer();
  state.glbBytes=buf.byteLength;
  const dv=new DataView(buf);
  const magic=dv.getUint32(0,true);
  if(magic!==0x46546C67)throw new Error('Invalid GLB magic');
  const jsonLen=dv.getUint32(12,true);
  const jsonStr=new TextDecoder().decode(new Uint8Array(buf,20,jsonLen));
  const gltf=JSON.parse(jsonStr);
  const binOffset=20+jsonLen+8;

  // Decode embedded M15 label PNG texture if present
  if(gltf.images&&gltf.images.length>0){
   const im=gltf.images[0];
   const bv=gltf.bufferViews[im.bufferView];
   const pngBytes=new Uint8Array(buf,binOffset+(bv.byteOffset||0),bv.byteLength);
   const blob=new Blob([pngBytes],{type:im.mimeType||'image/png'});
   const imgUrl=URL.createObjectURL(blob);
   const imgEl=new Image();
   await new Promise(resolve=>{
    imgEl.onload=resolve;
    imgEl.onerror=resolve;
    imgEl.src=imgUrl;
   });
   URL.revokeObjectURL(imgUrl);
   if(imgEl.naturalWidth>0)labelImgEl=imgEl;
  }

  if(!initGL()){
   const pImg=new Image();
   await new Promise(resolve=>{pImg.onload=resolve;pImg.onerror=resolve;pImg.src=prodInfo.plate;});
   if(pImg.naturalWidth>0)plateImgEl=pImg;
   state.loadedProduct=prodInfo.key;
   state.loadedNodes=(gltf.nodes||[]).length;
   state.loadedPolygons=prodInfo.polys;
   drawFrame();
   return;
  }

  if(labelImgEl&&gl){
   labelTex=gl.createTexture();
   gl.bindTexture(gl.TEXTURE_2D,labelTex);
   gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,labelImgEl);
   gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
   gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
   gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);
   gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
  }

  const getAccessorArray=(accIdx)=>{
   const acc=gltf.accessors[accIdx];
   const bv=gltf.bufferViews[acc.bufferView];
   const offset=binOffset+(bv.byteOffset||0)+(acc.byteOffset||0);
   const comps={SCALAR:1,VEC2:2,VEC3:3,VEC4:4}[acc.type]||1;
   const len=acc.count*comps;
   if(acc.componentType===5126)return new Float32Array(buf,offset,len);
   if(acc.componentType===5123)return new Uint16Array(buf,offset,len);
   if(acc.componentType===5125)return new Uint32Array(buf,offset,len);
   return new Float32Array(buf,offset,len);
  };

  let totalPolys=0;
  const rawMeshes=(gltf.nodes||[]).map(node=>{
   if(node.mesh===undefined)return null;
   const mesh=gltf.meshes[node.mesh];
   const prim=mesh.primitives[0];
   const pos=getAccessorArray(prim.attributes.POSITION);
   const norm=prim.attributes.NORMAL!==undefined?getAccessorArray(prim.attributes.NORMAL):new Float32Array(pos.length);
   const uv=prim.attributes.TEXCOORD_0!==undefined?getAccessorArray(prim.attributes.TEXCOORD_0):null;
   const idx=getAccessorArray(prim.indices);
   totalPolys+=Math.floor(idx.length/3);
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
    name:node.name,
    posBuf,normBuf,uvBuf,idxBuf,
    idxCount:idx.length,
    trans:node.translation||[0,0,0],
    quat:node.rotation||[0,0,0,1],
    scale:node.scale||[0.001,0.001,0.001],
    matType,
    order
   };
  }).filter(Boolean);

  meshes=rawMeshes.sort((a,b)=>a.order-b.order);
  state.loadedProduct=prodInfo.key;
  state.loadedNodes=meshes.length;
  state.loadedPolygons=totalPolys||prodInfo.polys;
  drawFrame();
 }

 function drawSoftwareTurntable(w,h){
  if(!ctx2d){try{ctx2d=canvas.getContext('2d');}catch{}}
  if(!ctx2d)return;
  ctx2d.clearRect(0,0,w,h);
  const cx=w*0.5,cy=h*0.53;
  const scale=Math.min(w,h)*state.zoom;
  const rig=LIGHT_RIGS[state.lighting]||LIGHT_RIGS.studio;

  // Studio floor shadow
  const shadowGrad=ctx2d.createRadialGradient(cx,cy+scale*0.36,scale*0.02,cx,cy+scale*0.36,scale*0.24);
  shadowGrad.addColorStop(0,'rgba(0,0,0,0.65)');
  shadowGrad.addColorStop(1,'rgba(0,0,0,0)');
  ctx2d.fillStyle=shadowGrad;
  ctx2d.fillRect(cx-scale*0.28,cy+scale*0.28,scale*0.56,scale*0.16);

  const bw=scale*0.26,bh=scale*0.48;
  const bx=cx-bw*0.5,by=cy-bh*0.32+state.pitch*scale*0.08;
  const yawShift=Math.sin(state.yaw)*bw*0.28;
  const spoutDir=Math.cos(state.yaw);
  const spoutLen=bw*0.64*spoutDir;
  const collarH=bh*0.15,collarY=by-collarH*0.92,stemH=bh*0.045,actH=bh*0.055,actY=collarY-stemH-actH;
  const lblY=by+bh*0.14,lblH=bh*0.72;

  if(plateImgEl&&plateImgEl.naturalWidth>0){
   ctx2d.save();
   const ph=h*0.86*state.zoom;
   const pw=ph*(plateImgEl.naturalWidth/plateImgEl.naturalHeight);
   const px=cx-pw*0.5+yawShift*0.45;
   const py=cy-ph*0.48+state.pitch*scale*0.06;
   ctx2d.beginPath();
   if(ctx2d.roundRect)ctx2d.roundRect(px,py,pw,ph,16);
   else ctx2d.rect(px,py,pw,ph);
   ctx2d.clip();
   ctx2d.drawImage(plateImgEl,px,py,pw,ph);
   if(state.lighting==='suite'){
    ctx2d.fillStyle='rgba(215,130,45,0.16)';
    ctx2d.globalCompositeOperation='multiply';
    ctx2d.fillRect(px,py,pw,ph);
   }else if(state.lighting==='daylight'){
    ctx2d.fillStyle='rgba(235,245,255,0.12)';
    ctx2d.globalCompositeOperation='screen';
    ctx2d.fillRect(px,py,pw,ph);
   }
   ctx2d.restore();
  }else{
   // Procedural fallback when plate image is still decoding
   const collarW=bw*0.48,collarX=cx-collarW*0.5;
   ctx2d.fillStyle='#14181e';
   ctx2d.fillRect(collarX,collarY,collarW,collarH);
   ctx2d.fillStyle='rgb(168,78,14)';
   ctx2d.fillRect(bx,by,bw,bh);
  }

  // Active optical hotspot indicator ring
  const hsPos={
   front:[cx+yawShift*0.35,cy+scale*0.04],
   glass:[cx+bw*0.42,cy+scale*0.22],
   pump:[cx-bw*0.32,cy-scale*0.26]
  }[state.hotspot]||[cx,cy];
  ctx2d.strokeStyle='rgba(248,243,234,0.92)';
  ctx2d.lineWidth=2;
  ctx2d.beginPath();
  ctx2d.arc(hsPos[0],hsPos[1],12,0,Math.PI*2);
  ctx2d.stroke();
  ctx2d.fillStyle='#ebaf4b';
  ctx2d.beginPath();
  ctx2d.arc(hsPos[0],hsPos[1],4,0,Math.PI*2);
  ctx2d.fill();

  // Technical HUD overlay in corner (strictly LTR)
  ctx2d.save();
  ctx2d.direction='ltr';
  ctx2d.textAlign='left';
  ctx2d.fillStyle='rgba(248,243,234,0.78)';
  ctx2d.font='12px SFMono-Regular,Menlo,monospace';
  const deg=Math.round((state.yaw*180/Math.PI)%360);
  ctx2d.fillText(`glTF 2.0 · ${state.loadedNodes||8} nodes · ${(state.loadedPolygons||20460).toLocaleString('en-US')} tris · yaw ${deg}°`,18,h-16);
  ctx2d.restore();
 }

 function drawFrame(){
  const rect=canvas.getBoundingClientRect();
  const dpr=Math.min(window.devicePixelRatio||1,2);
  const w=Math.max(300,Math.round((rect.width||640)*dpr));
  const h=Math.max(240,Math.round((rect.height||480)*dpr));
  if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}
  if(!gl||!prog||!meshes.length){
   drawSoftwareTurntable(w,h);
   return;
  }
  gl.viewport(0,0,w,h);
  gl.clearColor(0,0,0,0);
  gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
  gl.enable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);
  gl.useProgram(prog);

  const rig=LIGHT_RIGS[state.lighting]||LIGHT_RIGS.studio;
  gl.uniform1f(gl.getUniformLocation(prog,'uYaw'),state.yaw);
  gl.uniform1f(gl.getUniformLocation(prog,'uPitch'),state.pitch);
  gl.uniform1f(gl.getUniformLocation(prog,'uZoom'),state.zoom);
  gl.uniform1f(gl.getUniformLocation(prog,'uAspect'),w/h);
  gl.uniform3fv(gl.getUniformLocation(prog,'uKeyDir'),rig.keyDir);
  gl.uniform3fv(gl.getUniformLocation(prog,'uKeyCol'),rig.keyColor);
  gl.uniform3fv(gl.getUniformLocation(prog,'uFillCol'),rig.fillColor);
  gl.uniform3fv(gl.getUniformLocation(prog,'uRimCol'),rig.rimColor);
  gl.uniform3fv(gl.getUniformLocation(prog,'uAmbCol'),rig.ambient);
  gl.uniform1f(gl.getUniformLocation(prog,'uExposure'),rig.exposure);

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
 }

 function updateUI(){
  const p=PRODUCTS[state.productIndex];
  const pName=data.products[state.productIndex]||p.key;
  const rig=LIGHT_RIGS[state.lighting]||LIGHT_RIGS.studio;
  if(badge){
   badge.dataset.status=p.baseline?'baseline':'provisional';
   badge.textContent=p.baseline
    ?(ar?'خط الأساس المعتمد · معايرة بصرية M27a/M28':'Verified CGI Baseline · M27a/M28 Optical Calibration')
    :(ar?'نموذج ثلاثي الأبعاد تجريبي · قيد تأكيد المورّد':'Provisional 3D Geometry · Pending Supplier Confirmation');
  }
  if(readout){
   readout.textContent=ar
    ?`${pName} · زجاج كهرماني بمعامل انكسار 1.520 · ${p.polys.toLocaleString('en-US')} مضلعًا · ${rig.label}`
    :`${pName} · Optical Amber Glass (IOR 1.520) · ${p.polys.toLocaleString('en-US')} polygons · ${rig.label}`;
  }
  if(hotspotNote&&HOTSPOTS[state.hotspot]){
   hotspotNote.textContent=HOTSPOTS[state.hotspot].note;
  }
  if(plateImg){
   plateImg.src=p.plate;
   plateImg.alt=ar
    ?`معاينة استوديو لعبوة ${pName} الزجاجية الكهرمانية من GEM بملصق ثنائي اللغة`
    :`Studio render of the GEM amber glass ${pName} bottle with bilingual ink label`;
  }
  const show3d=state.mode==='3d';
  if(canvas)canvas.hidden=!show3d;
  if(plateImg)plateImg.hidden=show3d;
  if(viewport)viewport.dataset.lightingActive=state.lighting;
  section.querySelectorAll('[data-studio-product]').forEach((b,idx)=>b.setAttribute('aria-pressed',String(idx===state.productIndex)));
  section.querySelectorAll('[data-studio-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.studioMode===state.mode)));
  section.querySelectorAll('[data-lighting]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.lighting===state.lighting)));
  section.querySelectorAll('[data-hotspot]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.hotspot===state.hotspot)));
 }

 async function selectProduct(idx,fromPilot=false){
  const i=Math.max(0,Math.min(PRODUCTS.length-1,Number(idx)||0));
  if(!fromPilot){
   const pilotBtn=document.querySelector(`[data-product="${i}"]`);
   if(pilotBtn&&pilotBtn.getAttribute('aria-pressed')!=='true'){
    pilotBtn.click();
    return;
   }
  }
  state.productIndex=i;
  updateUI();
  try{
   await loadGLB(PRODUCTS[i]);
  }catch{
   state.mode='plate';
   updateUI();
  }
 }

 function setMode(mode){
  state.mode=mode==='plate'?'plate':'3d';
  updateUI();
  if(state.mode==='3d')drawFrame();
 }

 function setLighting(lightKey){
  if(!LIGHT_RIGS[lightKey])return;
  state.lighting=lightKey;
  updateUI();
  drawFrame();
 }

 function setHotspot(hsKey){
  const h=HOTSPOTS[hsKey];
  if(!h)return;
  state.hotspot=hsKey;
  updateUI();
  window.gsap.to(state,{
   yaw:h.yaw,
   pitch:h.pitch,
   zoom:h.zoom,
   duration:0.65,
   ease:'power3.out',
   onUpdate:()=>drawFrame()
  });
 }

 section.querySelectorAll('[data-studio-product]').forEach(b=>b.addEventListener('click',()=>selectProduct(Number(b.dataset.studioProduct),false)));
 section.querySelectorAll('[data-studio-mode]').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.studioMode)));
 section.querySelectorAll('[data-lighting]').forEach(b=>b.addEventListener('click',()=>setLighting(b.dataset.lighting)));
 section.querySelectorAll('[data-hotspot]').forEach(b=>b.addEventListener('click',()=>setHotspot(b.dataset.hotspot)));
 section.querySelectorAll('[data-turntable]').forEach(b=>b.addEventListener('click',()=>{
  const act=b.dataset.turntable;
  const targetYaw=act==='reset'?0:state.yaw+(act==='left'?-0.55:0.55);
  const targetPitch=act==='reset'?0.06:state.pitch;
  window.gsap.to(state,{yaw:targetYaw,pitch:targetPitch,duration:0.45,ease:'power3.out',onUpdate:()=>drawFrame()});
 }));

 if(canvas){
  canvas.addEventListener('pointerdown',e=>{dragging=true;lastX=e.clientX;lastY=e.clientY;try{canvas.setPointerCapture(e.pointerId);}catch{}});
  canvas.addEventListener('pointermove',e=>{
   if(!dragging)return;
   const dx=e.clientX-lastX,dy=e.clientY-lastY;
   lastX=e.clientX;lastY=e.clientY;
   state.yaw+=dx*0.012;
   state.pitch=Math.max(-0.45,Math.min(0.55,state.pitch+dy*0.008));
   drawFrame();
  });
  const endDrag=()=>{dragging=false;};
  canvas.addEventListener('pointerup',endDrag);
  canvas.addEventListener('pointercancel',endDrag);
  canvas.addEventListener('keydown',e=>{
   if(e.key==='ArrowLeft'){e.preventDefault();state.yaw-=0.25;drawFrame();}
   if(e.key==='ArrowRight'){e.preventDefault();state.yaw+=0.25;drawFrame();}
   if(e.key==='Home'){e.preventDefault();state.yaw=0;state.pitch=0.06;drawFrame();}
  });
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();state.webglActive=false;setMode('plate');});
 }
 addEventListener('resize',()=>{if(state.mode==='3d')drawFrame();},{passive:true});

 window.GEM3DStudio={
  state,
  selectProduct,
  setMode,
  setLighting,
  setHotspot,
  dispose:disposeGPU,
  redraw:drawFrame
 };

 selectProduct(0,true);
})();
