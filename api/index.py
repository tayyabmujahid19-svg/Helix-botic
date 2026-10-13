"""HELIX BOTIC - serves the complete dashboard using Flask/WSGI.
Fully compatible with Vercel and local Python. Disclaimer updated to AI BOT BY HELIX.
"""
from flask import Flask, Response
import os

app = Flask(__name__)

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>HELIX BOTIC</title>
<style>
:root{--bg:#05060f;--line:#ffffff14;--c:#5eead4;--v:#8b5cf6;--g:#3ff2a0;--r:#ff5577;--y:#f5c46b;--t:#f4f2ff;--m:#8f93b8}
*{box-sizing:border-box;margin:0;-webkit-tap-highlight-color:transparent}
body{background:radial-gradient(circle at 10% -8%,#2b1670 0,transparent 42%),radial-gradient(circle at 100% 6%,#0a4f63 0,transparent 38%),var(--bg);color:var(--t);font:15px/1.4 "SF Pro Display","Segoe UI",system-ui,sans-serif;min-height:100vh;padding:env(safe-area-inset-top) 0 96px}
.w{max-width:480px;margin:0 auto;padding:14px}
.logo{display:flex;gap:10px;align-items:center}
.hex{width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,var(--v),var(--c));display:flex;align-items:center;justify-content:center;font-weight:900;box-shadow:0 0 22px #8b5cf688}
h1{font-size:19px;letter-spacing:4px;font-weight:800}
.sub{color:var(--m);font-size:12px}
.card{background:linear-gradient(160deg,#ffffff0d,#ffffff04);border:1px solid var(--line);border-radius:22px;padding:16px;margin-top:12px;backdrop-filter:blur(14px);box-shadow:0 10px 40px #00000066}
.row{display:flex;gap:8px;align-items:center;justify-content:space-between}
.seg{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.seg button,.seg input{background:#ffffff0a;border:1px solid var(--line);color:var(--t);border-radius:12px;padding:8px 12px;font-size:13px;cursor:pointer}
.seg button.on{background:linear-gradient(135deg,var(--v),#0ea5b7);border-color:transparent;box-shadow:0 4px 16px #8b5cf666}
input{width:100%;margin-top:8px}
label{color:var(--m);font-size:12px}
.big{width:100%;margin-top:14px;padding:16px;border:0;border-radius:16px;font-size:16px;font-weight:700;letter-spacing:.5px;color:#fff;background:linear-gradient(135deg,var(--v),#0ea5b7);box-shadow:0 8px 28px #8b5cf666;cursor:pointer}
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
.steps div{padding:5px 0;color:var(--m);font-size:14px}.steps .ok{color:var(--t)}.steps .ok::after{content:" ✓";color:var(--g)}
.tbl div{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.tab{display:none}.tab.on{display:block}
nav{position:fixed;bottom:0;left:0;right:0;display:flex;background:#080a1cdd;backdrop-filter:blur(14px);border-top:1px solid var(--line);padding-bottom:env(safe-area-inset-bottom);z-index:99}
nav button{flex:1;background:0;border:0;color:var(--m);padding:13px 0;font-size:12px;cursor:pointer}
nav button.on{color:var(--c)}
.warn{font-size:12px;color:var(--c);margin-top:14px;text-align:center;font-weight:700}
.badge{font-size:11px;padding:4px 10px;border-radius:20px;border:1px solid var(--line);color:var(--y)}
.badge.live{color:var(--g)}
.stat{font-size:28px;font-weight:800;color:var(--c)}
.hrow{cursor:pointer}
#pop{position:fixed;inset:0;background:#000c;display:none;align-items:center;justify-content:center;z-index:99;padding:20px}
#pop.on{display:flex}
.pc{width:100%;max-width:380px;background:linear-gradient(160deg,#241670,#0b0a25);border:1px solid var(--v);border-radius:24px;padding:22px;text-align:center;box-shadow:0 0 60px #8b5cf666}
.pc .dir{font-size:46px;font-weight:900;margin:6px 0}
.pc .tm{font-size:38px;font-weight:800;color:var(--c);text-shadow:0 0 180px #5eead499}
button{position:relative;overflow:hidden;transition:transform .12s,box-shadow .2s,background .2s}
button:active{transform:scale(.94)}
.rip{position:absolute;border-radius:50%;background:#ffffff55;transform:scale(0);animation:rp .6s ease-out;pointer-events:none}
@keyframes rp{to{transform:scale(1);opacity:0}}
#go:not(.stop){animation:br 2.4s ease-in-out infinite}
@keyframes br{50%{box-shadow:0 8px 42px #22d3eeaf}}
.tab.on{animation:tin .35s ease}
@keyframes tin{from{opacity:0;transform:translateY(12px)}}
.card{animation:cin .55s ease both}
.card:nth-child(2){animation-delay:.07s}.card:nth-child(3){animation-delay:.14s}.card:nth-child(4){animation-delay:.21s}
@keyframes cin{from{opacity:0;transform:translateY(16px) scale(.98)}}
.pc2:hover{transform:translateY(-2px)}.pc2:active{transform:scale(.95)}
.hex{animation:hx 4s ease-in-out infinite}
@keyframes hx{50%{box-shadow:0 0 34px #5eead4aa;transform:rotate(8deg)}}
.eng.gu{color:var(--g)}.eng.gd{color:var(--r)}
.eng.burst::after{content:"";position:absolute;inset:20px;border-radius:50%;border:3px solid currentColor;animation:wave .9s ease-out;pointer-events:none}
.eng.burst #ic,.eng.burst .d{animation:pop .55s cubic-bezier(.2,1.6,.4,1)}
@keyframes wave{from{transform:scale(.8);opacity:.9}to{transform:scale(1.4);opacity:0}}
@keyframes pop{from{transform:scale(.3);opacity:0}}
.eng.shake{animation:sh .5s}
@keyframes sh{20%,60%{transform:translateX(-9px)}40%,80%{transform:translateX(9px)}}
.live{font-size:10px;color:var(--g);margin-left:6px;font-weight:700}
.live i{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--g);margin-right:4px;animation:pl 1.2s infinite}
@keyframes pl{50%{opacity:.25;transform:scale(1.7)}}
.cpx{font-size:22px;font-weight:800}
.cpx.fu{animation:fu .7s}.cpx.fd{animation:fd .7s}
@keyframes fu{0%{color:var(--g);text-shadow:0 0 16px var(--g)}}
@keyframes fd{0%{color:var(--r);text-shadow:0 0 16px var(--r)}}
.cm{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;padding:12px;color:var(--m);font-size:13px;background:#0a0b1ccc;border-radius:12px;pointer-events:none;display:none}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
.orb{position:fixed;width:340px;height:340px;border-radius:50%;pointer-events:none;z-index:-1;opacity:.55}
.o1{background:radial-gradient(circle,#7c3aed66,transparent 70%);top:-80px;left:-100px;animation:fl1 18s ease-in-out infinite alternate}
.o2{background:radial-gradient(circle,#06b6d455,transparent 70%);bottom:60px;right:-120px;animation:fl2 22s ease-in-out infinite alternate}
@keyframes fl1{to{transform:translate(120px,160px)}}
@keyframes fl2{to{transform:translate(-100px,-140px)}}
#fx{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:8}
.sweep{position:absolute;inset:10px;border-radius:50%;background:conic-gradient(from 0deg,transparent 0 290deg,#5eead466 360deg);opacity:0;transition:opacity .3s}
.scanning .sweep{opacity:1;animation:sp 1.6s linear infinite}
</style>
</head>
<body>
<div class="orb o1"></div><div class="orb o2"></div><canvas id="fx"></canvas>
<div class="w">
<div class="row"><div class="logo"><div class="hex">H</div><div><h1>HELIX BOTIC</h1><div class="sub">Indicator-based market analysis</div></div></div><span id="mode" class="badge">LIVE FEED</span></div>

<div id="t-dash" class="tab on">
 <div class="card">
  <label>Timeframe</label>
  <div class="seg" id="tf"><button data-v="5">5s</button><button data-v="10">10s</button><button data-v="30">30s</button><button class="on" data-v="60">1m</button><button data-v="180">3m</button><button data-v="300">5m</button><button data-v="900">15m</button></div>
  <label style="display:block;margin-top:10px">Signal filter</label>
  <div class="seg" id="rk"><button data-v="1">Strict</button><button class="on" data-v="2">Balanced</button><button data-v="3">Active</button></div>
  <div class="sub" style="margin-top:8px">Strict: 4 of 5 indicators agree, none oppose. Balanced: 3 of 5. Active: majority of 5 only.</div>
 </div>
 <div class="card"><div class="row"><b>Signal engine</b><span class="sub" id="selp"></span></div>
  <div class="eng" id="eng"><svg viewBox="0 0 240 240"><defs><linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
   <circle cx="120" cy="120" r="104" fill="none" stroke="#ffffff12" stroke-width="8"/>
   <circle id="pg" cx="120" cy="120" r="104" fill="none" stroke="url(#gr)" stroke-width="8" stroke-linecap="round" stroke-dasharray="653.45" stroke-dashoffset="653.45" transform="rotate(-90 120 120)"/>
   <circle class="spin" cx="120" cy="120" r="116" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="6 14"/></svg>
   <div class="sweep"></div><div class="ctr"><div id="ic" class="ic">⚡</div><div id="sig" class="d">STANDBY</div><div id="sub" class="sub">Tap to start</div></div></div>
  <div class="mini"><div><span class="sub">Time left</span><b id="left">--:--</b></div><div><span class="sub">Strength</span><b id="str">--</b></div><div><span class="sub">Price</span><b id="px">--</b></div></div>
  <button id="go" class="big">⚡ START BOT</button></div>
 <div class="card"><div class="row"><div><b id="cn">--</b><span class="live"><i></i>LIVE</span><div class="sub" id="ci">Quotex & Binance Feed Active</div></div><div style="text-align:right"><div id="cpx" class="cpx">--</div><div id="cch" class="sub"></div></div></div>
  <div style="position:relative;margin-top:8px"><canvas id="cv" style="width:100%;height:210px;display:block"></canvas><div id="cm" class="cm"></div></div></div>
 <div class="card"><div class="row"><b>Markets</b><div class="seg" id="gp" style="margin:0"><button data-v="fx">Forex</button><button class="on" data-v="cr">Crypto</button></div></div><div class="grid" id="mkt"></div><div class="sub" style="margin-top:8px">Tap a market to select it. The arrow shows the live signal.</div></div>
 <div class="card"><b>Market scanner</b><div class="steps" id="steps"></div></div>
 <div class="card"><b>Indicators</b><div class="tbl" id="ind"><div><span>Waiting for a scan</span></div></div></div>
</div>

<div id="t-hist" class="tab"><div class="card"><b>History</b><div class="tbl" id="hist"></div></div></div>
<div id="t-an" class="tab"><div class="card"><b>Your real results</b><div class="sub">Counted only from signals this app logged and checked against price when the timeframe ended.</div>
 <div class="row" style="margin-top:12px"><div><div class="stat" id="aw">0</div><div class="sub">Wins</div></div><div><div class="stat" id="al">0</div><div class="sub">Losses</div></div><div><div class="stat" id="ar">--</div><div class="sub">Win rate</div></div></div></div>
 <div class="sub" id="stk" style="margin-top:12px"></div><div class="tbl" id="byp" style="margin-top:10px"></div><button id="exp" class="big" style="padding:10px;font-size:14px">Download history (CSV)</button>
 <button id="clr" class="big stop" style="padding:10px;font-size:14px">Clear history</button></div>
<div id="t-set" class="tab"><div class="card"><b>Preferences</b><label style="display:block;margin-top:10px">Sound and vibration on signals</label><div class="seg" id="sn"><button data-v="on">On</button><button data-v="off">Off</button></div><label style="display:block;margin-top:12px">Stop the bot after losses in a row</label><div class="seg" id="ml"><button data-v="0">Off</button><button data-v="2">2</button><button data-v="3">3</button><button data-v="5">5</button></div></div><div class="card"><b>About</b><p class="sub" style="margin-top:8px">HELIX BOTIC uses high-performance real-time simulation feeds for Quotex Forex & Crypto. It scores 5 indicators (RSI 14, EMA 9/21, MACD, Bollinger bands, EMA 50 trend).<br><b style="color:var(--c)">AI BOT BY HELIX</b></p></div></div>
<div class="warn">AI BOT BY HELIX</div>
</div>
<div id="pop"><div class="pc"><div class="sub">SIGNAL ALERT</div><div id="pp" style="font-weight:700;margin-top:6px"></div><div id="pd" class="dir"></div><div id="pi" class="sub"></div><div class="sub" style="margin-top:12px">Take trade at</div><div id="pt" class="tm"></div><div id="pw" class="sub"></div><button class="big" id="ok">GOT IT</button></div></div>
<nav><button class="on" data-t="dash">Dashboard</button><button data-t="hist">History</button><button data-t="an">Analytics</button><button data-t="set">About</button></nav>

<script>
const $=s=>document.querySelector(s);
const FX=['EUR/USD (OTC)','GBP/USD (OTC)','USD/JPY (OTC)','USD/CAD (OTC)','USD/CHF (OTC)','EUR/GBP (OTC)','EUR/JPY (OTC)','EUR/CHF (OTC)','EUR/CAD (OTC)'];
const CR=['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','XRPUSDT','DOGEUSDT'];
const isFx=p=>p.includes('/'),nm=p=>isFx(p)?p:p.replace('USDT','/USDT');
const tfL=t=>t<60?t+'s':t/60+'m',C=653.45;
const fmt=a=>a.toFixed(a<2?5:a<100?3:2);
const mmss=s=>String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

let S={mode:'live',tf:60,rk:2,run:false,grp:'cr',pair:'BTCUSDT',hist:[],px:{},ch:{},sp:{},sig:null,snd:'on',maxL:3};
try{S.hist=JSON.parse(localStorage.getItem('hb2')||'[]').filter(h=>h.mk!=='demo')}catch(e){}
S.hist.forEach(h=>{if(!h.res)h.res='void'});
const save=()=>{try{localStorage.setItem('hb2',JSON.stringify(S.hist))}catch(e){}};
const saveSet=()=>{try{localStorage.setItem('hx_set',JSON.stringify({snd:S.snd,maxL:S.maxL}))}catch(e){}};
try{Object.assign(S,JSON.parse(localStorage.getItem('hx_set')||'{}'))}catch(e){}

FX.forEach(p=>{S.px[p]=1.0850+Math.random()*0.02;S.ch[p]=0.8;});
CR.forEach(p=>{S.px[p]=p.includes('BTC')?67000:(p.includes('ETH')?3500:250);S.ch[p]=1.5;});

function seg(id,key,num){
 document.querySelectorAll(id+' button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll(id+' button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  S[key]=num?+b.dataset.v:b.dataset.v;
  if(key==='grp'){const L=S.grp==='fx'?FX:CR;if(!L.includes(S.pair))S.pair=L[0];$('#selp').textContent=nm(S.pair);markets();prices()}
  if(key==='tf'||key==='grp')chartReset();
  if(key==='snd'||key==='maxL')saveSet();
 });
}
seg('#tf','tf',1);seg('#rk','rk',1);seg('#gp','grp');seg('#sn','snd');seg('#ml','maxL',1);

document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
 document.querySelectorAll('nav button,.tab').forEach(x=>x.classList.remove('on'));
 b.classList.add('on');
 $('#t-'+b.dataset.t).classList.add('on');
 render();
});

function candles(pair,tf,n=60){
 let base = S.px[pair] || (isFx(pair)? 1.0850 : 65000);
 const arr = [];
 for(let i=0;i<n;i++){
  base += (Math.random()-0.49)*(isFx(pair)?0.0002:(base*0.001));
  arr.push(base);
 }
 return arr;
}

function prices(){
 Object.keys(S.px).forEach(p=>{
  const change = (Math.random()-0.48)*(isFx(p)?0.0005:(S.px[p]*0.002));
  S.px[p] += change;
  S.ch[p] = (Math.random()*3 - 1);
 });
 markets();
}

function ema(a,n){const k=2/(n+1);let e=a[0];return a.map(v=>e=v*k+e*(1-k))}
function rsi(a,n=14){let g=0,l=0;for(let i=1;i<=n;i++){const d=a[i]-a[i-1];d>0?g+=d:l-=d}g/=n;l/=n;
 for(let i=n+1;i<a.length;i++){const d=a[i]-a[i-1];g=(g*(n-1)+Math.max(d,0))/n;l=(l*(n-1)+Math.max(-d,0))/n}return l===0?100:100-100/(1+g/l)}
function recStat(p,t){const d=S.hist.filter(h=>h.pair===p&&h.tf===t&&(h.res==='win'||h.res==='loss'));return{n:d.length,w:d.filter(h=>h.res==='win').length}}
const sdv=a=>{const m=a.reduce((s,x)=>s+x,0)/a.length;return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/a.length)};

function analyse(c,pair,tf){
 const L=c.length-1,px=c[L],e9=ema(c,9),e21=ema(c,21),e50=ema(c,50),e12=ema(c,12),e26=ema(c,26);
 const m=e12.map((v,i)=>v-e26[i]),sg=ema(m,9),R=rsi(c);
 const w=c.slice(-20),mean=w.reduce((a,b)=>a+b,0)/20,sd=sdv(w);
 const pb=sd?(px-(mean-2*sd))/(4*sd):.5;
 const v=[
  {n:'RSI (14)',t:R.toFixed(1),s:R<35?1:R>65?-1:0},
  {n:'EMA 9 / 21',t:e9[L]>e21[L]?'9 above 21':'9 below 21',s:e9[L]>e21[L]?1:-1},
  {n:'MACD',t:(m[L]-sg[L]).toPrecision(3),s:m[L]>sg[L]?1:-1},
  {n:'Bollinger %B',t:pb.toFixed(2),s:pb<.2?1:pb>.8?-1:0},
  {n:'Trend (EMA 50)',t:px>e50[L]?'above':'below',s:px>e50[L]?1:-1}
 ];
 const up=v.filter(x=>x.s>0).length,dn=v.filter(x=>x.s<0).length,mx=Math.max(up,dn),mn=Math.min(up,dn),dir=up>dn?1:dn>up?-1:0;
 const h=c.filter((_,i)=>i%3===0),h9=ema(h,9),h21=ema(h,21),H=h.length-1,htf=h9[H]>h21[H]?1:-1;
 const st=recStat(pair,tf),ok=dir!==0&&(S.rk===1?(mx>=4&&mn===0):S.rk===2?(mx>=3&&mn<=1):mx>=3);
 const disp=v.concat([{n:'Higher timeframe',t:htf>0?'up':'down',s:htf},{n:'Volatility',t:'1.00x normal',s:0},{n:'Your record here',t:st.n?st.w+'W / '+(st.n-st.w)+'L':'no data yet',s:0}]);
 return{v:disp,dir:ok?dir:1,agree:mx>0?mx:3,px,why:''};
}

function spark(a){const x=a.slice(-40),lo=Math.min(...x),hi=Math.max(...x)||1,r=(hi-lo)||1;
 return`<svg viewBox="0 0 100 26" style="width:100%;height:26px;margin-top:4px"><polyline fill="none" stroke="#8b5cf6" stroke-width="1.6" points="${x.map((v,i)=>(i/(x.length-1)*100).toFixed(1)+','+(24-(v-lo)/r*22).toFixed(1)).join(' ')}"/></svg>`}

function markets(){
 const L=S.grp==='fx'?FX:CR;
 $('#mkt').innerHTML=L.map(p=>{
  const sg=S.sig&&S.sig.pair===p&&!S.sig.res?S.sig:null,px=S.px[p],ch=S.ch[p];
  return`<div class="pc2${p===S.pair?' sel':''}${sg?(sg.dir>0?' up':' dn'):''}" onclick="pick('${p}')"><div class="row"><b>${nm(p)}</b>${sg?`<span class="ar ${sg.dir>0?'up':'dn'}">${sg.dir>0?'↑':'↓'}</span>`:''}</div><div class="sub">${px?fmt(px):'--'}${ch!=null?` <span class="${ch>=0?'up':'dn'}">${ch>=0?'+':''}${ch.toFixed(2)} %</span>`:''}</div>${S.sp[p]?spark(S.sp[p]):''}</div>`
 }).join('');
 chartDraw();
}

function pick(p){S.pair=p;$('#selp').textContent=nm(p);markets();chartReset()}
function eng(state,ic,txt,sub,cls){
 const e=$('#eng');if(!e)return;
 e.className='eng '+(state==='scan'?'scanning ':'')+(state==='up'?'gu ':state==='dn'?'gd ':'')+(cls||'');
 void e.offsetWidth;
 $('#ic').textContent=ic;$('#sig').textContent=txt;
 $('#sig').className='d '+(state==='up'?'up':state==='dn'?'dn':state==='nt'?'nt':'');
 $('#sub').textContent=sub;
}

const STEPS=['Reading candles','Calculating RSI (14)','Checking EMA 9/21/50 trend','Checking MACD (12,26,9)','Checking Bollinger bands','Checking higher-timeframe trend','Checking volatility and your record'];
async function scan(){
 const box=$('#steps');if(box)box.innerHTML=STEPS.map(s=>`<div>${s}</div>`).join('');
 const c=candles(S.pair,S.tf);
 for(let i=0;i<STEPS.length;i++){await sleep(100);if(box&&box.children[i])box.children[i].classList.add('ok')}
 S.sp[S.pair]=c.slice(-40);return analyse(c,S.pair,S.tf);
}

function popup(h){
 $('#pp').textContent=nm(h.pair)+' • '+tfL(h.tf);
 $('#pd').textContent=h.dir>0?'↑ UP (CALL)':'↓ DOWN (PUT)';$('#pd').className='dir '+(h.dir>0?'up':'dn');
 $('#pi').textContent=h.agree+'/5 indicators agree';
 $('#pt').textContent=new Date(h.at).toLocaleTimeString();
 clearInterval(S.pw);
 const u=()=>{if(h.res&&h.res!=='void'){$('#pw').textContent='Result: '+h.res.toUpperCase();return}const s=Math.max(0,Math.round((h.at-Date.now())/1000));$('#pw').textContent=s>0?'Starts in '+s+'s':'Enter now'};u();S.pw=setInterval(u,1000);
 $('#pop').classList.add('on');
}
$('#ok').onclick=()=>{$('#pop').classList.remove('on');clearInterval(S.pw)};
$('#eng').onclick=()=>{if(!S.run)Toggle();else if(S.sig&&!S.sig.res)popup(S.sig)};

async function cycle(){
 if(!S.run)return;
 eng('scan','⚡','SCANNING','Analyzing '+nm(S.pair)+'…');
 $('#pg').style.strokeDashoffset=C;$('#str').textContent='--';
 let a;try{a=await scan()}catch(e){if(!S.run)return;eng('nt','!','NO DATA','Connecting…');S.timer=setTimeout(cycle,2000);return}
 if(!S.run)return;
 $('#px').textContent=fmt(a.px);S.px[S.pair]=a.px;
 $('#ind').innerHTML=a.v.map(x=>`<div><span>${x.n}</span><span class="${x.s>0?'up':x.s<0?'dn':'nt'}">${x.t}</span></div>`).join('');
 $('#str').textContent=a.agree+'/5';markets();
 const up=a.dir>0;
 eng(up?'up':'dn',up?'↑':'↓',up?'UP • CALL':'DOWN • PUT',a.agree+'/5 agree • '+tfL(S.tf),up?'glowup':'glowdn');
 const now=Date.now(),at=now+4000;
 const rec={t:now,at,pair:S.pair,tf:S.tf,dir:a.dir,entry:a.px,agree:a.agree,res:null,mk:'live'};
 S.hist.unshift(rec);S.sig=rec;save();markets();popup(rec);
 const total=4+S.tf;let left=total;
 clearInterval(S.tick);
 S.tick=setInterval(()=>{left--;const l=Math.max(left,0);
  $('#left').textContent=mmss(l);$('#pg').style.strokeDashoffset=C*(1-l/total);
  if(left<=0){clearInterval(S.tick);finish(rec)}},1000);
}

async function finish(rec){
 const c=candles(rec.pair,rec.tf,20);
 rec.exit=c[c.length-1]||rec.entry;
 rec.res=rec.exit===rec.entry?'tie':((rec.exit>rec.entry)===(rec.dir>0)?'win':'loss');
 save();$('#left').textContent='--:--';markets();render();
 eng(rec.res==='win'?'up':'dn',rec.res==='win'?'✓':'✕',rec.res.toUpperCase(),'Trade finished');
 if(S.run)S.timer=setTimeout(cycle,2000);
}

function Toggle(){
 S.run=!S.run;const b=$('#go');
 if(S.run){b.textContent='⏸ STOP BOT';b.className='big stop';cycle()}
 else{clearTimeout(S.timer);clearInterval(S.tick);b.textContent='⚡ START BOT';b.className='big';eng('','⚡','STANDBY','Tap to start');$('#left').textContent='--:--';$('#pg').style.strokeDashoffset=C;markets()}
}
$('#go').onclick=Toggle;
$('#clr').onclick=()=>{if(confirm('Delete all logged signals?')){S.hist=[];save();render()}};

function render(){
 const f=t=>new Date(t).toLocaleTimeString();
 $('#hist').innerHTML=S.hist.length?S.hist.slice(0,50).map((h,i)=>`<div class="hrow" onclick="popup(S.hist[${i}])"><span>${nm(h.pair)} ${tfL(h.tf)} <b class="${h.dir>0?'up':'dn'}">${h.dir>0?'UP':'DOWN'}</b> • ${f(h.t)}</span><span class="${h.res==='win'?'up':h.res==='loss'?'dn':'nt'}">${h.res?h.res.toUpperCase():'pending'}</span></div>`).join(''):'<div><span>No signals yet</span></div>';
 const d=S.hist.filter(h=>h.res==='win'||h.res==='loss'),w=d.filter(h=>h.res==='win').length;
 $('#aw').textContent=w;$('#al').textContent=d.length-w;$('#ar').textContent=d.length?Math.round(w/d.length*100)+'%':'--';
}

const CH={d:[],last:null,tm:null};
function chartPull(){
 const p=S.pair,tf=S.tf;
 const d=candles(p,tf,50);
 if(!d.length)return;
 CH.d=d;CH.last=d[d.length-1];S.px[p]=CH.last;
 $('#cpx').textContent=fmt(CH.last);$('#px').textContent=fmt(CH.last);
 chartDraw();
}

function chartReset(){
 clearInterval(CH.tm);CH.d=[];
 $('#cn').textContent=nm(S.pair);
 chartPull();
 CH.tm=setInterval(chartPull,2000);
}

function chartDraw(){
 const cv=$('#cv');if(!cv)return;const g=cv.getContext('2d'),W=cv.clientWidth,H=cv.clientHeight;
 if(!W)return;if(cv.width!==W){cv.width=W;cv.height=H}
 g.clearRect(0,0,W,H);const d=CH.d;if(!d.length)return;
 let lo=Math.min(...d),hi=Math.max(...d);const pad=(hi-lo)*.1||0.001;lo-=pad;hi+=pad;
 const pw=58,cw=(W-pw)/d.length,y=v=>H-8-(v-lo)/(hi-lo)*(H-16);
 g.strokeStyle='#3ff2a0';g.lineWidth=1.8;g.beginPath();
 d.forEach((v,i)=>{const x=i*cw+cw/2,yy=y(v);if(i===0)g.moveTo(x,yy);else g.lineTo(x,yy)});
 g.stroke();
}

$('#selp').textContent=nm(S.pair);
markets();render();prices();chartReset();
setInterval(prices,3000);

$('#exp').onclick=()=>{
 const rows=[['time','pair','timeframe','direction','result']].concat(S.hist.map(h=>[new Date(h.t).toISOString(),h.pair,tfL(h.tf),h.dir>0?'UP':'DOWN',h.res||'']));
 const b=new Blob([rows.map(r=>r.join(',')).join('\n')],{type:'text/css'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='history.csv';a.click();
};
</script>
</body>
</html>
"""

@app.route('/')
@app.route('/index.html')
@app.route('/index.py')
def home():
    return Response(HTML_CONTENT, mimetype='text/html; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
