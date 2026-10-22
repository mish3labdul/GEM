// Required font failure is visible and disables the embedded reader.
Promise.all([
  document.fonts.load('16px "Noto Sans Arabic"', 'أصول المشروع'),
  document.fonts.load('16px Jost', 'GEM'),
  document.fonts.load('16px Inter', 'Project Assets')
]).then(results => {
  if(results.some(fonts=>!fonts.length || fonts.some(font=>font.status!=='loaded')))throw Error('Required font missing');
}).catch(()=>{
  document.documentElement.classList.add('font-failed');
  document.getElementById('font-failure').hidden=false;
});
