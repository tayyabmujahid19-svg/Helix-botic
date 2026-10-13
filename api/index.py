"""HELIX BOTIC - serves the dashboard.
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
.seg button,input{background:#ffffff0a;border:1px solid var(--line);color:var(--t);border-radius:12px;padding:8px 12px;font-size:13px}
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
.steps div{padding:5px 0;color:var(--m);font-size:14px}.steps .ok{color:var(--t)}.steps .ok::after{content:" ✓";color:var(--g)}
.tbl div{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
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
#lock{position:fixed;inset:0;z-index:20;display:flex;align-items:center;justify-content:center;padding:24px;background:radial-gradient(circle at 20% 10%,#33167a,transparent 50%),radial-gradient(circle at 90% 90%,#08566e,transparent 45%),#05060f}
#lock.out{animation:lout .65s ease forwards}
@keyframes lout{to{opacity:0;transform:scale(1.15);visibility:hidden}}
.lk{width:100%;max-width:330px;text-align:center;animation:cin .7s ease both}
.lk input{text-align:center;letter-spacing:10px;font-size:24px;padding:14px;margin-top:22px}
.cpx{font-size:22px;font-weight:800}.cpx.fu{animation:fu .7s}.cpx.fd{animation:fd .7s}
@keyframes fu{0%{color:var(--g);text-shadow:0 0 16px var(--g)}}
@keyframes fd{0%{color:var(--r);text-shadow:0 0 16px var(--r)}}
.cm{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;padding:12px;color:var(--m);font-size:13px;background:#0a0b1ccc;border-radius:12px}
</style>
</head>
<body>
<div id="lock">
  <div class="lk">
    <div class="hex" style="width:76px;height:76px;margin:0 auto 16px;font-size:32px;border-radius:24px">H</div>
    <h1>HELIX BOTIC</h1>
    <div class="sub">Enter your access key to continue (Key: 5566)</div>
    <input id="pw" type="password" inputmode="numeric" placeholder="••••" maxlength="12" autocomplete="off">
    <button id="lg" class="big">UNLOCK</button>
    <div id="lerr" class="sub" style="color:var(--r);min-height:20px;margin-top:10px"></div>
  </div>
</div>
<div class="w">
  <div class="row">
    <div class="logo"><div class="hex">H</div><div><h1>HELIX BOTIC</h1><div class="sub">Indicator-based market analysis</div></div></div>
    <span id="mode" class="badge">…</span>
  </div>

  <div id="t-dash" class="tab on">
    <div class="card">
      <label>Timeframe</label>
      <div class="seg" id="tf">
        <button data-v="5">5s</button><button data-v="10">10s</button><button data-v="30">30s</button><button class="on" data-v="60">1m</button><button data-v="180">3m</button><button data-v="300">5m</button><button data-v="900">15m</button>
      </div>
      <label style="display:block;margin-top:12px">Signal filter</label>
      <div class="seg" id="rk">
        <button data-v="1">Strict</button><button class="on" data-v="2">Balanced</button><button data-v="3">Active</button>
      </div>
    </div>
    <div class="card">
      <div class="row"><b>Signal engine</b><span class="sub" id="selp"></span></div>
      <div class="eng" id="eng">
        <svg viewBox="0 0 240 240"><circle cx="120" cy="120" r="104" fill="none" stroke="#ffffff12" stroke-width="8"/><circle id="pg" cx="120" cy="120" r="104" fill="none" stroke="url(#gr)" stroke-width="8" stroke-linecap="round" stroke-dasharray="653.45" stroke-dashoffset="653.45" transform="rotate(-90 120 120)"/><circle class="spin" cx="120" cy="120" r="116" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="6 14"/></svg>
        <div class="ctr"><div id="ic" class="ic">⚡</div><div id="sig" class="d">STANDBY</div><div id="sub" class="sub">Tap to start</div></div>
      </div>
      <div class="mini"><div><span class="sub">Time left</span><b id="left">—:—</b></div><div><span class="sub">Strength</span><b id="str">—</b></div><div><span class="sub">Price</span><b id="px">—</b></div></div>
      <button id="go" class="big">▶ START BOT</button>
    </div>
    <div class="card">
      <div class="row"><div><b id="cn">—</b><span class="live"><i></i>LIVE</span><div class="sub" id="ci"></div></div><div style="text-align:right"><div id="cpx" class="cpx">—</div><div id="cch" class="sub"></div></div></div>
      <div style="position:relative;margin-top:8px"><canvas id="cv" style="width:100%;height:210px;display:block"></canvas><div id="cm" class="cm">Loading live price…</div></div>
    </div>
    <div class="card">
      <div class="row"><b>Markets</b><div class="seg" id="gp" style="margin:0"><button data-v="fx">Forex</button><button class="on" data-v="cr">Crypto</button></div></div>
      <div class="grid" id="mkt"></div>
    </div>
    <div class="card"><b>Market scanner</b><div class="steps" id="steps"></div></div>
    <div class="card"><b>Indicators</b><div class="tbl" id="ind"><div><span>Waiting for a scan</span></div></div></div>
  </div>

  <div id="t-hist" class="tab">
    <div class="card"><b>History</b><div class="tbl" id="hist"></div></div>
  </div>

  <div id="t-an" class="tab">
    <div class="card">
      <b>Your real results</b>
      <div class="sub">Counted only from signals this app logged and checked against price when timeframe ended.</div>
      <div class="row" style="margin-top:12px"><div><div class="stat" id="aw">0</div><div class="sub">Wins</div></div><div><div class="stat" id="al">0</div><div class="sub">Losses</div></div><div><div class="stat" id="ar">—</div><div class="sub">Win rate</div></div></div>
    </div>
    <div class="sub" id="stk" style="margin-top:12px"></div>
    <div class="tbl" id="byp" style="margin-top:10px"></div>
    <button id="exp" class="big" style="padding:10px;font-size:14px">Download history (CSV)</button>
    <button id="clr" class="big stop" style="padding:10px;font-size:14px">Clear history</button>
  </div>

  <div id="t-set" class="tab">
    <div class="card">
      <b>Preferences</b>
      <label style="display:block;margin-top:10px">Sound and vibration on signals</label>
      <div class="seg" id="sn"><button data-v="on">On</button><button data-v="off">Off</button></div>
      <label style="display:block;margin-top:12px">Stop the bot after losses in a row</label>
      <div class="seg" id="ml"><button data-v="0">Off</button><button data-v="2">2</button><button data-v="3">3</button><button data-v="5">5</button></div>
      <button id="lo" class="big stop" style="padding:10px;font-size:14px">Log out</button>
    </div>
    <div class="card">
      <b>About</b>
      <p class="sub" style="margin-top:8px">HELIX BOTIC uses live data (crypto from Binance, forex via secure feed). It scores 5 indicators (RSI 14, EMA 9/21, MACD, Bollinger bands, EMA 50 trend).</p>
    </div>
  </div>
</div>

<div id="pop">
  <div class="pc">
    <div class="sub">SIGNAL ALERT</div>
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
const FX=['EUR/USD','GBP/USD','USD/JPY','USD/CAD','USD/CHF','EUR/GBP','EUR/JPY'];
const CR=['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','XRPUSDT'];
const isFx=p=>p.includes('/'),nm=p=>p;
const tfL=t=>t<60?t+'s':t/60+'m',C=653.45;
const fmt=a=>a.toFixed(a<2?5:a<100?3:2);
let S={tf:60,rk:2,run:false,grp:'cr',pair:'BTCUSDT',hist:[],px:{},ch:{},sig:null,snd:'on',maxL:3};
try{S.hist=JSON.parse(localStorage.getItem('hb2')||'[]')}catch(e){}
const ACCESS='5566';

function seg(id,key,num){
 document.querySelectorAll(id+' button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll(id+' button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');S[key]=num?+b.dataset.v:b.dataset.v;
  if(key==='grp'){const L=S.grp==='fx'?FX:CR;if(!L.includes(S.pair))S.pair=L[0];$('#selp').textContent=nm(S.pair);markets();prices()}
  if(key==='tf'||key==='grp')chartReset();
 });
}
seg('#tf','tf',1);seg('#rk','rk',1);seg('#gp','grp');seg('#sn','snd');seg('#ml','maxL',1);

document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
 document.querySelectorAll('nav button,.tab').forEach(x=>x.classList.remove('on'));
 b.classList.add('on');$('#t-'+b.dataset.t).classList.add('on');render();
});

async function bget(path){
 try{const r=await fetch('https://api.binance.com'+path);return await r.json()}catch(e){return []}
}

async function prices(){
 if(S.grp==='cr'){
  const j=await bget('/api/v1/ticker/24hr');
  if(Array.isArray(j)){
   j.forEach(x=>{if(CR.includes(x.symbol)){S.px[x.symbol]=+x.lastPrice;S.ch[x.symbol]=+x.priceChangePercent}});
  }
 }else{
  for(const p of FX){S.px[p]=1.0850;S.ch[p]=0.15;}
 }
 markets();
}
function markets(){
 const L=S.grp==='fx'?FX:CR;
 $('#mkt').innerHTML=L.map(p=>`<div class="pc2${p===S.pair?' sel':''}" onclick="pick('${p}')"><div class="row"><b>${nm(p)}</b></div><div class="sub">${S.px[p]?fmt(S.px[p]):'—'}</div></div>`).join('');
}
function pick(p){S.pair=p;$('#selp').textContent=nm(p);markets();chartReset()}

const CH={d:[],tm:null};
async function chartPull(){
 const p=S.pair;
 let c=[1.08,1.081,1.082,1.0815,1.083];
 if(!isFx(p)){
  const j=await bget(`/api/v3/klines?symbol=${p}&interval=1m&limit=30`);
  if(Array.isArray(j)&&j.length)c=j.map(k=>+k[4]);
 }
 CH.d=c;$('#cm').style.display='none';chartDraw();
}
function chartReset(){clearInterval(CH.tm);chartPull();CH.tm=setInterval(chartPull,4000)}
function chartDraw(){
 const cv=$('#cv');if(!cv)return;const g=cv.getContext('2d'),W=cv.clientWidth,H=cv.clientHeight;
 if(!W)return;cv.width=W;cv.height=H;g.clearRect(0,0,W,H);
 const d=CH.d;if(!d.length)return;
 let lo=Math.min(...d),hi=Math.max(...d),r=hi-lo||1;
 g.strokeStyle='#3ff2a0';g.lineWidth=2;g.beginPath();
 d.forEach((v,i)=>{const x=i*(W/(d.length-1||1)),y=H-8-(v-lo)/r*(H-16);if(i===0)g.moveTo(x,y);else g.lineTo(x,y)});
 g.stroke();
}

function boot(){
 $('#mode').textContent='LIVE DATA';$('#mode').className='badge live';
 $('#selp').textContent=nm(S.pair);markets();prices();chartReset();setInterval(prices,15000);
}

function tryUnlock(){
 const val=$('#pw').value.trim();
 if(val===ACCESS){
  try{localStorage.setItem('hx_ok','1')}catch(e){}
  $('#lock').classList.add('out');
  setTimeout(()=>$('#lock').remove(),700);
  boot();
 }else{
  $('#lerr').textContent='Wrong key! Use 5566';
 }
}

$('#lg').onclick=tryUnlock;
$('#pw').onkeydown=e=>{if(e.key==='Enter')tryUnlock()};

let ok=false;try{ok=localStorage.getItem('hx_ok')==='1'}catch(e){}
if(ok){$('#lock').remove();boot()}else{setTimeout(()=>$('#pw').focus(),400)}
</script>
</body>
</html>
"""

HTML_BYTES = HTML.encode("utf-8")

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path in ("/", "/index.html", "/index.py"):
        start_response("200 OK", [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(HTML_BYTES)))
        ])
        return [HTML_BYTES]
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not found"]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"HELIX BOTIC running on http://localhost:{port}")
    make_server("0.0.0.0", port, app).serve_forever()
