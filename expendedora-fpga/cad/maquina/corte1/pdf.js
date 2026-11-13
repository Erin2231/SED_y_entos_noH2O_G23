const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.cwd()+'/plano_corte1.svg');
await p.pdf({path:'plano_corte1.pdf',width:'297mm',height:'420mm',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});
const q=await b.newPage({viewport:{width:1123,height:1588},deviceScaleFactor:1.6});await q.goto('file://'+process.cwd()+'/plano_corte1.svg');await q.screenshot({path:'plano_corte1.png'});await b.close();})();
