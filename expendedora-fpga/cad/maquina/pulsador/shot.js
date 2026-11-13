const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1123,height:794},deviceScaleFactor:1.6});
await p.goto('file://'+process.cwd()+'/esquema_pulsador.svg');await p.screenshot({path:'esquema_pulsador.png'});
await p.pdf({path:'esquema_pulsador.pdf',width:'297mm',height:'210mm',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});await b.close();})();
