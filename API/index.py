from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>HELIX BOTICS</title>
<style>
:root{--bg:#020617;--card:rgba(10, 22, 42, 0.88);--line:#1e3a5f;--cyan:#00f3ff;--purple:#b026ff;--green:#00ff88;--red:#ff0055;--txt:#f1f5f9;--mut:#94a3b8}
*{box-sizing:border-box;margin:0;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
body{background:var(--bg);color:var(--txt);font-family:"Trebuchet MS","Segoe UI",sans-serif;overflow-x:hidden}
#bg{position:fixed;inset:0;width:100%;height:100%;z-index:0}

/* Access Key Overlay Modal */
#auth-modal{position:fixed;inset:0;background:rgba(2,6,23,0.96);z-index:999;display:flex;justify-content:center;align-items:center;padding:20px;backdrop-filter:blur(18px)}
.auth-box{width:100%;max-width:380px;padding:30px 24px;border-radius:28px;border:1px solid var(--cyan);background:var(--card);text-align:center;box-shadow:0 0 50px rgba(0,243,255,0.3)}
.auth-box h2{font-size:24px;letter-spacing:2px;margin-bottom:8px;background:linear-gradient(90deg,#00f3ff,#b026ff,#ff0055);-webkit-background-clip:text;background-clip:text;color:transparent}
.auth-box p{color:var(--mut);font-size:13px;margin-bottom:20px}
.auth-input{width:100%;padding:14px;border-radius:14px;border:1px solid var(--line);background:rgba(0,0,0,0.6);color:var(--cyan);font-size:18px;text-align:center;letter-spacing:6px;outline:none;margin-bottom:16px;box-shadow:inset 0 0 12px rgba(0,243,255,0.25)}
.auth-input:focus{border-color:var(--cyan);box-shadow:0 0 20px rgba(0,243,255,0.5)}
.auth-btn{width:100%;padding:14px;border:0;border-radius:14px;font-size:16px;font-weight:800;letter-spacing:1px;color:#020617;background:linear-gradient(90deg,#b026ff,#00f3ff);cursor:pointer;box-shadow:0 0 25px rgba(0,243,255,0.5);transition:.18s}
.auth-btn:active{transform:scale(0.97)}
.auth-err{color:var(--red);font-size:12px;margin-top:10px;display:none}

.wrap{position:relative;z-index:1;max-width:460px;margin:0 auto;padding:max(14px,env(safe-area-inset-top)) 14px max(24px,env(safe-area-inset-bottom))}
header{display:flex;justify-content:space-between;align-items:center;padding:10px 4px 14px}
.logo{font-weight:900;letter-spacing:3px;font-size:24px;background:linear-gradient(90deg,#00f3ff,#b026ff,#ff0055);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 15px rgba(0,243,255,0.6))}
.badge{font-size:12px;color:var(--green);display:flex;align-items:center;gap:6px;font-weight:700;text-shadow:0 0 10px rgba(0,255,136,0.6)}
.badge i{width:9px;height:9px;border-radius:50%;background:var(--green);box-shadow:0 0 12px var(--green);animation:p 1.4s infinite}
@keyframes p{50%{opacity:.3}}

/* Professional Card & Monitor Layout (Shifted UP) */
.card{margin-top:6px;padding:22px 16px;border-radius:26px;border:1px solid var(--line);background:var(--card);backdrop-filter:blur(12px);text-align:center;box-shadow:0 0 40px rgba(0,243,255,0.15)}
.card small{color:var(--mut);font-size:12px}
.pair{color:var(--cyan);font-weight:800;letter-spacing:1px;font-size:15px;text-shadow:0 0 10px rgba(0,243,255,0.5)}
.res{font-size:40px;font-weight:900;margin:10px 0;letter-spacing:2px;transition:.3s}
.up{color:var(--green);text-shadow:0 0 25px var(--green)}
.down{color:var(--red);text-shadow:0 0 25px var(--red)}
.flat{color:#ffd700;text-shadow:0 0 25px #ffd700}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px}
.stats div{padding:10px 4px;border-radius:14px;background:rgba(255,255,255,0.05);font-size:12px;color:var(--mut)}
.stats b{display:block;color:var(--txt);font-size:15px;margin-top:3px}

.go{width:100%;margin-top:16px;padding:16px;border:0;border-radius:18px;font-size:16px;font-weight:800;letter-spacing:1px;color:#020617;cursor:pointer;background:linear-gradient(90deg,#b026ff,#00f3ff);box-shadow:0 0 30px rgba(0,243,255,0.55);transition:.18s}
.go:active{transform:scale(.97)}

/* Market Controls (Shifted DOWN) */
.group{margin-top:16px}
.group h3{font-size:12px;letter-spacing:1.5px;color:var(--mut);margin:0 0 8px 4px;font-weight:600}
.row{display:grid;gap:8px}
.c2{grid-template-columns:1fr 1fr}.c4{grid-template-columns:repeat(4,1fr)}
.btn{padding:13px 6px;border-radius:16px;border:1px solid var(--line);background:var(--card);color:var(--txt);font-weight:700;font-size:14px;cursor:pointer;backdrop-filter:blur(8px);transition:.18s}
.btn:active{transform:scale(.96)}
.btn.on{border-color:var(--cyan);color:var(--cyan);background:rgba(0,243,255,0.18);box-shadow:0 0 22px rgba(0,243,255,0.4)}

.note{margin-top:18px;font-size:12px;letter-spacing:1px;color:var(--cyan);text-align:center;font-weight:700;text-shadow:0 0 10px rgba(0,243,255,0.4)}
.bar{height:12px;border-radius:99px;background:rgba(255,255,255,0.08);margin:14px 6px 4px;overflow:hidden}.bar i{display:block;height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,#b026ff,#00f3ff);box-shadow:0 0 18px rgba(0,243,255,0.8);transition:width .6s}
.strlbl{display:flex;justify-content:space-between;margin:0 6px;font-size:12px;color:var(--mut)}
.strlbl b{color:var(--cyan)}
@media (prefers-reduced-motion:reduce){.badge i{animation:none}}
</style>
</head>
<body>

<!-- Access Key Modal -->
<div id="auth-modal">
  <div class="auth-box">
    <h2>HELIX BOTICS</h2>
    <p>Enter Access Key to Continue</p>
    <input type="password" id="access-key-input" class="auth-input" placeholder="••••" maxlength="6">
    <button class="auth-btn" id="verify-btn">UNLOCK</button>
    <div id="auth-err" class="auth-err">Incorrect Access Key! Try again.</div>
  </div>
</div>

<canvas id="bg"></canvas>
<div class="wrap">
  <header>
    <div class="logo">HELIX BOTICS</div>
    <div class="badge"><i></i>HELIX C</div>
  </header>

  <!-- RESULT MONITOR CARD (MOVED UP) -->
  <div class="card">
    <div class="pair" id="pair">EUR/USD - 1m</div>
    <small>Trend reading (EMA 9/21 + RSI 14 + momentum)</small>
    <div class="res flat" id="res">--</div>
    <small id="why">Press Analyze</small>
    <div class="bar"><i id="sbar"></i></div>
    <div class="strlbl"><span>Signal strength</span><b id="sval">-</b></div>
    <div class="stats">
      <div>Price<b id="px">-</b></div>
      <div>RSI<b id="rsi">-</b></div>
      <div>EMA gap<b id="gap">-</b></div>
    </div>
  </div>

  <button class="go" id="go">ANALYZE NOW</button>

  <!-- MARKET CONTROLS (MOVED DOWN) -->
  <div class="group"><h3>MARKET TYPE</h3>
    <div class="row c2" data-g="mkt">
      <button class="btn on">OTC Market</button><button class="btn">Real Market</button>
    </div>
  </div>
  <div class="group"><h3>SELECT ASSET</h3>
    <div class="row c2" data-g="asset">
      <button class="btn on">EUR/USD</button><button class="btn">GBP/USD</button>
      <button class="btn">USD/JPY</button><button class="btn">AUD/USD</button>
    </div>
  </div>
  <div class="group"><h3>TIMEFRAME</h3>
    <div class="row c4" data-g="tf">
      <button class="btn" data-s="10">10s</button><button class="btn" data-s="30">30s</button>
      <button class="btn on" data-s="60">1m</button><button class="btn" data-s="120">2m</button>
    </div>
  </div>

  <!-- AI TYPE PROFESSIONAL DISCLAIMER IN ENGLISH -->
  <p class="note">⚡ Neural AI Core Engine Active — Autonomous Market Analytics & Intelligence</p>
</div>

<script>
// Access Key Logic
const correctKey = "1914";
document.getElementById('verify-btn').addEventListener('click', checkKey);
document.getElementById('access-key-input').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') checkKey();
});

function checkKey() {
  const val = document.getElementById('access-key-input').value;
  const err = document.getElementById('auth-err');
  if (val === correctKey) {
    document.getElementById('auth-modal').style.display = 'none';
  } else {
    err.style.display = 'block';
    document.getElementById('access-key-input').value = '';
  }
}

const cv=document.getElementById('bg'),ctx=cv.getContext('2d');
let W,H,dpr=Math.min(devicePixelRatio||1,2);
function size(){W=innerWidth;H=innerHeight;cv.width=W*dpr;cv.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
addEventListener('resize',size);size();

const bases={'EUR/USD':1.0850,'GBP/USD':1.2710,'USD/JPY':149.20,'AUD/USD':0.6540};
let asset='EUR/USD',tf=60,candles=[],cur=null;
const MAX=46;

function vol(){return bases[asset]*0.00035}
function seed(){
  candles=[];let p=bases[asset];
  for(let i=0;i<MAX;i++){
    const o=p,c=o+(Math.random()-.5)*vol()*3;
    candles.push({o,c,h:Math.max(o,c)+Math.random()*vol(),l:Math.min(o,c)-Math.random()*vol()});p=c;
  }
  const last=candles[candles.length-1];
  cur={o:last.c,c:last.c,h:last.c,l:last.c};
}
function tick(){
  const drift=(Math.random()-.5)*vol();
  cur.c+=drift;cur.h=Math.max(cur.h,cur.c);cur.l=Math.min(cur.l,cur.c);
}
function nextCandle(){
  candles.push(cur);if(candles.length>MAX)candles.shift();
  cur={o:cur.c,c:cur.c,h:cur.c,l:cur.c};
}

let acc=0,last=performance.now();
function draw(now){
  const dt=(now-last)/1000;last=now;
  const speed=Math.max(3,tf/6);
  for(let i=0;i<3;i++)tick();
  acc+=dt;if(acc>=speed){acc=0;nextCandle()}
  ctx.clearRect(0,0,W,H);
  const all=candles.concat(cur);
  let mn=Infinity,mx=-Infinity;
  all.forEach(k=>{mn=Math.min(mn,k.l);mx=Math.max(mx,k.h)});
  const top=H*.12,bot=H*.88,rng=(mx-mn)||1,step=W/(MAX+1);
  const y=v=>bot-((v-mn)/rng)*(bot-top);
  ctx.globalAlpha=.55;
  ctx.strokeStyle='rgba(30,58,95,.5)';ctx.lineWidth=1;
  for(let i=1;i<6;i++){ctx.beginPath();ctx.moveTo(0,H*i/6);ctx.lineTo(W,H*i/6);ctx.stroke()}
  all.forEach((k,i)=>{
    const x=step*(i+.8),up=k.c>=k.o,col=up?'#00ff88':'#ff0055';
    ctx.strokeStyle=col;ctx.fillStyle=col;ctx.shadowColor=col;ctx.shadowBlur=14;
    ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x,y(k.h));ctx.lineTo(x,y(k.l));ctx.stroke();
    const bw=Math.max(4,step*.5),yt=y(Math.max(k.o,k.c)),hh=Math.max(2,Math.abs(y(k.o)-y(k.c)));
    ctx.beginPath();ctx.roundRect(x-bw/2,yt,bw,hh,3);ctx.fill();
  });
  ctx.shadowBlur=0;
  const py=y(cur.c);ctx.setLineDash([6,6]);ctx.strokeStyle='#00f3ff';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(0,py);ctx.lineTo(W,py);ctx.stroke();ctx.setLineDash([]);
  ctx.globalAlpha=1;
  requestAnimationFrame(draw);
}
seed();requestAnimationFrame(draw);

function ema(arr,n){const k=2/(n+1);let e=arr[0];for(let i=1;i<arr.length;i++)e=arr[i]*k+e*(1-k);return e}
function rsi(arr,n=14){
  let g=0,l=0;const s=arr.slice(-n-1);
  for(let i=1;i<s.length;i++){const d=s[i]-s[i-1];d>=0?g+=d:l-=d}
  if(l===0)return 100;return 100-100/(1+g/l);
}
function analyze(){
  const closes=candles.map(k=>k.c).concat(cur.c);
  const e9=ema(closes,9),e21=ema(closes,21),r=rsi(closes),gap=(e9-e21)/e21*10000;
  let t='NEUTRAL',cls='flat',why='EMAs and RSI do not agree';
  if(e9>e21&&r<70&&r>50){t='BULLISH';cls='up';why='EMA 9 above EMA 21, RSI above 50'}
  else if(e9<e21&&r>30&&r<50){t='BEARISH';cls='down';why='EMA 9 below EMA 21, RSI below 50'}
  else if(r>=70){why='RSI overbought, trend may be stretched'}
  else if(r<=30){why='RSI oversold, trend may be stretched'}
  const cl=(v)=>Math.max(0,Math.min(1,v));
  const mom=(closes[closes.length-1]-closes[closes.length-6])/closes[closes.length-6]*10000;
  const votes=[Math.sign(gap),Math.sign(r-50),Math.sign(mom)];
  const net=votes.reduce((a,b)=>a+b,0),agree=Math.max(votes.filter(v=>v>0).length,votes.filter(v=>v<0).length);
  const raw=0.4*cl(Math.abs(gap)/3)+0.3*cl(Math.abs(r-50)/25)+0.3*cl(Math.abs(mom)/3);
  const str=Math.round(100*raw*(agree===3?1:agree===2?0.7:0.4));
  document.getElementById('sbar').style.width=str+'%';
  document.getElementById('sval').textContent=str+'%  ('+agree+'/3 indicators agree)';
  const res=document.getElementById('res');
  res.textContent=t;res.className='res '+cls;
  document.getElementById('why').textContent=why;
  const dec=asset==='USD/JPY'?3:5;
  document.getElementById('px').textContent=cur.c.toFixed(dec);
  document.getElementById('rsi').textContent=r.toFixed(1);
  document.getElementById('gap').textContent=gap.toFixed(1)+' pips';
}
function label(){document.getElementById('pair').textContent=asset+' - '+(tf>=60?tf/60+'m':tf+'s')}

document.querySelectorAll('[data-g]').forEach(g=>{
  g.querySelectorAll('.btn').forEach(b=>b.addEventListener('click',()=>{
    g.querySelectorAll('.btn').forEach(x=>x.classList.remove('on'));b.classList.add('on');
    const k=g.dataset.g;
    if(k==='asset'){asset=b.textContent;seed()}
    if(k==='tf'){tf=+b.dataset.s}
    label();
  }));
});
document.getElementById('go').addEventListener('click',analyze);
label();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return Response(HTML, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True)
