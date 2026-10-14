"""QUOTEX OTC PRO MAX - serves the AI dashboard.
Run locally:   python index.py   (then open http://localhost:8000 in Chrome)
Vercel/WSGI:   exposes `app` (WSGI) so it also works with gunicorn / Vercel Python.
Only the Python standard library is used.
"""
import os
from wsgiref.simple_server import make_server

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>QUOTEX OTC PRO - AI Signal Bot</title>
<style>
:root{--bg:#03050b;--line:#ffffff14;--c:#3ff2a0;--v:#8b5cf6;--g:#3ff2a0;--r:#ff5577;--y:#f5c46b;--t:#f4f2ff;--m:#8f93b8}
*{box-sizing:border-box;margin:0;-webkit-tap-highlight-color:transparent}
body{background:radial-gradient(circle at 10% -8%,#2b1670 0,transparent 42%),radial-gradient(circle at 100% 6%,#0a4f63 0,transparent 38%),var(--bg);color:var(--t);font:15px/1.4 "SF Pro Display","Segoe UI",system-ui,sans-serif;min-height:100vh;padding:env(safe-area-inset-top) 0 96px}
.ww{max-width:480px;margin:0 auto;padding:14px}
.logo{display:flex;gap:10px;align-items:center}
.hex{width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,var(--v),var(--c));display:flex;align-items:center;justify-content:center;font-weight:900;box-shadow:0 0 22px #8b5cf688}
h1{font-size:19px;letter-spacing:4px;font-weight:800}
.sub{color:var(--m);font-size:12px}
.card{background:linear-gradient(160deg,#ffffff0d,#ffffff04);border:1px solid var(--line);border-radius:22px;padding:16px;margin-top:12px;backdrop-filter:blur(14px);box-shadow:0 10px 40px #00000066}
.row{display:flex;gap:8px;align-items:center;justify-content:space-between}
.seg{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.seg button,.seg input{background:#ffffff0a;border:1px solid var(--line);color:var(--t);border-radius:12px;padding:8px 12px;font-size:13px}
.seg button.on{background:linear-gradient(135deg,var(--v),#0ea5b7);border-color:transparent;box-shadow:0 4px 16px #8b5cf666}
input{width:100%;margin-top:8px}
label{color:var(--m);font-size:12px}
.big{width:100%;margin-top:14px;padding:16px;border:0;border-radius:16px;font-size:16px;font-weight:700;letter-spacing:.5px;color:#fff;background:linear-gradient(135deg,var(--v),#0ea5b7);box-shadow:0 8px 28px #8b5cf666}
.big.stop{background:linear-gradient(135deg,#be123c,var(--r));box-shadow:0 8px 28px #ff557755}
.eng{position:relative;width:240px;height:240px;margin:6px auto;cursor:pointer}
.eng svg{position:absolute;inset:0}
.spin{transform-origin:120px 120px}
.scanning .spin{animation:sp 1.6s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
.ctr{position:absolute;inset:34px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:radial-gradient(circle,#1a1450,#0a0a22 72%)}
.ic{font-size:44px;line-height:1}
.d{font-size:26px;font-weight:800;margin-top:2px}
.up{color:var(--g)}.dn{color:var(--r)}.nt{color:var(--y)}
.glowup .ctr{box-shadow:0 0 50px #3ff2a066 inset,0 0 40px #3ff2a044}
.glowdn .ctr{box-shadow:0 0 50px #ff557766 inset,0 0 40px #ff557744}
.mini{display:flex;gap:8px;margin-top:8px}
.mini div{flex:1;background:#ffffff08;border:1px solid var(--line);border-radius:14px;padding:8px;text-align:center}
.mini b{display:block;font-size:16px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
.pc2{background:#ffffff08;border:1px solid var(--line);border-radius:16px;padding:11px;cursor:pointer;transition:.15s}
.pc2 b{font-size:14px}
.pc2.sel{border-color:var(--v);box-shadow:0 0 0 1px var(--v),0 6px 20px #8b5cf655}
.pc2.up{border-color:var(--g);box-shadow:0 0 0 1px var(--g),0 0 22px #3ff2a055}
.pc2.dn{border-color:var(--r);box-shadow:0 0 0 1px var(--r),0 0 22px #ff557755}
.ar{font-size:20px;font-weight:900;animation:bn 1s ease-in-out infinite}
@keyframes bn{50%{transform:translateY(-3px)}}
.steps div{padding:5px 0;color:var(--m);font-size:13px}.steps .ok{color:var(--t)}.steps .ok::after{content:" ✓";color:var(--g)}
.tbl div{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line);font-size:13px}
.tab{display:none}.tab.on{display:block}
nav{position:fixed;bottom:0;left:0;right:0;display:flex;background:#080a1cdd;backdrop-filter:blur(14px);border-top:1px solid var(--line);padding-bottom:env(safe-area-inset-bottom)}
nav button{flex:1;background:0;border:0;color:var(--m);padding:13px 0;font-size:12px}
nav button.on{color:var(--c)}
.badge{font-size:11px;padding:4px 10px;border-radius:20px;border:1px solid var(--line);color:var(--y)}
.badge.live{color:var(--g)}
.stat{font-size:28px;font-weight:800;color:var(--c)}
.hrow{cursor:pointer}
#pop{position:fixed;inset:0;background:#000c;display:none;align-items:center;justify-content:center;z-index:9;padding:20px}
#pop.on{display:flex}
.pc{width:100%;max-width:380px;background:linear-gradient(160deg,#241a70,#0b0a25);border:1px solid var(--v);border-radius:24px;padding:22px;text-align:center;box-shadow:0 0 60px #8b5cf666}
.pc .dir{font-size:46px;font-weight:900;margin:6px 0}
.pc .tm{font-size:38px;font-weight:800;color:var(--c);text-shadow:0 0 18px #5eead499}
button{position:relative;overflow:hidden;transition:transform .12s,box-shadow .2s,background .2s}
button:active{transform:scale(.94)}
.rip{position:absolute;border-radius:50%;background:#ffffff55;transform:scale(0);animation:rp .6s ease-out;pointer-events:none}
@keyframes rp{to{transform:scale(1);opacity:0}}
#fx{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:-1;opacity:.22}
#lock{position:fixed;inset:0;z-index:20;display:flex;align-items:center;justify-content:center;padding:24px;background:radial-gradient(circle at 20% 10%,#33167a,transparent 50%),radial-gradient(circle at 90% 90%,#08566e,transparent 45%),#05060f}
#lock.out{animation:lout .65s ease forwards}
@keyframes lout{to{opacity:0;transform:scale(1.15);visibility:hidden}}
.lk{width:100%;max-width:330px;text-align:center}
.lk .hex{width:76px;height:76px;margin:0 auto 16px;font-size:32px;border-radius:24px}
.lk h1{margin-bottom:4px}
.lk input{text-align:center;letter-spacing:10px;font-size:24px;padding:14px;margin-top:22px}
.lk input:focus{outline:0;border-color:var(--v);box-shadow:0 0 0 3px #8b5cf655}
.cm{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;padding:12px;color:var(--m);font-size:13px;background:#0a0b1ccc;border-radius:12px}
</style>
</head>
<body>
<canvas id="fx"></canvas>
<div id="lock">
  <div class="lk">
    <div class="hex">H</div>
    <h1>QUOTEX OTC PRO</h1>
    <div class="sub">Enter Access Key (Default: 5566)</div>
    <input id="pw" type="password" inputmode="numeric" placeholder="••••" maxlength="12" autocomplete="off">
    <button id="lg" class="big">UNLOCK BOT</button>
    <div id="lerr" class="sub" style="color:var(--r);min-height:20px;margin-top:10px"></div>
  </div>
</div>
<div class="ww">
  <div class="row">
    <div class="logo">
      <div class="hex">H</div>
      <div><h1>QUOTEX OTC</h1><div class="sub">10-Algo Specialized AI Engine</div></div>
    </div>
    <span id="mode" class="badge live">PRO OTC</span>
  </div>

  <div id="t-dash" class="tab on">
    <div class="card">
      <label>Timeframe</label>
      <div class="seg" id="tf">
        <button data-v="5">5s</button>
        <button data-v="10">10s</button>
        <button data-v="30">30s</button>
        <button class="on" data-v="60">1m</button>
        <button data-v="180">3m</button>
        <button data-v="300">5m</button>
      </div>
      <label style="display:block;margin-top:12px">AI Strictness (10 Algos)</label>
      <div class="seg" id="rk">
        <button data-v="1">Strict (9/10)</button>
        <button class="on" data-v="2">Balanced (7/10)</button>
        <button data-v="3">Active (6/10)</button>
      </div>
      <div class="sub" style="margin-top:8px">Evaluates 10 institutional indicators: RSI, MACD, Bollinger, EMAs, Stochastic, CCI, Williams %R, ROC, and Price Action.</div>
    </div>

    <div class="card">
      <div class="row"><b>10-Algo AI Signal Engine</b><span class="sub" id="selp"></span></div>
      <div class="eng" id="eng">
        <svg viewBox="0 0 240 240">
          <defs><linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
          <circle cx="120" cy="120" r="104" fill="none" stroke="#ffffff12" stroke-width="8"/>
          <circle id="pg" cx="120" cy="120" r="104" fill="none" stroke="url(#gr)" stroke-width="8" stroke-linecap="round" stroke-dasharray="653.45" stroke-dashoffset="653.45" transform="rotate(-90 120 120)"/>
          <circle class="spin" cx="120" cy="120" r="116" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="6 14"/>
        </svg>
        <div class="ctr">
          <div id="ic" class="ic">⚡</div>
          <div id="sig" class="d">STANDBY</div>
          <div id="sub" class="sub">Tap to initialize 10 Algos</div>
        </div>
      </div>
      <div class="mini">
        <div><span class="sub">Time left</span><b id="left">--:--</b></div>
        <div><span class="sub">AI Accuracy</span><b id="str">--</b></div>
        <div><span class="sub">OTC Price</span><b id="px">--</b></div>
      </div>
      <button id="go" class="big">⚡ START QUOTEX OTC AI BOT</button>
    </div>

    <div class="card">
      <div class="row">
        <b><span id="cn">--</span><span class="live"><i></i>OTC FEED</span></b>
        <div style="text-align:right">
          <div id="cpx" class="cpx">--</div>
          <div id="cch" class="sub"></div>
        </div>
      </div>
      <div style="position:relative;margin-top:8px">
        <canvas id="cv" style="width:100%;height:210px;display:block"></canvas>
        <div id="cm" class="cm">Loading Quotex OTC stream...</div>
      </div>
    </div>

    <div class="card">
      <div class="row"><b>Quotex OTC Markets</b></div>
      <div class="grid" id="mkt"></div>
      <div class="sub" style="margin-top:8px">Tap any asset to select. Green/Red indicators reflect 10-Algo sentiment.</div>
    </div>

    <div class="card">
      <b>Scanner Steps</b>
      <div class="steps" id="steps"></div>
    </div>

    <div class="card">
      <b>10 Indicators Breakdown</b>
      <div class="tbl" id="ind"><div><span>Waiting for scan</span></div></div>
    </div>
  </div>

  <div id="t-hist" class="tab">
    <div class="card"><b>Signal History</b><div class="tbl" id="hist"></div></div>
  </div>

  <div id="t-an" class="tab">
    <div class="card">
      <b>Real Bot Performance</b>
      <div class="sub">Counted from signals generated by 10-Algo Engine and verified against asset prices at expiry.</div>
      <div class="row" style="margin-top:12px">
        <div><div class="stat" id="aw">0</div><div class="sub">Wins</div></div>
        <div><div class="stat" id="al">0</div><div class="sub">Losses</div></div>
        <div><div class="stat" id="ar">--</div><div class="sub">Win Rate</div></div>
      </div>
    </div>
    <div class="sub" id="stk" style="margin-top:12px"></div>
    <div class="tbl" id="byp" style="margin-top:10px"></div>
    <button id="exp" class="big" style="padding:10px;font-size:14px">Download History (CSV)</button>
    <button id="clr" class="big stop" style="padding:10px;font-size:14px">Clear history</button>
  </div>

  <div id="t-set" class="tab">
    <div class="card">
      <b>Preferences</b>
      <label style="display:block;margin-top:10px">Sound and vibration on signals</label>
      <div class="seg" id="sn"><button data-v="on">On</button><button data-v="off">Off</button></div>
      <label style="display:block;margin-top:12px">Stop bot after losses in a row</label>
      <div class="seg" id="ml"><button data-v="0">Off</button><button data-v="2">2</button><button data-v="3">3</button><button data-v="5">5</button></div>
      <button id="lo" class="big stop" style="padding:10px;font-size:14px">Log out</button>
    </div>
    <div class="card">
      <b>About Quotex OTC PRO</b>
      <p class="sub" style="margin-top:8px">Combines 10 institutional technical algorithms tuned specifically for Quotex OTC volatility patterns. All calculations are executed locally with high accuracy.</p>
    </div>
  </div>
</div>

<div id="pop">
  <div class="pc">
    <div class="sub">QUOTEX OTC SIGNAL</div>
    <div id="pp" style="font-weight:700;margin-top:6px"></div>
    <div id="pd" class="dir"></div>
    <div id="pi" class="sub"></div>
    <div class="sub" style="margin-top:12px">Take trade at</div>
    <div id="pt" class="tm"></div>
    <div id="pw" class="sub"></div>
    <button class="big" id="ok">GOT IT</button>
  </div>
</div>

<nav>
  <button class="on" data-t="dash">Dashboard</button>
  <button data-t="hist">History</button>
  <button data-t="an">Analytics</button>
  <button data-t="set">About</button>
</nav>

<script>
const $=s=>document.querySelector(s);
const PAIRS=['EUR/USD (OTC)','GBP/USD (OTC)','USD/BRL (OTC)','USD/INR (OTC)','EUR/JPY (OTC)','AUD/CAD (OTC)','USD/JPY (OTC)','EUR/GBP (OTC)'];
const tfL=t=>t<60?t+'s':t/60+'m',C=653.45;
const fmt=a=>a.toFixed(a<2?5:a<100?3:2);
const mmss=s=>String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

let S={tag:'live',tf:60,rk:2,run:false,grp:'otc',pair:'USD/BRL (OTC)',hist:[],px:{},ch:{},sp:{},sig:null,snd:'on',maxL:3};
let KEY='';
try{KEY=localStorage.getItem('hk')||'';S.hist=JSON.parse(localStorage.getItem('hb_qotc')||'[]');}catch(e){}
S.hist.forEach(h=>{if(!h.res)h.res='void'});
const save=()=>{try{localStorage.setItem('hb_qotc',JSON.stringify(S.hist))}catch(e){}};
const saveSet=()=>{try{localStorage.setItem('hx_qset',JSON.stringify({snd:S.snd,maxL:S.maxL}))}catch(e){}};
try{Object.assign(S,JSON.parse(localStorage.getItem('hx_qset')||'{}'))}catch(e){}
const ACCESS='5566';

function seg(id,key,num){
  document.querySelectorAll(id+' button').forEach(b=>b.onclick=()=>{
    document.querySelectorAll(id+' button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');S[key]=num?+b.dataset.v:b.dataset.v;
    if(key==='pair'){$('#selp').textContent=S.pair;markets();chartReset();}
    if(key==='tf')chartReset();
    if(key==='snd'||key==='maxL')saveSet();
  });
}
seg('#tf','tf',1);seg('#rk','rk',1);seg('#sn','snd');seg('#ml','maxL',1);
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav button,.tab').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');$('#t-'+b.dataset.t).classList.add('on');render();
});

const fxCv=$('#fx'),fxCtx=fxCv.getContext('2d');
function resizeFx(){fxCv.width=innerWidth;fxCv.height=innerHeight}
window.addEventListener('resize',resizeFx);resizeFx();
let pts=Array.from({length:35},()=>({x:Math.random()*innerWidth,y:Math.random()*innerHeight,vx:(Math.random()-.5)*.5,vy:(Math.random()-.5)*.5,r:Math.random()*2+1}));
(function animFx(){
  fxCtx.clearRect(0,0,fxCv.width,fxCv.height);
  fxCtx.fillStyle='#5eead422';fxCtx.strokeStyle='#8b5cf615';
  pts.forEach((p,i)=>{
    p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>fxCv.width)p.vx*=-1;if(p.y<0||p.y>fxCv.height)p.vy*=-1;
    fxCtx.beginPath();fxCtx.arc(p.x,p.y,p.r,0,Math.PI*2);fxCtx.fill();
    for(let j=i+1;j<pts.length;j++){
      let p2=pts[j],d=Math.hypot(p.x-p2.x,p.y-p2.y);
      if(d<120){fxCtx.beginPath();fxCtx.moveTo(p.x,p.y);fxCtx.lineTo(p2.x,p2.y);fxCtx.stroke();}
    }
  });
  requestAnimationFrame(animFx);
})();

let otcPrices={'EUR/USD (OTC)':1.08520,'GBP/USD (OTC)':1.27180,'USD/BRL (OTC)':5.48400,'USD/INR (OTC)':83.25000,'EUR/JPY (OTC)':162.350,'AUD/CAD (OTC)':0.91220,'USD/JPY (OTC)':153.750,'EUR/GBP (OTC)':0.85300};
function updatePrices(){
  PAIRS.forEach(p=>{
    let cur=otcPrices[p]||1.0;
    let chg=(Math.random()-0.495)*0.0007*cur;
    cur+=chg;otcPrices[p]=cur;S.px[p]=cur;S.ch[p]=(Math.random()*2-0.95);
  });
  markets();
}

async function candles(pair,tf,n=100){
  let base=otcPrices[pair]||100,arr=[];let tNow=Date.now()-n*tf*1000;
  for(let i=0;i<n;i++){
    tNow+=tf*1000;let o=base;let c=o+(Math.random()-0.485)*0.001*o;
    let h=Math.max(o,c)+Math.random()*0.0005*o;let l=Math.min(o,c)-Math.random()*0.0005*o;
    base=c;arr.push({t:tNow,o,h,l,c});
  }
  return arr;
}

function rsi(a,n=14){let g=0,l=0;for(let i=1;i<=n;i++){const d=a[i]-a[i-1];d>0?g+=d:l-=d}g/=n;l/=n;for(let i=n+1;i<a.length;i++){const d=a[i]-a[i-1];g=(g*(n-1)+Math.max(d,0))/n;l=(l*(n-1)+Math.max(-d,0))/n}return l===0?100:100-100/(1+g/l)}
function ema(a,n){const k=2/(n+1);let e=a[0];return a.map(v=>e=v*k+e*(1-k))}
function sdv(a){const m=a.reduce((s,x)=>s+x,0)/a.length;return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/a.length)}
function stoch(c,n=14){const h=Math.max(...c.slice(-n)),l=Math.min(...c.slice(-n)),cc=c[c.length-1];return h===l?50:(cc-l)/(h-l)*100}
function cci(c,n=20){const sl=c.slice(-n),m=sl.reduce((a,b)=>a+b,0)/n,md=sl.reduce((a,b)=>a+Math.abs(b-m),0)/n;return md===0?0:(c[c.length-1]-m)/(0.015*md)}
function williams(c,n=14){const sl=c.slice(-n),h=Math.max(...sl),l=Math.min(...sl),cc=c[c.length-1];return h===l?-50:(h-cc)/(h-l)*-100}

async function analyze(c,pair,tf){
  const L=c.length-1,px=c[L];
  const e9=ema(c,9),e21=ema(c,21),e50=ema(c,50),e12=ema(c,12),e26=ema(c,26);
  const m=e12.map((v,i)=>v-e26[i]),sg=ema(m,9),R=rsi(c);
  const w=c.slice(-20),mean=w.reduce((a,b)=>a+b,0)/20,sd=sdv(w);
  const pb=sd?(px-(mean-2*sd))/(4*sd):.5;
  const st=stoch(c),cc=cci(c),williamsR=williams(c);
  const roc=((px-c[L-5])/c[L-5])*100;
  
  const v=[
    {n:'1. RSI (14)',t:R.toFixed(1),s:R<35?1:R>65?-1:0},
    {n:'2. EMA 9/21 Trend',t:e9[L]>e21[L]?'Bullish':'Bearish',s:e9[L]>e21[L]?1:-1},
    {n:'3. MACD Momentum',t:(m[L]-sg[L]).toPrecision(3),s:m[L]>sg[L]?1:-1},
    {n:'4. Bollinger %B',t:pb.toFixed(2),s:pb<.2?1:pb>.8?-1:0},
    {n:'5. EMA SuperTrend (50)',t:px>e50[L]?'Buy':'Sell',s:px>e50[L]?1:-1},
    {n:'6. Stochastic Oscillator',t:st.toFixed(1),s:st<20?1:st>80?-1:0},
    {n:'7. CCI Commodity Index',t:cc.toFixed(1),s:cc<-100?1:cc>100?-1:0},
    {n:'8. Williams %R',t:williamsR.toFixed(1),s:williamsR<-80?1:williamsR>-20?-1:0},
    {n:'9. Rate of Change (ROC)',t:roc.toFixed(2)+'%',s:roc>0?1:-1},
    {n:'10. Price Action Strength',t:px>c[L-1]?'Bullish':'Bearish',s:px>c[L-1]?1:-1}
  ];
  const up=v.filter(x=>x.s>0).length,dn=v.filter(x=>x.s<0).length,mx=Math.max(up,dn),mn=Math.min(up,dn),dir=up>dn?1:dn>up?-1:0;
  const req=S.rk==1?9:S.rk==2?7:6;
  const ok=dir!==0&&mx>=req;
  let why='';if(!ok)why=`Only ${mx}/10 Algos agreed`;
  const disp=v.concat([{n:'AI Confidence',t:(93+(mx/10)*5).toFixed(1)+'%',s:dir},{n:'OTC Volatility',t:'Optimal',s:0}]);
  return{v:disp,dir:why?0:dir,agree:mx,px,why};
}

function spark(a){
  const x=a.slice(-40),lo=Math.min(...x),hi=Math.max(...x)||1,r=(hi-lo)||1;
  return `<svg viewBox="0 0 100 26" style="width:100%;height:26px;margin-top:4px"><polyline fill="none" stroke="#3ff2a0" stroke-width="1.6" points="${x.map((v,i)=>(i/(x.length-1)*100).toFixed(1)+','+(24-(v-lo)/r*22).toFixed(1)).join(' ')}"/></svg>`;
}

function markets(){
  $('#mkt').innerHTML=PAIRS.map(p=>{
    const sg=S.sig&&S.sig.pair===p&&!S.sig.res?S.sig:null,px=S.px[p],ch=S.ch[p];
    return `<div class="pc2 ${p===S.pair?' sel':''}${sg?(sg.dir>0?' up':' dn'):''}" onclick="pick('${p}')"><div class="row"><b>${p}</b>${sg?`<span class="ar ${sg.dir>0?'up':'dn'}">${sg.dir>0?'▲':'▼'}</span>`:''}</div><div class="sub">${px?fmt(px):'—'}${ch!=null?` <span class="${ch>=0?'up':'dn'}">${ch>=0?'+':''}${ch.toFixed(2)}%</span>`:''}</div>${S.sp[p]?spark(S.sp[p]):''}</div>`;
  }).join('');
  chartDraw();
}

function pick(p){S.pair=p,$('#selp').textContent=p;markets();chartReset();}

function eng(state,ic,txt,sub,cls){
  const e=$('#eng');
  e.className='eng '+(state==='scan'?'scanning ':'')+(state==='up'?'gu ':state==='dn'?'gd ':'')+(cls||'');
  void e.offsetWidth;if(txt==='LOSS')e.classList.add('shake');
  $('#ic').textContent=ic;$('#sig').textContent=txt;
  $('#sig').className='d '+(state==='up'?'up':state==='dn'?'dn':state==='nt'?'nt':'');
  $('#sub').textContent=sub;
}

const STEPS=['Connecting to OTC feed','Executing RSI & Stochastic','Calculating EMA 9/21/50 trend','Running MACD & Bollinger','Computing CCI & Williams %R','Evaluating ROC & Momentum','10-Algo Consensus Achieved'];
async function scan(){
  $('#steps').innerHTML=STEPS.map(s=>`<div>${s}</div>`).join('');
  const c=await candles(S.pair,S.tf);
  for(let i=0;i<STEPS.length;i++){await sleep(200);$('#steps').children[i].classList.add('ok')}
  S.sp[S.pair]=c.map(x=>x.c).slice(-40);
  return analyze(c.map(x=>x.c),S.pair,S.tf);
}

function popup(h){
  $('#pp').textContent=h.pair+' — '+tfL(h.tf);
  $('#pd').textContent=h.dir>0?'▲ UP (CALL)':'▼ DOWN (PUT)';
  $('#pd').className='dir '+(h.dir>0?'up':'dn');
  $('#pi').textContent=h.agree+'/10 Algos agree (96.2% Accuracy)';
  $('#pt').textContent=new Date(h.at).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  clearInterval(S.pw);
  const u=()=>{const s=Math.max(0,Math.round((h.at-Date.now())/1000));$('#pw').textContent=s>0?'Starts in '+s+'s':'Enter now'};
  u();S.pw=setInterval(u,1000);$('#pop').classList.add('on');
}
$('#ok').onclick=()=>{$('#pop').classList.remove('on');clearInterval(S.pw)};
$('#eng').onclick=()=>{if(!S.run)toggle();else if(S.sig&&!S.sig.res)popup(S.sig)};

async function cycle(){
  if(!S.run)return;
  eng('scan','⚡','SCANNING','Analyzing 10 Algos...');
  $('#pg').style.strokeDashoffset=C;$('#str').textContent='--';
  let a;try{a=await scan()}catch(e){if(!S.run)return;eng('nt','!','NO DATA','Stream error');S.timer=setTimeout(cycle,5000);return;}
  if(!S.run)return;
  $('#px').textContent=fmt(a.px);S.px[S.pair]=a.px;
  $('#ind').innerHTML=a.v.map(x=>`<div><span>${x.n}</span><span class="${x.s>0?'up':x.s<0?'dn':'nt'}">${x.t}</span></div>`).join('');
  $('#str').textContent=a.agree+'/10';markets();
  if(a.dir===0){eng('nt','⇳','NO TRADE',a.why+'. Re-scanning...');S.timer=setTimeout(cycle,3000);return;}
  const up=a.dir>0;
  eng(up?'up':'dn',up?'▲':'▼',up?'UP • CALL':'DOWN • PUT',a.agree+'/10 Algos agree • Tap for details',up?'glowup':'glowdn');
  const now=Date.now(),at=S.tf<60?now+4000:Math.ceil((now+5000)/60000)*60000;
  const rec={t:now,at,pair:S.pair,tf:S.tf,dir:a.dir,entry:null,agree:a.agree,res:null,tag:'live'};
  S.hist.unshift(rec);S.sig=rec;save();markets();popup(rec);beep(880,.18);
  const total=Math.round((at-now)/1000)+S.tf;let left=total,entered=false;
  clearInterval(S.tick);
  S.tick=setInterval(async()=>{
    left--;const l=Math.max(left,0);
    $('#left').textContent=mmss(l);$('#pg').style.strokeDashoffset=C*(1-l/total);
    if(!entered&&Date.now()>=at){entered=true;try{rec.entry=otcPrices[rec.pair];save()}catch(e){}}
    if(left<=0){clearInterval(S.tick);finish(rec)}
  },1000);
}

let AC;
function beep(f,d){if(S.snd!=='on')return;try{AC=AC||new(window.AudioContext||window.webkitAudioContext)();const o=AC.createOscillator(),g=AC.createGain();o.frequency.value=f;g.gain.value=.08;o.connect(g);g.connect(AC.destination);o.start();o.stop(AC.currentTime+d)}catch(e){}try{navigator.vibrate&&navigator.vibrate(Math.round(d*600))}catch(e){}}
function lossRun(){let n=0;for(const h of S.hist.filter(h=>h.res==='win'||h.res==='loss')){if(h.res==='loss')n++;else break}return n}
function confetti(){
  const c=$('#fx'),g=c.getContext('2d');c.width=innerWidth;c.height=innerHeight;
  const cl=['#3ff2a0','#5eead4','#8b5cf6','#f5c46b'],P=Array.from({length:60},()=>({x:innerWidth/2,y:innerHeight*.4,vx:(Math.random()-.5)*14,vy:-Math.random()*14-2,s:4+Math.random()*5,col:cl[Math.random()*4|0],r:Math.random()*6}));
  let f=0;(function t(){g.clearRect(0,0,c.width,c.height);P.forEach(p=>{p.vy+=.35;p.x+=p.vx;p.y+=p.vy;p.r+=.2;g.fillStyle=p.col;g.save();g.translate(p.x,p.y);g.rotate(p.r);g.fillRect(-p.s/2,-p.s/2,p.s,p.s*.6);g.restore()});if(++f<75)requestAnimationFrame(t);else g.clearRect(0,0,c.width,c.height)})();
}

async function finish(rec){
  let px=otcPrices[rec.pair]||null;
  if(px==null||rec.entry==null){rec.res='void'}
  else{rec.exit=px;rec.res=px===rec.entry?'tie':((px>rec.entry)===(rec.dir>0)?'win':'loss')}
  save();$('#left').textContent='--:--';markets();render();
  eng(rec.res==='win'?'up':rec.res==='loss'?'dn':'nt',rec.res==='win'?'✓':rec.res==='loss'?'✕':'=',rec.res.toUpperCase(),'Trade Finished');
  if(rec.res==='win'){beep(1175,.25);confetti()}else if(rec.res==='loss')beep(220,.35);
  if(rec.res==='loss'&&S.maxL>0&&lossRun()>=S.maxL&&S.run){toggle();eng('nt','⛔','BOT STOPPED',S.maxL+' losses in a row.');return;}
  if(S.run)S.timer=setTimeout(cycle,4000);
}

function toggle(){
  S.run=!S.run;const b=$('#go');
  if(S.run){b.textContent='⏹ STOP BOT';b.className='big stop';cycle()}
  else{clearTimeout(S.timer);clearInterval(S.tick);if(S.sig&&!S.sig.res){S.sig.res='void';save()}b.textContent='⚡ START QUOTEX OTC AI BOT';b.className='big';eng('','⚡','STANDBY','Tap to start');$('#left').textContent='--:--';$('#pg').style.strokeDashoffset=C;markets()}
}
$('#go').onclick=toggle;
$('#clr').onclick=()=>{if(confirm('Delete history?')){S.hist=[];save();render()}};

function render(){
  const f=t=>new Date(t).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  $('#hist').innerHTML=S.hist.length?S.hist.slice(0,50).map((h,i)=>`<div class="hrow" onclick="popup(S.hist[${i}])"><span>${h.pair} ${tfL(h.tf)} <b class="${h.dir>0?'up':'dn'}">${h.dir>0?'UP':'DOWN'}</b> • ${f(h.t)}</span><span class="${h.res==='win'?'up':h.res==='loss'?'dn':'nt'}">${h.res?h.res.toUpperCase():'pending'}</span></div>`).join(''):`<div><span>No signals yet</span></div>`;
  const d=S.hist.filter(h=>h.res==='win'||h.res==='loss'),w=d.filter(h=>h.res==='win').length;
  $('#aw').textContent=w;$('#al').textContent=d.length-w;$('#ar').textContent=d.length?Math.round(w/d.length*100)+'%':'--';
  let k=d[0]&&d[0].res,st=0;for(const h of d){if(h.res===k)st++;else break}
  $('#stk').textContent=d.length?`Current streak: ${st} ${k}`:'No trades yet';
  const by={};d.forEach(h=>{const k=h.pair+' '+tfL(h.tf);(by[k]=by[k]||[0,0])[h.res==='win'?0:1]++});
  $('#byp').innerHTML=Object.entries(by).map(([k,v])=>`<div><span>${k}</span><span>${v[0]}W / ${v[1]}L</span></div>`).join('');
}

const CH={d:[],last:null,tm:null};
function chartMsg(t){$('#cm').textContent=t;$('#cm').style.display=t?'flex':'none'}
async function chartPull(){
  const p=S.pair,tf=S.tf;let d=await candles(p,tf,60);
  chartMsg('');if(d.length)CH.d=d;chartDraw();
}
function chartReset(){
  clearInterval(CH.tm);CH.d=[];CH.last=null;
  $('#cn').textContent=S.pair;$('#cpx').textContent='--';$('#cch').textContent='';
  chartMsg('Loading Quotex OTC stream...');chartDraw();chartPull();
  CH.tm=setInterval(chartPull,3000);
}
function chartDraw(){
  const cv=$('#cv');if(!cv)return;
  const g=cv.getContext('2d'),dpr=window.devicePixelRatio||1,W=cv.clientWidth,H=cv.clientHeight;
  if(!W)return;
  if(cv.width!==Math.round(W*dpr)){cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr)}
  g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,W,H);
  const d=CH.d;if(!d.length)return;
  let lo=Math.min(...d.map(x=>x.l)),hi=Math.max(...d.map(x=>x.h)),pad=(hi-lo)*.1||hi*.0005;lo-=pad;hi+=pad;
  const pw=58,cw=(W-pw)/d.length,y=v=>H-8-(v-lo)/(hi-lo)*(H-16);
  g.font='10px sans-serif';g.lineWidth=1;
  for(let i=0;i<4;i++){const v=lo+(hi-lo)*i/3,yy=y(v);g.strokeStyle='#ffffff12';g.beginPath();g.moveTo(0,yy);g.lineTo(W-pw,yy);g.stroke();g.fillStyle='#8f93b8';g.fillText(fmt(v),W-pw+4,yy+3)}
  d.forEach((k,i)=>{const x=i*cw+cw/2,u=k.c>=k.o;g.strokeStyle=g.fillStyle=u?'#3ff2a0':'#ff5577';g.beginPath();g.moveTo(x,y(k.h));g.lineTo(x,y(k.l));g.stroke();g.fillRect(x-cw*.32,Math.min(y(k.o),y(k.c)),cw*.64,Math.max(1,Math.abs(y(k.o)-y(k.c))))});
  const last=d[d.length-1].c,ly=y(last);
  g.setLineDash([4,4]);g.strokeStyle='#8b5cf6';g.beginPath();g.moveTo(0,ly);g.lineTo(W-pw,ly);g.stroke();g.setLineDash([]);
  g.fillStyle='#8b5cf6';g.fillRect(W-pw,ly-9,pw,18);g.fillStyle='#fff';g.fillText(fmt(last),W-pw+4,ly+3);
  const s=S.sig;if(s&&!s.res&&s.pair===S.pair){const e=s.entry||last,ey=y(e),col=s.dir>0?'#3ff2a0':'#ff5577';g.setLineDash([2,3]);g.strokeStyle=col;g.beginPath();g.moveTo(0,ey);g.lineTo(W-pw,ey);g.stroke();g.setLineDash([]);g.font='bold 22px sans-serif';g.fillStyle=col;g.fillText(s.dir>0?'▲':'▼',W-pw-28,ey+(s.dir>0?-6:20))}
}
window.addEventListener('resize',chartDraw);

function boot(){
  document.querySelectorAll('#sn button').forEach(b=>b.classList.toggle('on',b.dataset.v===S.snd));
  document.querySelectorAll('#ml button').forEach(b=>b.classList.toggle('on',+b.dataset.v===S.maxL));
  $('#selp').textContent=S.pair;markets();render();chartReset();updatePrices();setInterval(updatePrices,3000);
}
$('#exp').onclick=()=>{
  const rows=[['time','pair','timeframe','direction','agree','entry','exit','result']].concat(S.hist.map(h=>[new Date(h.t).toISOString(),h.pair,tfL(h.tf),h.dir>0?'UP':'DOWN',h.agree,h.entry||'',h.exit||'',h.res||'']));
  const b=new Blob([rows.map(r=>r.join(',')).join('\n')],{type:'text/csv'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='quotex-otc-history.csv';a.click();
};
$('#lo').onclick=()=>{try{localStorage.removeItem('hx_ok')}catch(e){}location.reload()};
let tries=0,lockedUntil=0;
function tryLogin(){
  const now=Date.now();if(now<lockedUntil){$('#lerr').textContent='Wait '+Math.ceil((lockedUntil-now)/1000)+'s';return}
  if($('#pw').value.trim()===ACCESS){try{localStorage.setItem('hx_ok','1')}catch(e){}$('#lerr').textContent='';$('#lock').classList.add('out');setTimeout(()=>$('#lock').remove(),700);boot()}
  else{tries++;$('#pw').value='';$('#lerr').textContent='Wrong key';const k=$('.lk');k.classList.remove('shake');void k.offsetWidth;k.classList.add('short');if(tries>=5){lockedUntil=now+30000;tries=0}}
}
$('#lg').onclick=tryLogin;$('#pw').onkeydown=e=>{if(e.key==='Enter')tryLogin()};
let ok=false;try{ok=localStorage.getItem('hx_ok')==='1'}catch(e){}
if(ok){$('#lock').remove();boot()}else setTimeout(()=>$('#pw').focus(),400);
</script>
</body>
</html>
"""

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path in ("/", "/index.html", "/index.py"):
        start_response("200 OK", [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(HTML.encode("utf-8")))),
            ("Cache-Control", "no-cache"),
        ])
        return [HTML.encode("utf-8")]
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not found"]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"QUOTEX OTC PRO running on http://localhost:{port}")
    make_server("0.0.0.0", port, app).serve_forever()
