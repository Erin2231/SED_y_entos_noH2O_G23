const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1588,height:1123},deviceScaleFactor:1.4});
await p.goto('file://'+process.cwd()+'/crestas.svg');await p.screenshot({path:'crestas.png'});
await p.pdf({path:'crestas.pdf',width:'420mm',height:'297mm',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});await b.close();})();
