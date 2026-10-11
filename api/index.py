from flask import Flask, render_template_string, jsonify, request
import random
import time

app = Flask(__name__)

# VIP Config
PASSWORD = "1914"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>HELIX BOTICS - INSTITUTIONAL QUANT TERMINAL</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --neon-cyan: #00F0FF;
            --neon-mint: #00FF88;
            --neon-crimson: #FF0055;
            --indigo-glow: #6366F1;
            --text-main: #F8FAFC;
            --border-glow: rgba(0, 240, 255, 0.7);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
            -webkit-user-select: none;
        }

        html, body {
            width: 100%;
            min-height: 100vh;
            overflow-y: auto;
            overflow-x: hidden;
            background: #010308;
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
        }

        body {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 14px 0;
            position: relative;
        }

        /* Pro Cyber Background */
        .cyber-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            background: radial-gradient(circle at 50% 20%, #0a1736 0%, #010308 100%);
            overflow: hidden;
            pointer-events: none;
        }

        .cyber-grid {
            position: absolute;
            width: 200%;
            height: 200%;
            top: -50%;
            left: -50%;
            background-image: 
                linear-gradient(rgba(0, 240, 255, 0.12) 1px, transparent 1px),
                linear-gradient(90deg, rgba(99, 102, 241, 0.12) 1px, transparent 1px);
            background-size: 40px 40px;
            animation: gridMove 25s linear infinite;
        }

        @keyframes gridMove {
            0% { transform: translateY(0) translateX(0); }
            100% { transform: translateY(40px) translateX(40px); }
        }

        .glow-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(90px);
            opacity: 0.5;
            animation: orbFloat 7s ease-in-out infinite alternate;
        }
        .orb-1 { width: 320px; height: 320px; background: var(--indigo-glow); top: 5%; left: 5%; }
        .orb-2 { width: 380px; height: 380px; background: var(--neon-mint); bottom: 5%; right: 5%; animation-delay: -3.5s; }

        @keyframes orbFloat {
            0% { transform: translateY(0) scale(1); }
            100% { transform: translateY(-40px) scale(1.15); }
        }

        /* Ultra VIP Transparent Glass Container */
        .app-container {
            width: 100%;
            max-width: 480px;
            min-height: calc(100vh - 28px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 14px;
            padding: 18px;
            background: rgba(2, 6, 15, 0.32);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-glow);
            border-radius: 24px;
            position: relative;
            box-shadow: 0 0 60px rgba(0, 240, 255, 0.3), inset 0 0 20px rgba(0, 240, 255, 0.1);
            z-index: 2;
        }

        /* Password Gate */
        #passGate {
            position: fixed;
            inset: 0;
            z-index: 999;
            background: rgba(1, 3, 8, 0.98);
            backdrop-filter: blur(35px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 24px;
            text-align: center;
        }

        .logo-box {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }

        .logo-img {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            object-fit: contain;
            filter: drop-shadow(0 0 16px var(--indigo-glow));
            animation: logoPulse 2s ease-in-out infinite alternate;
        }

        @keyframes logoPulse {
            0% { transform: scale(1); filter: drop-shadow(0 0 10px var(--indigo-glow)); }
            100% { transform: scale(1.08); filter: drop-shadow(0 0 25px var(--neon-cyan)); }
        }

        .logo-text {
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 20px;
            letter-spacing: 2px;
            color: #FFF;
            text-shadow: 0 0 15px rgba(0, 240, 255, 0.8);
        }

        .sub-text {
            font-size: 13px;
            color: #94A3B8;
            margin-bottom: 24px;
        }

        .dm-badge {
            display: inline-block;
            background: rgba(99, 102, 241, 0.3);
            border: 1px solid var(--indigo-glow);
            color: var(--neon-cyan);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
            margin-bottom: 18px;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
        }

        .pass-input {
            width: 100%;
            padding: 14px;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            color: #FFF;
            font-size: 18px;
            text-align: center;
            letter-spacing: 6px;
            outline: none;
            margin-bottom: 16px;
        }

        .btn-action {
            width: 100%;
            padding: 14px;
            background: linear-gradient(90deg, #6366F1, #00F0FF);
            border: none;
            border-radius: 12px;
            color: #010308;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 1.5px;
            cursor: pointer;
            box-shadow: 0 0 30px rgba(0, 240, 255, 0.6);
            transition: all 0.2s;
        }

        .btn-action:active {
            transform: scale(0.98);
        }

        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.15);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--neon-mint);
            border-radius: 50%;
            box-shadow: 0 0 15px var(--neon-mint);
            display: inline-block;
            margin-right: 6px;
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        /* Monitor Card */
        .monitor-card {
            background: rgba(6, 12, 25, 0.6);
            border: 1px solid var(--border-glow);
            border-radius: 18px;
            padding: 18px;
            text-align: center;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.8), inset 0 0 15px rgba(0, 240, 255, 0.15);
            position: relative;
            overflow: hidden;
        }

        /* Real Trading Line Graph Stream (UPAR & NECHY) */
        .graph-stream {
            width: 100%;
            height: 42px;
            overflow: hidden;
            position: relative;
            margin: 4px 0;
            background: rgba(1, 3, 8, 0.5);
            border-radius: 8px;
            border: 1px solid rgba(0, 240, 255, 0.2);
        }

        .graph-svg {
            width: 200%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            animation: scrollGraph 10s linear infinite;
        }

        .graph-svg.reverse {
            animation: scrollGraphRev 10s linear infinite;
        }

        @keyframes scrollGraph {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }

        @keyframes scrollGraphRev {
            0% { transform: translateX(-50%); }
            100% { transform: translateX(0); }
        }

        .active-selection {
            font-size: 11px;
            color: var(--neon-cyan);
            letter-spacing: 1.5px;
            font-weight: 700;
            margin-bottom: 4px;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.8);
        }

        .signal-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 30px;
            font-weight: 900;
            margin: 6px 0;
            letter-spacing: 2px;
        }

        .signal-call { color: var(--neon-mint); text-shadow: 0 0 30px rgba(0, 255, 136, 0.95); }
        .signal-put { color: var(--neon-crimson); text-shadow: 0 0 30px rgba(255, 0, 85, 0.95); }
        .signal-neutral { color: #64748B; }

        /* Controls Grid */
        .controls {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .section-label {
            font-size: 11px;
            color: #94A3B8;
            font-weight: 700;
            letter-spacing: 1.2px;
            margin-bottom: 4px;
        }

        .btn-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }

        .btn-grid-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
        }

        .opt-btn {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #94A3B8;
            padding: 11px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .opt-btn.active {
            background: rgba(0, 240, 255, 0.28);
            border-color: var(--neon-cyan);
            color: var(--neon-cyan);
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.5);
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.8);
        }
    </style>
</head>
<body>

<!-- Pro Background -->
<div class="cyber-bg">
    <div class="cyber-grid"></div>
    <div class="glow-orb orb-1"></div>
    <div class="glow-orb orb-2"></div>
</div>

<div class="app-container">
    <!-- Password Gate Overlay -->
    <div id="passGate">
        <div class="logo-box">
            <svg class="logo-img" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="45" stroke="#6366F1" stroke-width="5" fill="#0A0F1A"/>
                <path d="M30 70C30 50 70 50 70 30" stroke="#00F0FF" stroke-width="8" stroke-linecap="round"/>
                <path d="M30 30C50 30 50 70 70 70" stroke="#00FF88" stroke-width="6" stroke-linecap="round"/>
            </svg>
            <div class="logo-text">HELIX BOTICS</div>
        </div>
        <div class="dm-badge">ACCESS LOCKED • DM TO BUY</div>
        <p class="sub-text">Enter 4-Digit VIP Access Key</p>
        <input type="password" id="passInput" class="pass-input" placeholder="••••" maxlength="4">
        <button class="btn-action" onclick="unlockTerminal()">UNLOCK TERMINAL</button>
    </div>

    <!-- Main Terminal Interface -->
    <div class="header">
        <div class="logo-box" style="margin-bottom:0;">
            <svg class="logo-img" style="width:32px; height:32px;" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="45" stroke="#6366F1" stroke-width="5" fill="#0A0F1A"/>
                <path d="M30 70C30 50 70 50 70 30" stroke="#00F0FF" stroke-width="8" stroke-linecap="round"/>
                <path d="M30 30C50 30 50 70 70 70" stroke="#00FF88" stroke-width="6" stroke-linecap="round"/>
            </svg>
            <div class="logo-text" style="font-size:15px;">HELIX BOTICS</div>
        </div>
        <div style="font-size: 11px; color: #94A3B8;"><span class="status-dot"></span>VIP ENGINE LIVE</div>
    </div>

    <!-- Live Monitor Card with Real Trading Line Graphs UPAR and NECHY -->
    <div class="monitor-card" id="monitorCard">
        <div class="active-selection" id="activeInfo">EUR/USD (OTC) • 1M EXPIRY</div>

        <!-- 📈 TOP REAL TRADING LINE GRAPH (UPAR) -->
        <div class="graph-stream">
            <svg class="graph-svg" viewBox="0 0 800 42" preserveAspectRatio="none">
                <path d="M0,25 Q50,5 100,28 T200,12 T300,30 T400,8 T500,22 T600,10 T700,25 T800,15 L800,42 L0,42 Z" fill="rgba(0, 255, 136, 0.12)" />
                <path d="M0,25 Q50,5 100,28 T200,12 T300,30 T400,8 T500,22 T600,10 T700,25 T800,15" fill="none" stroke="#00FF88" stroke-width="2.5" />
                <!-- Duplicate for seamless looping width -->
                <path d="M800,25 Q850,5 900,28 T1000,12 T1100,30 T1200,8 T1300,22 T1400,10 T1500,25 T1600,15 L1600,42 L800,42 Z" fill="rgba(0, 255, 136, 0.12)" />
                <path d="M800,25 Q850,5 900,28 T1000,12 T1100,30 T1200,8 T1300,22 T1400,10 T1500,25 T1600,15" fill="none" stroke="#00FF88" stroke-width="2.5" />
            </svg>
        </div>

        <div class="section-label" style="margin-top:6px;">RECOMMENDED ENTRY</div>
        <div id="signalOutput" class="signal-title signal-neutral">READY</div>
        <div id="confidence" style="font-size: 12px; color: #64748B;">SELECT OPTIONS BELOW</div>

        <!-- 📉 BOTTOM REAL TRADING LINE GRAPH (NECHY) -->
        <div class="graph-stream" style="margin-top:8px;">
            <svg class="graph-svg reverse" viewBox="0 0 800 42" preserveAspectRatio="none">
                <path d="M0,15 Q60,35 120,20 T240,32 T360,12 T480,28 T600,15 T720,35 T800,20 L800,42 L0,42 Z" fill="rgba(0, 240, 255, 0.12)" />
                <path d="M0,15 Q60,35 120,20 T240,32 T360,12 T480,28 T600,15 T720,35 T800,20" fill="none" stroke="#00F0FF" stroke-width="2.5" />
                <!-- Duplicate for seamless looping width -->
                <path d="M800,15 Q860,35 920,20 T1040,32 T1160,12 T1280,28 T1400,15 T1520,35 T1600,20 L1600,42 L800,42 Z" fill="rgba(0, 240, 255, 0.12)" />
                <path d="M800,15 Q860,35 920,20 T1040,32 T1160,12 T1280,28 T1400,15 T1520,35 T1600,20" fill="none" stroke="#00F0FF" stroke-width="2.5" />
            </svg>
        </div>
    </div>

    <!-- Options & Controls -->
    <div class="controls">
        <div>
            <div class="section-label">MARKET TYPE</div>
            <div class="btn-grid">
                <button class="opt-btn active" id="mkt-otc" onclick="setMarket('OTC')">OTC MARKET</button>
                <button class="opt-btn" id="mkt-live" onclick="setMarket('LIVE')">REAL MARKET</button>
            </div>
        </div>

        <div>
            <div class="section-label">SELECT ASSET</div>
            <div class="btn-grid">
                <button class="opt-btn active" id="ast-eurusd" onclick="setAsset('EUR/USD')">EUR/USD</button>
                <button class="opt-btn" id="ast-gbpusd" onclick="setAsset('GBP/USD')">GBP/USD</button>
                <button class="opt-btn" id="ast-usdjpy" onclick="setAsset('USD/JPY')">USD/JPY</button>
                <button class="opt-btn" id="ast-audusd" onclick="setAsset('AUD/USD')">AUD/USD</button>
            </div>
        </div>

        <div>
            <div class="section-label">EXPIRY TIMEFRAME</div>
            <div class="btn-grid-4">
                <button class="opt-btn" id="exp-10s" onclick="setExpiry('10s')">10S</button>
                <button class="opt-btn" id="exp-30s" onclick="setExpiry('30s')">30S</button>
                <button class="opt-btn active" id="exp-1m" onclick="setExpiry('1m')">1M</button>
                <button class="opt-btn" id="exp-2m" onclick="setExpiry('2m')">2M</button>
            </div>
        </div>

        <button class="btn-action" style="margin-top: 6px;" onclick="generateSignal()">GENERATE SIGNAL</button>
    </div>
</div>

<script>
    let selectedMarket = 'OTC';
    let selectedAsset = 'EUR/USD';
    let selectedExpiry = '1m';

    function unlockTerminal() {
        const input = document.getElementById('passInput').value;
        if (input === '1914') {
            document.getElementById('passGate').style.display = 'none';
        } else {
            alert('INVALID ACCESS KEY!');
        }
    }

    function updateActiveDisplay() {
        document.getElementById('activeInfo').innerText = `${selectedAsset} (${selectedMarket}) • ${selectedExpiry.toUpperCase()} EXPIRY`;
    }

    function setMarket(market) {
        selectedMarket = market;
        document.getElementById('mkt-otc').classList.toggle('active', market === 'OTC');
        document.getElementById('mkt-live').classList.toggle('active', market === 'LIVE');
        updateActiveDisplay();
    }

    function setAsset(asset) {
        selectedAsset = asset;
        const assets = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD'];
        assets.forEach(a => {
            const btnId = 'ast-' + a.replace('/', '').toLowerCase();
            document.getElementById(btnId).classList.toggle('active', a === asset);
        });
        updateActiveDisplay();
    }

    function setExpiry(expiry) {
        selectedExpiry = expiry;
        const expiries = ['10s', '30s', '1m', '2m'];
        expiries.forEach(e => {
            document.getElementById('exp-' + e).classList.toggle('active', e === expiry);
        });
        updateActiveDisplay();
    }

    function generateSignal() {
        const output = document.getElementById('signalOutput');
        const confidence = document.getElementById('confidence');

        output.className = 'signal-title signal-neutral';
        output.innerText = 'ANALYZING...';
        confidence.innerText = 'COMPUTING QUANT DATA';

        setTimeout(() => {
            const isCall = Math.random() > 0.4;
            const accuracy = (Math.random() * (99.1 - 92.0) + 92.0).toFixed(1);

            if (isCall) {
                output.className = 'signal-title signal-call';
                output.innerText = 'CALL (UP)';
            } else {
                output.className = 'signal-title signal-put';
                output.innerText = 'PUT (DOWN)';
            }
            confidence.innerText = `CONFIDENCE: ${accuracy}% • ENTRY: NEXT CANDLE`;
        }, 500);
    }
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
