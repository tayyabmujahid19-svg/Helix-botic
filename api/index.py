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
body{background:radial-gradient(circle at 100% 6%,#0a4f63 0,transparent 38%),radial-gradient(circle at 10% -8%,#2b1670 0,transparent 42%),var(--bg);color:var(--t);font:15px/1.4 "SF Pro Display","Segoe UI",system-ui,sans-serif;min-height:100vh;padding:env(safe-area-inset-top) 0 96px}
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
</style>
</head>
<body>
<div class="w">
  <div class="row"><div class="logo"><div class="hex">H</div><div><h1>HELIX BOTIC</h1><div class="sub">Indicator-based market analysis</div></div></div><span id="mode" class="badge">…</span></div>
  <div id="t-dash" class="tab on">
    <div class="card">
      <label>Timeframe</label>
      <div class="seg" id="tf"><button data-v="5">5s</button><button data-v="10">10s</button><button data-v="30">30s</button><button class="on" data-v="60">1m</button><button data-v="180">3m</button><button data-v="300">5m</button><button data-v="900">15m</button></div>
    </div>
    <div class="card"><div class="row"><b>Signal engine</b><span class="sub" id="selp"></span></div>
      <div class="eng" id="eng">
        <svg viewBox="0 0 240 240"><circle cx="120" cy="120" r="104" fill="none" stroke="#ffffff12" stroke-width="8"/><circle id="pg" cx="120" cy="120" r="104" fill="none" stroke="url(#gr)" stroke-width="8" stroke-linecap="round" stroke-dasharray="653.45" stroke-dashoffset="653.45" transform="rotate(-90 120 120)"/><circle class="spin" cx="120" cy="120" r="116" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="6 14"/></svg>
        <div class="ctr"><div id="ic" class="ic">⚡</div><div id="sig" class="d">STANDBY</div><div id="sub" class="sub">Tap to start</div></div>
      </div>
      <div class="mini"><div><span class="sub">Time left</span><b id="left">—:—</b></div><div><span class="sub">Strength</span><b id="str">—</b></div><div><span class="sub">Price</span><b id="px">—</b></div></div>
      <button id="go" class="big">▶ START BOT</button>
    </div>
    <div class="card"><div class="row"><div><b id="cn">—</b><span class="live"><i></i>LIVE</span><div class="sub" id="ci"></div></div><div style="text-align:right"><div id="cpx" class="cpx">—</div><div id="cch" class="sub"></div></div></div></div>
    <div class="card"><b class="sub">Markets</b><div class="seg" id="gp"><button data-v="fx">Forex</button><button class="on" data-v="cr">Crypto</button></div><div class="grid" id="mkt"></div></div>
  </div>
</div>
<script>
const $=s=>document.querySelector(s);
const FX=['EUR/USD','GBP/USD','USD/JPY','USD/CAD','USD/CHF','EUR/GBP','EUR/JPY'];
const CR=['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','XRPUSDT'];
const isFx=p=>p.includes('/'),nm=p=>p;
const fmt=a=>a.toFixed(2);
let S={tf:60,run:false,grp:'cr',pair:'BTCUSDT',px:{},ch:{}};
function seg(id,key){
 document.querySelectorAll(id+' button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll(id+' button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');S[key]=b.dataset.v;
  if(key==='grp'){const L=S.grp==='fx'?FX:CR;if(!L.includes(S.pair))S.pair=L[0];$('#selp').textContent=S.pair;markets()}
 });
}
seg('#gp','grp');
async function bget(path){const r=await fetch('https://api.binance.com'+path);return await r.json()}
async function qqet(path){try{const r=await fetch('https://api.quotex.com/'+path);return await r.json()}catch(e){return {price:1.0850,change:0.12}}}
async function prices(){
 if(S.grp==='cr'){
  try{const j=await bget('/api/v1/ticker/24hr');
  j.forEach(x=>{if(CR.includes(x.symbol)){S.px[x.symbol]=+x.lastPrice;S.ch[x.symbol]=+x.priceChangePercent}})}catch(e){}
 }else{
  for(const p of FX){const r=await qqet(`api/v1/ticker?pair=${p}`);S.px[p]=r.price||1.08;S.ch[p]=r.change||0;}
 }
 markets();
}
function markets(){
 const L=S.grp==='fx'?FX:CR;
 $('#mkt').innerHTML=L.map(p=>`<div class="pc2${p===S.pair?' sel':''}" onclick="S.pair='${p}';markets()"><div class="row"><b>${p}</b></div><div class="sub">${S.px[p]?fmt(S.px[p]):'—'}</div></div>`).join('');
}
$('#selp').textContent=S.pair;
markets();prices();setInterval(prices,15000);
</script>
</body>
</html>
"""

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path in ("/", "/index.html", "/index.py"):
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(HTML)))])
        return [HTML.encode("utf-8")]
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not found"]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"HELIX BOTIC running on http://localhost:{port}")
    make_server("0.0.0.0", port, app).serve_forever()
