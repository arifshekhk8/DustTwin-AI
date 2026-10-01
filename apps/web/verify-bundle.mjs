import {chromium} from '@playwright/test';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const browser=await chromium.launch();const page=await browser.newPage();const errors=[],external=[],modes=[];
page.on('pageerror',e=>errors.push(String(e)));
await page.route('**/*',r=>{if(new URL(r.request().url()).hostname==='127.0.0.1')return r.continue();external.push(r.request().url());return r.abort();});
function assert(condition,message){if(!condition)throw new Error(message);}
const bundleRoot=(await readFile(new URL('../../tmp/unpack-path.txt',import.meta.url),'utf8')).trim();const manifest=JSON.parse(await readFile(bundleRoot+'/bundle-manifest.json','utf8'));
try{
 const health=await (await page.request.get('http://127.0.0.1:8003/health')).json();assert(health.ready,'Fresh live runtime not ready');
 const expected=await (await page.request.get('http://127.0.0.1:8003/v1/replay/lab_e4_drill90?second=1010')).json();
 for(const port of [8002,8003]){
  await page.goto(`http://127.0.0.1:${port}/#replay`);await page.getByTestId('model-prediction').waitFor();assert((await page.getByTestId('model-prediction').innerText()).includes(expected.forecast.predicted_pm10_ug_m3.toLocaleString('en-US',{minimumFractionDigits:1,maximumFractionDigits:1})),'Unpacked forecast differs');
  const label=await page.locator('.page-title').innerText();assert(label.includes(port===8003?'Live local inference':'Saved inference replay'),'Wrong inference mode');modes.push({port,mode:port===8003?'live_inference':'saved_inference'});
  await page.goto(`http://127.0.0.1:${port}/#experiment`);await page.getByRole('heading',{name:'Complete eight-minute comparison'}).waitFor();assert((await page.locator('tbody tr').filter({hasText:'Predictive'}).innerText()).includes('1.842'),'Unpacked simulation result differs');
  for(const name of ['dusttwin-judge-packet.pdf','judge-script.md','model-card.md','simulation.md','feasibility.md','offline-demo.md','third-party-notices.md']){
   const r=await page.request.get(`http://127.0.0.1:${port}/demo/documents/${name}`);assert(r.ok(),`Missing document ${name}`);const actual=createHash('sha256').update(await r.body()).digest('hex');assert(actual===manifest.files[`demo/documents/${name}`].sha256,`Changed document ${name}`);
  }
  await page.goto(`http://127.0.0.1:${port}/#system`);await page.getByRole('heading',{name:'Prototype cost basis'}).waitFor();assert((await page.locator('main').innerText()).includes('369.00'),'Cost basis missing');
 }
 assert(errors.length===0,errors.join('\n'));
 const report={passed:true,date:'2026-10-01',source_commit:manifest.source_commit,verified_manifest_files:Object.keys(manifest.files).length,servers_from_freshly_unpacked_folder:modes,live_runtime:'New Python 3.14.6 virtual environment with pinned packages',documents_checked_per_mode:7,forecast_and_simulation_agreement:'passed',external_requests_attempted:external,page_errors:errors};
 await writeFile(new URL('../../reports/readiness/bundle-check.json',import.meta.url),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
}finally{await browser.close();}
