const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{
 const dir=process.argv[2], out=process.argv[3];
 let body='';
 for(let i=1;i<=7;i++){ let s=fs.readFileSync(path.join(dir,`hoja${i}.svg`),'utf8').replace(/<\?xml[^>]*>/,'');
   s=s.replace(/<svg([^>]*?)width="[^"]*"/,'<svg$1width="297mm"').replace(/<svg([^>]*?)height="[^"]*"/,'<svg$1height="210mm"');
   body+=`<div class="p">${s}</div>`;}
 const html=`<!doctype html><meta charset="utf-8"><style>@page{size:297mm 210mm;margin:0}body{margin:0}.p{width:297mm;height:210mm;page-break-after:always;overflow:hidden}.p svg{display:block;width:297mm;height:210mm}</style>${body}`;
 const b=await chromium.launch(); const p=await b.newPage(); await p.setContent(html);
 await p.pdf({path:out,width:'297mm',height:'210mm',printBackground:true}); await b.close();
})();
