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
 Promise.all([document.fonts.load('16px Arabic','العربية'),document.fonts.load('16px Jost','GEM'),document.fonts.load('16px Inter','GEM')]).then(loaded=>{if(loaded.some(a=>!a.length))throw Error('Required font missing');}).catch(()=>{document.documentElement.classList.add('font-error');document.querySelector('.font-failure').hidden=false;});
})();
