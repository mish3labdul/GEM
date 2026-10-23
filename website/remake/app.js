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
   image.alt=data.products[i]+'. '+data.concept;
   document.getElementById('pilot-selected-name').textContent=data.products[i];
  }
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
 if(visual)visual.setAttribute('data-zoom-hint',lang==='ar'?'اضغط للتكبير':'Click to inspect');
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
   if(!open&&y>220&&y>lastY+6)header.classList.add('is-hidden');
   if(open||y<lastY-4||y<=220)header.classList.remove('is-hidden');
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
  lb.innerHTML=`<button type="button" class="gem-lightbox-close">${lang==='ar'?'إغلاق ✕':'Close ✕'}</button><div class="gem-lightbox-inner"><img alt=""><p class="gem-lightbox-caption"></p></div>`;
  document.body.appendChild(lb);
  const lbImg=lb.querySelector('img'),lbCap=lb.querySelector('.gem-lightbox-caption'),lbClose=lb.querySelector('.gem-lightbox-close');
  let trigger=null;
  const close=()=>{lb.classList.remove('is-open');lb.setAttribute('aria-hidden','true');if(trigger)trigger.focus();};
  lbClose.addEventListener('click',close);
  lb.addEventListener('click',e=>{if(e.target===lb)close();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&lb.classList.contains('is-open'))close();});
  zoomables.forEach(img=>{
   const target=img.closest('.product-visual')||img;
   if(!target.hasAttribute('tabindex'))target.setAttribute('tabindex','0');
   const open=()=>{trigger=target;lbImg.src=img.currentSrc||img.src;lbImg.alt=img.alt||'';lbCap.textContent=img.closest('figure')?.querySelector('figcaption')?.textContent||document.getElementById('product-name')?.textContent||img.alt||'';lb.classList.add('is-open');lb.setAttribute('aria-hidden','false');lbClose.focus();};
   target.addEventListener('click',open);
   target.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();open();}});
  });
 }
})();
