from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>HELIX BOTICS</title>
<style>
@property --cyan{syntax:"<color>";inherits:true;initial-value:#22d3ee}@property --purple{syntax:"<color>";inherits:true;initial-value:#8b5cf6}@property --bg{syntax:"<color>";inherits:true;initial-value:#050816}@property --bg2{syntax:"<color>";inherits:true;initial-value:#0f1a3d}
:root{--bg2:#0f1a3d;transition:--cyan .8s,--purple .8s,--bg .8s,--bg2 .8s;--bg:#050816;--card:rgba(14,22,44,.72);--line:rgba(120,150,220,.18);--cyan:#22d3ee;--purple:#8b5cf6;--green:#34d399;--red:#fb7185;--gold:#fbbf24;--txt:#f1f5f9;--mut:#8b98b8}
*{box-sizing:border-box;margin:0;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
body{background:radial-gradient(120% 80% at 50% 0%,var(--bg2) 0%,var(--bg) 60%);color:var(--txt);font-family:system-ui,"Segoe UI",sans-serif;overflow-x:hidden}
#bg{position:fixed;inset:0;width:100%;height:100%;z-index:0;opacity:.4;pointer-events:none}
#auth{position:fixed;inset:0;background:rgba(5,8,22,.94);z-index:99;display:flex;justify-content:center;align-items:center;padding:20px;transition:opacity .4s}
#auth.hide{opacity:0;pointer-events:none}
.ab{width:100%;max-width:360px;padding:28px 22px;border-radius:26px;border:1px solid var(--line);background:var(--card);text-align:center}
.ab h2,.logo{background:linear-gradient(90deg,var(--cyan),var(--purple));-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:800;letter-spacing:3px}
.ab p{color:var(--mut);font-size:13px;margin:8px 0 18px}
.ai{width:100%;padding:14px;border-radius:14px;border:1px solid var(--line);background:rgba(0,0,0,.35);color:var(--cyan);font-size:18px;text-align:center;letter-spacing:6px;outline:none;transition:.2s}
.ai:focus{border-color:var(--cyan);box-shadow:0 0 0 3px rgba(34,211,238,.15)}
.ae{color:var(--red);font-size:12px;height:16px;margin:8px 0}
.wrap{position:relative;z-index:1;max-width:460px;margin:0 auto;padding:max(14px,env(safe-area-inset-top)) 14px max(24px,env(safe-area-inset-bottom))}
header{display:flex;justify-content:space-between;align-items:center;padding:8px 4px 12px}
.logo{font-size:22px}
.badge{font-size:6px;font-weight:700;display:inline-flex;align-items:center;gap:2px;color:var(--gold);padding:1px 3px;border-radius:4px;background:rgba(255,255,255,.05);border:1px solid var(--line);transform:scale(0.65);transform-origin:right center}
.badge i{width:3px;height:3px;border-radius:50%;background:currentColor;animation:p 1.6s infinite}
.badge.live{color:var(--green)}
@keyframes p{50%{opacity:.25}}
.card{padding:20px 16px;border-radius:24px;border:1px solid var(--line);background:var(--card);text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.35)}
.card small{color:var(--mut);font-size:12px}
.pair{color:var(--cyan);font-weight:700;letter-spacing:1px;font-size:14px}
.res{font-size:38px;font-weight:800;margin:8px 0;letter-spacing:2px;transition:color .4s,text-shadow .4s}
.up{color:var(--green);text-shadow:0 0 24px rgba(52,211,153,.6)}
.down{color:var(--red);text-shadow:0 0 24px rgba(251,113,133,.6)}
.flat{color:var(--gold);text-shadow:0 0 24px rgba(251,191,36,.45)}
.bar{height:8px;border-radius:99px;background:rgba(255,255,255,.07);margin:14px 4px 6px;overflow:hidden}
.bar i{display:block;height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,var(--purple),var(--cyan));transition:width .7s cubic-bezier(.2,.8,.2,1)}
.sl{display:flex;justify-content:space-between;margin:0 4px;font-size:12px;color:var(--mut)}.sl b{color:var(--cyan)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:14px}
.stats div{padding:9px 2px;border-radius:12px;background:rgba(255,255,255,.04);font-size:11px;color:var(--mut)}
.stats b{display:block;color:var(--txt);font-size:13px;margin-top:3px;font-variant-numeric:tabular-nums}
.votes{display:flex;gap:6px;justify-content:center;margin-top:12px}
.votes span{font-size:11px;padding:4px 9px;border-radius:99px;border:1px solid var(--line);color:var(--mut);transition:.3s}
.votes span.u{color:var(--green);border-color:rgba(52,211,153,.5)}.votes span.d{color:var(--red);border-color:rgba(251,113,133,.5)}
.go{width:100%;margin-top:14px;padding:15px;border:0;border-radius:16px;font-size:15px;font-weight:800;letter-spacing:1px;color:#050816;cursor:pointer;background:linear-gradient(90deg,var(--purple),var(--cyan));box-shadow:0 8px 26px color-mix(in srgb,var(--cyan) 30%,transparent);transition:transform .15s}
.go:active{transform:scale(.97)}
.auto{display:flex;align-items:center;justify-content:space-between;margin-top:12px;padding:12px 14px;border-radius:14px;border:1px solid var(--line);background:var(--card);font-size:13px;color:var(--mut);cursor:pointer}
.sw{width:38px;height:22px;border-radius:99px;background:rgba(255,255,255,.12);position:relative;transition:.3s}
.sw:after{content:"";position:absolute;top:3px;left:3px;width:16px;height:16px;border-radius:50%;background:#fff;transition:.3s}
.auto.on .sw{background:var(--cyan)}.auto.on .sw:after{left:19px}
.group{margin-top:14px}.group h3{font-size:11px;letter-spacing:1.5px;color:var(--mut);margin:0 0 7px 4px;font-weight:600}
.row{display:grid;gap:8px}.c2{grid-template-columns:1fr 1fr}.c4{grid-template-columns:repeat(4,1fr)}
.btn{padding:12px 6px;border-radius:14px;border:1px solid var(--line);background:var(--card);color:var(--txt);font-weight:600;font-size:13px;cursor:pointer;transition:.2s}
.btn:active{transform:scale(.96)}
.btn.on{border-color:var(--cyan);color:var(--cyan);background:color-mix(in srgb,var(--cyan) 14%,transparent)}
.note{margin-top:16px;font-size:11px;line-height:1.5;color:var(--mut);text-align:center}
.themes{display:flex;gap:8px}.sw2{flex:1;height:40px;border-radius:12px;border:2px solid transparent;cursor:pointer;font-size:10px;font-weight:800;letter-spacing:1px;color:var(--txt);background:var(--card);transition:.25s}.sw2:active{transform:scale(.94)}.sw2.on{border-color:#fff;box-shadow:0 0 14px color-mix(in srgb,var(--cyan) 50%,transparent)}
@keyframes drift{to{transform:translate3d(3%,2%,0) scale(1.08)}}
@keyframes shine{to{left:130%}}
body:before{content:"";position:fixed;inset:-20%;z-index:0;pointer-events:none;will-change:transform;background:radial-gradient(40% 30% at 20% 15%,color-mix(in srgb,var(--cyan) 18%,transparent),transparent),radial-gradient(35% 30% at 85% 70%,color-mix(in srgb,var(--purple) 16%,transparent),transparent);animation:drift 18s ease-in-out infinite alternate}
.go{position:relative;overflow:hidden}.go:after{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.35),transparent);transform:skewX(-20deg);animation:shine 3.5s infinite}
.gwrap{position:relative;width:170px;height:170px;margin:8px auto 4px}
.gauge{width:100%;height:100%;transform:rotate(-90deg)}
.gt{fill:none;stroke:rgba(255,255,255,.07);stroke-width:8}
.gf{fill:none;stroke:var(--cyan);stroke-width:8;stroke-linecap:round;stroke-dasharray:327;stroke-dashoffset:327;transition:stroke-dashoffset .9s cubic-bezier(.2,.8,.2,1),stroke .4s}
.gwrap.up .gf{stroke:var(--green)}.gwrap.down .gf{stroke:var(--red)}
.gc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.gc .res{font-size:21px;margin:0}
.live{font-size:28px;font-weight:700;margin:6px 0 2px;font-variant-numeric:tabular-nums;transition:color .3s}
.trow{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}.trow .auto{margin-top:0}
.hist{margin-top:12px;text-align:left}.hist h3{font-size:11px;letter-spacing:1.5px;color:var(--mut);font-weight:600;margin-bottom:10px}
.hist .stats{grid-template-columns:repeat(3,1fr);margin:0 0 8px;text-align:center}
.hr{display:flex;justify-content:space-between;font-size:12px;padding:8px 2px;border-top:1px solid var(--line);color:var(--mut)}
.hr b.u{color:var(--green)}.hr b.d{color:var(--red)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div id="auth"><div class="ab"><h2>HELIX BOTICS</h2><p>Enter Access Key</p>
<input type="password" id="key" class="ai" placeholder="••••" maxlength="6" inputmode="numeric">
<div class="ae" id="aerr"></div><button class="go" id="unlock" style="margin:0">UNLOCK</button></div></div>

<canvas id="bg"></canvas>
<div class="wrap">
<header><div class="logo">HELIX BOTICS</div><div class="badge live" id="badge"><i></i><span id="bt">LIVE</span></div></header>

<div class="card">
  <div class="pair" id="pair">EUR/USD - 1m</div>
  <div class="live" id="live">-</div>
  <small>EMA 9/21 + RSI 14 + MACD + Bollinger</small>
  <div class="gwrap" id="gw"><svg class="gauge" viewBox="0 0 120 120"><circle class="gt" cx="60" cy="60" r="52"/><circle class="gf" id="gf" cx="60" cy="60" r="52"/></svg><div class="gc"><div class="res flat" id="res">--</div><small id="gp">0%</small></div></div>
  <small id="why">Press Analyze</small>
  <div class="sl"><span>Signal strength</span><b id="sval">-</b></div>
  <div class="votes"><span id="v1">EMA</span><span id="v2">RSI</span><span id="v3">MACD</span><span id="v4">BB</span></div>
  <div class="stats">
    <div>Price<b id="px">-</b></div><div>RSI<b id="rsi">-</b></div>
    <div>MACD<b id="mac">-</b></div><div>Volatility<b id="atr">-</b></div>
  </div>
</div>

<button class="go" id="go">ANALYZE NOW</button>
<div class="trow"><div class="auto" id="auto"><span>Auto 3s</span><div class="sw"></div></div><div class="auto" id="alrt"><span>Alert</span><div class="sw"></div></div></div>
<div class="card hist"><h3>SESSION SCORECARD</h3>
  <div class="stats"><div>Signals<b id="sn">0</b></div><div>Win rate<b id="sw">-</b></div><div>Open P/L<b id="so">-</b></div></div>
  <div id="hl"></div>
  <small style="display:block;margin-top:8px;font-size:11px">Win rate counts closed signals only. Small samples prove nothing.</small></div>

<div class="group"><h3>MARKET TYPE</h3>
  <div class="row c2" id="g-mkt"><button class="btn on" data-v="demo">Binary Chart</button><button class="btn" data-v="real">Real (live crypto)</button></div></div>
<div class="group"><h3>SELECT ASSET</h3><div class="row c2" id="g-asset"></div></div>
<div class="group"><h3>TIMEFRAME</h3>
  <div class="row c4" id="g-tf"><button class="btn" data-v="30s">30s</button><button class="btn on" data-v="1m">1m</button><button class="btn" data-v="5m">5m</button><button class="btn" data-v="15m">15m</button></div></div>

<div class="group"><h3>THEME</h3><div class="themes" id="g-theme"></div></div>
<p class="note"><b>AI-Driven Analysis Engine:</b></p>
</div>

<script>
const KEY="1914",$=id=>document.getElementById(id);
function unlock(){if($('key').value===KEY){$('auth').classList.add('hide')}else{$('aerr').textContent='Incorrect key';$('key').value=''}}
$('unlock').onclick=unlock;$('key').addEventListener('keydown',e=>{if(e.key==='Enter')unlock()});

const ASSETS={demo:{'EUR/USD':1.0850,'GBP/USD':1.2710,'USD/JPY':149.20,'AUD/USD':0.6540},
 real:{'BTC/USDT':'BTCUSDT','ETH/USDT':'ETHUSDT','SOL/USDT':'SOLUSDT','BNB/USDT':'BNBUSDT'}};
const TFS={'30s':30,'1m':60,'5m':300,'15m':900,'1h':3600};
let mkt='demo',asset='EUR/USD',tf='1m',candles=[],cur=null,regime=0,autoOn=false,timer=null,ver=0;
const MAX=60;

/* ---------- background + chart ---------- */
const cv=$('bg'),ctx=cv.getContext('2d');let W,H,dpr=Math.min(devicePixelRatio||1,2);
function size(){W=innerWidth;H=innerHeight;cv.width=W*dpr;cv.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
addEventListener('resize',size);size();
let shownMin=0,shownMax=1;
function draw(){
  ctx.clearRect(0,0,W,H);
  const all=cur?candles.concat(cur):candles;
  if(all.length>2){
    let mn=Infinity,mx=-Infinity;all.forEach(k=>{mn=Math.min(mn,k.l);mx=Math.max(mx,k.h)});
    if(!shownMax||shownMin===0){shownMin=mn;shownMax=mx}
    shownMin+=(mn-shownMin)*.08;shownMax+=(mx-shownMax)*.08;
    const top=H*.1,bot=H*.9,rng=(shownMax-shownMin)||1,step=W/(MAX+1);
    const y=v=>bot-((v-shownMin)/rng)*(bot-top);
    ctx.strokeStyle='rgba(120,150,220,.12)';ctx.lineWidth=1;
    for(let i=1;i<6;i++){ctx.beginPath();ctx.moveTo(0,H*i/6);ctx.lineTo(W,H*i/6);ctx.stroke()}
    all.forEach((k,i)=>{
      const x=step*(i+.8),up=k.c>=k.o,col=up?'#34d399':'#fb7185';
      ctx.strokeStyle=col;ctx.fillStyle=col;ctx.lineWidth=1.5;
      ctx.beginPath();ctx.moveTo(x,y(k.h));ctx.lineTo(x,y(k.l));ctx.stroke();
      const bw=Math.max(3,step*.55),yt=y(Math.max(k.o,k.c)),hh=Math.max(2,Math.abs(y(k.o)-y(k.c)));
      ctx.beginPath();ctx.roundRect(x-bw/2,yt,bw,hh,2);ctx.fill();
    });
    const cl=all.map(k=>k.c);
    [[9,pal.a],[21,pal.b]].forEach(([n,c])=>{
      const e=emaArr(cl,n);ctx.strokeStyle=c;ctx.lineWidth=1.5;ctx.beginPath();
      e.forEach((v,i)=>{const x=step*(i+.8);i?ctx.lineTo(x,y(v)):ctx.moveTo(x,y(v))});ctx.stroke();
    });
  }
  requestAnimationFrame(draw);
}

/* ---------- data: demo (simulated) ---------- */
const base=()=>ASSETS.demo[asset],vol=()=>base()*0.0004;
function seedDemo(){
  candles=[];let p=base();
  for(let i=0;i<MAX;i++){
    regime=regime*.9+(Math.random()-.5)*.6;
    const o=p,c=o+(regime+(Math.random()-.5))*vol();
    candles.push({o,c,h:Math.max(o,c)+Math.random()*vol()*.6,l:Math.min(o,c)-Math.random()*vol()*.6});p=c;
  }
  const l=candles[candles.length-1];cur={o:l.c,c:l.c,h:l.c,l:l.c};
}
let acc=0;
setInterval(()=>{
  if(mkt!=='demo'||!cur)return;
  regime=regime*.97+(Math.random()-.5)*.3;
  cur.c+=(regime+(Math.random()-.5))*vol()*.25;cur.h=Math.max(cur.h,cur.c);cur.l=Math.min(cur.l,cur.c);
  acc+=250;
  if(acc>=Math.max(4000,TFS[tf]*40)){acc=0;candles.push(cur);if(candles.length>MAX)candles.shift();cur={o:cur.c,c:cur.c,h:cur.c,l:cur.c}}
},250);

/* ---------- data: real (Binance public API) ---------- */
async function loadReal(){
  const v=++ver;
  try{
    let k;
    if(tf==='30s'){
      const r=await fetch('https://api.binance.com/api/v3/klines?symbol='+ASSETS.real[asset]+'&interval=1s&limit='+(MAX*30+30));
      const d=await r.json();if(v!==ver||mkt!=='real')return;
      k=[];
      for(let i=0;i+30<=d.length;i+=30){const g=d.slice(i,i+30);
        k.push({o:+g[0][1],h:Math.max(...g.map(x=>+x[2])),l:Math.min(...g.map(x=>+x[3])),c:+g[29][4]})}
      k=k.slice(-(MAX+1));
    }else{
      const r=await fetch('https://api.binance.com/api/v3/klines?symbol='+ASSETS.real[asset]+'&interval='+tf+'&limit='+(MAX+1));
      const d=await r.json();if(v!==ver||mkt!=='real')return;
      k=d.map(x=>({o:+x[1],h:+x[2],l:+x[3],c:+x[4]}));
    }
    cur=k.pop();candles=k;$('why').textContent=$('why').textContent==='Live data unavailable'?'Press Analyze':$('why').textContent;
  }catch(e){$('why').textContent='Live data unavailable'}
}
setInterval(()=>{if(mkt==='real')loadReal()},tf==='30s'?2000:4000);

/* ---------- indicators ---------- */
function emaArr(a,n){const k=2/(n+1);let e=a[0];return a.map((v,i)=>i?(e=v*k+e*(1-k)):e)}
function rsiCalc(a,n=14){
  if(a.length<n+1)return 50;let g=0,l=0;
  for(let i=1;i<=n;i++){const d=a[i]-a[i-1];d>=0?g+=d:l-=d}g/=n;l/=n;
  for(let i=n+1;i<a.length;i++){const d=a[i]-a[i-1];g=(g*(n-1)+Math.max(d,0))/n;l=(l*(n-1)+Math.max(-d,0))/n}
  return l===0?100:100-100/(1+g/l);
}
function macdCalc(a){const e12=emaArr(a,12),e26=emaArr(a,26),m=e12.map((v,i)=>v-e26[i]),s=emaArr(m,9);return m[m.length-1]-s[s.length-1]}
function bbPos(a,n=20){const s=a.slice(-n),m=s.reduce((x,y)=>x+y,0)/s.length,sd=Math.sqrt(s.reduce((x,y)=>x+(y-m)**2,0)/s.length)||1e-9;return (a[a.length-1]-(m-2*sd))/(4*sd)}
function atrPct(){const s=candles.slice(-14);return s.reduce((x,k)=>x+(k.h-k.l),0)/s.length/cur.c*100}

function setVote(id,v){const e=$(id);e.className=v>0?'u':v<0?'d':''}
function analyze(){
  if(!cur||candles.length<30){$('why').textContent='Collecting data...';return}
  const cl=candles.map(k=>k.c).concat(cur.c),n=cl.length;
  const e9=emaArr(cl,9)[n-1],e21=emaArr(cl,21)[n-1],r=rsiCalc(cl),mh=macdCalc(cl),bb=bbPos(cl);
  const gap=(e9-e21)/e21*100;
  const vE=gap>0?1:-1;
  const vR=r>=70||r<=30?0:r>55?1:r<45?-1:0;
  const vM=mh>0?1:-1;
  const vB=bb>0.8||bb<0.2?0:bb>0.55?1:bb<0.45?-1:0;
  const votes=[vE,vR,vM,vB],net=votes.reduce((a,b)=>a+b,0);
  let t='WAIT',cls='flat',why='Indicators do not agree, no clear setup';
  if(net>=3){t='BULLISH';cls='up';why='Trend, momentum and MACD agree upward'}
  else if(net<=-3){t='BEARISH';cls='down';why='Trend, momentum and MACD agree downward'}
  else if(r>=70)why='RSI overbought, reversal risk';
  else if(r<=30)why='RSI oversold, reversal risk';
  const str=Math.round(Math.abs(net)/4*100);
  setGauge(str);$('gw').className='gwrap '+cls;$('sval').textContent=str+'%  ('+votes.filter(v=>v!==0&&v===Math.sign(net)).length+'/4 agree)';
  $('res').textContent=t;$('res').className='res '+cls;$('why').textContent=why;
  ['v1','v2','v3','v4'].forEach((id,i)=>setVote(id,votes[i]));lastCls=cls;smartTheme(cls);track(t,cur.c);
  const dec=cur.c>1000?2:cur.c>100?3:5;
  $('px').textContent=cur.c.toFixed(dec);$('rsi').textContent=r.toFixed(1);
  $('mac').textContent=(mh>0?'+':'')+(mh/cur.c*1e4).toFixed(1);$('atr').textContent=atrPct().toFixed(3)+'%';
}

/* ---------- UI ---------- */
function buildAssets(){
  const g=$('g-asset');g.innerHTML='';
  Object.keys(ASSETS[mkt]).forEach((a,i)=>{const b=document.createElement('button');b.className='btn'+(i?'':' on');b.textContent=a;b.dataset.v=a;g.appendChild(b)});
  asset=Object.keys(ASSETS[mkt])[0];
}
function reload(){
  shownMin=0;$('res').textContent='--';$('res').className='res flat';setGauge(0);$('gw').className='gwrap';openSig=null;renderHist();$('sval').textContent='-';
  ['v1','v2','v3','v4'].forEach(i=>$(i).className='');
  $('pair').textContent=asset+' - '+tf;
  $('badge').className='badge live';
  $('bt').textContent='LIVE';
  $('why').textContent='Press Analyze';
  if(mkt==='demo')seedDemo();else{candles=[];cur=null;loadReal()}
}
function group(id,fn){const g=$(id);g.addEventListener('click',e=>{const b=e.target.closest('.btn');if(!b)return;g.querySelectorAll('.btn').forEach(x=>x.classList.remove('on'));b.classList.add('on');fn(b.dataset.v)})}
group('g-mkt',v=>{mkt=v;buildAssets();reload()});
group('g-asset',v=>{asset=v;reload()});
group('g-tf',v=>{tf=v;reload()});
$('go').onclick=analyze;
$('auto').onclick=()=>{autoOn=!autoOn;$('auto').classList.toggle('on',autoOn);clearInterval(timer);if(autoOn){analyze();timer=setInterval(analyze,3000)}};
/* ---------- scorecard, alerts, live price ---------- */
const sigs=[];let openSig=null,alertOn=false,actx=null,prevPx=0;
const decs=p=>p>1000?2:p>100?3:5;
function setGauge(p){$('gf').style.strokeDashoffset=327*(1-p/100);$('gp').textContent=p+'%'}
function dirPct(s,px){return (px-s.px)/s.px*100*(s.t==='BULLISH'?1:-1)}
function fmt(p){return (p>=0?'+':'')+p.toFixed(3)+'%'}
function track(t,px){
  if(openSig&&openSig.t!==t){const p=dirPct(openSig,px);openSig.pct=p;openSig.res=p>0?'win':'loss';openSig=null}
  if(!openSig&&(t==='BULLISH'||t==='BEARISH')){
    openSig={t,px,asset,tm:new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}),res:null};
    sigs.unshift(openSig);if(sigs.length>30)sigs.pop();alertNow();
  }
  renderHist();
}
function renderHist(){
  const done=sigs.filter(s=>s.res),w=done.filter(s=>s.res==='win').length;
  $('sn').textContent=sigs.length;$('sw').textContent=done.length?Math.round(w/done.length*100)+'%':'-';
  $('so').textContent=openSig&&cur?fmt(dirPct(openSig,cur.c)):'-';
  $('hl').innerHTML=sigs.slice(0,5).map(s=>{
    const p=s.res?s.pct:(cur?dirPct(s,cur.c):0),c=p>=0?'u':'d';
    return '<div class="hr"><span>'+s.tm+' '+(s.t==='BULLISH'?'▲':'▼')+' '+s.asset+'</span><b class="'+c+'">'+fmt(p)+(s.res?'':' live')+'</b></div>';
  }).join('')||'<div class="hr"><span>No signals yet</span></div>';
}
function alertNow(){
  if(!alertOn)return;
  try{
    if(navigator.vibrate)navigator.vibrate(120);
    if(actx){const o=actx.createOscillator(),g=actx.createGain();o.frequency.value=880;g.gain.value=.08;o.connect(g);g.connect(actx.destination);o.start();o.stop(actx.currentTime+.15)}
  }catch(e){}
}
$('alrt').onclick=()=>{
  alertOn=!alertOn;$('alrt').classList.toggle('on',alertOn);
  if(alertOn&&!actx){try{actx=new (window.AudioContext||window.webkitAudioContext)()}catch(e){}}
  if(alertOn)alertNow();
};
setInterval(()=>{
  if(!cur)return;const p=cur.c,e=$('live');
  e.textContent=p.toFixed(decs(p));e.className='live '+(p>prevPx?'up':p<prevPx?'down':'');prevPx=p;renderHist();
},500);

/* ---------- themes ---------- */
const THEMES={aurora:['#22d3ee','#8b5cf6','#050816','#0f1a3d'],sunset:['#fb923c','#ec4899','#14080f','#3b1226'],emerald:['#34d399','#14b8a6','#03110d','#0b2e24'],gold:['#fbbf24','#f97316','#110d03','#2e2308'],mono:['#e2e8f0','#94a3b8','#0a0a0a','#1c1c1c']};
let pal={a:'#22d3ee',b:'#8b5cf6'},smartOn=false,themeName='aurora',lastCls='flat';
function applyTheme(n){
  const t=THEMES[n];if(!t)return;const s=document.documentElement.style;
  s.setProperty('--cyan',t[0]);s.setProperty('--purple',t[1]);s.setProperty('--bg',t[2]);s.setProperty('--bg2',t[3]);
  pal={a:t[0],b:t[1]};
}
function markTheme(){document.querySelectorAll('#g-theme .sw2').forEach(x=>x.classList.toggle('on',x.dataset.v==='smart'?smartOn:(!smartOn&&x.dataset.v===themeName)))}
function smartTheme(cls){
  if(!smartOn)return;
  const h=new Date().getHours(),night=h>=19||h<6;
  applyTheme(cls==='up'?'emerald':cls==='down'?'sunset':night?'aurora':'gold');
}
(function(){
  const g=$('g-theme'),sm=document.createElement('button');
  sm.className='sw2';sm.dataset.v='smart';sm.textContent='AUTO';g.appendChild(sm);
  Object.keys(THEMES).forEach(n=>{const b=document.createElement('button'),t=THEMES[n];b.className='sw2';b.dataset.v=n;b.title=n;b.style.background='linear-gradient(135deg,'+t[0]+','+t[1]+')';g.appendChild(b)});
  g.addEventListener('click',e=>{
    const b=e.target.closest('.sw2');if(!b)return;const v=b.dataset.v;
    if(v==='smart'){smartOn=!smartOn;if(smartOn)smartTheme(lastCls);else applyTheme(themeName)}
    else{smartOn=false;themeName=v;applyTheme(v);try{localStorage.setItem('hx-theme',v)}catch(x){}}
    markTheme();
  });
  try{const sv=localStorage.getItem('hx-theme');if(THEMES[sv])themeName=sv}catch(x){}
  applyTheme(themeName);markTheme();
})();

buildAssets();reload();requestAnimationFrame(draw);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return Response(HTML, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True)
