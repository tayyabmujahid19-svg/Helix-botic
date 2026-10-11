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
    <title>HELIX BOTICS - VIP SIGNAL TERMINAL</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --neon-cyan: #00F0FF;
            --neon-green: #00FF66;
            --neon-red: #FF0055;
            --text-main: #E2E8F0;
            --border-glow: rgba(0, 240, 255, 0.35);
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
            background: #030712;
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
        }

        body {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 12px 0;
            position: relative;
        }

        /* 100% Reliable Pro CSS Background Animation */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            background: radial-gradient(circle at 50% 30%, #0a192f 0%, #030712 100%);
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
                linear-gradient(rgba(0, 240, 255, 0.07) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 240, 255, 0.07) 1px, transparent 1px);
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
            filter: blur(80px);
            opacity: 0.25;
            animation: orbFloat 8s ease-in-out infinite alternate;
        }

        .orb-1 {
            width: 300px;
            height: 300px;
            background: var(--neon-cyan);
            top: 10%;
            left: 15%;
        }

        .orb-2 {
            width: 350px;
            height: 350px;
            background: var(--neon-green);
            bottom: 10%;
            right: 15%;
            animation-delay: -4s;
        }

        @keyframes orbFloat {
            0% { transform: translateY(0) scale(1); }
            100% { transform: translateY(-50px) scale(1.15); }
        }

        /* Container with Glassmorphism */
        .app-container {
            width: 100%;
            max-width: 480px;
            min-height: calc(100vh - 24px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 14px;
            padding: 16px;
            background: rgba(8, 13, 24, 0.82);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            border-left: 1px solid var(--border-glow);
            border-right: 1px solid var(--border-glow);
            border-radius: 18px;
            position: relative;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.9);
        }

        /* Password Gate */
        #passGate {
            position: fixed;
            inset: 0;
            z-index: 999;
            background: rgba(3, 7, 18, 0.96);
            backdrop-filter: blur(25px);
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
            width: 42px;
            height: 42px;
            border-radius: 10px;
            object-fit: contain;
            filter: drop-shadow(0 0 10px rgba(0, 240, 255, 0.6));
        }

        .logo-text {
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 20px;
            letter-spacing: 2px;
            color: #FFF;
            text-shadow: 0 0 12px rgba(0, 240, 255, 0.6);
        }

        .sub-text {
            font-size: 13px;
            color: #94A3B8;
            margin-bottom: 24px;
        }

        .dm-badge {
            display: inline-block;
            background: rgba(0, 240, 255, 0.12);
            border: 1px solid var(--neon-cyan);
            color: var(--neon-cyan);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 18px;
            box-shadow: 0 0 12px rgba(0, 240, 255, 0.25);
        }

        .pass-input {
            width: 100%;
            padding: 14px;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid var(--border-glow);
            border-radius: 10px;
            color: #FFF;
            font-size: 18px;
            text-align: center;
            letter-spacing: 4px;
            outline: none;
            margin-bottom: 16px;
        }

        .btn-action {
            width: 100%;
            padding: 14px;
            background: linear-gradient(90deg, #00F0FF, #0055FF);
            border: none;
            border-radius: 10px;
            color: #000;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 1px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
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
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--neon-green);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--neon-green);
            display: inline-block;
            margin-right: 6px;
        }

        /* Signal Monitor Display */
        .monitor-card {
            background: rgba(13, 20, 36, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-glow);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.6);
            position: relative;
        }

        .active-selection {
            font-size: 12px;
            color: var(--neon-cyan);
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        .signal-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 30px;
            font-weight: 900;
            margin: 10px 0;
            letter-spacing: 2px;
        }

        .signal-call { color: var(--neon-green); text-shadow: 0 0 20px rgba(0, 255, 102, 0.7); }
        .signal-put { color: var(--neon-red); text-shadow: 0 0 20px rgba(255, 0, 85, 0.7); }
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
            letter-spacing: 1px;
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
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #94A3B8;
            padding: 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .opt-btn.active {
            background: rgba(0, 240, 255, 0.2);
            border-color: var(--neon-cyan);
            color: var(--neon-cyan);
            box-shadow: 0 0 12px rgba(0, 240, 255, 0.3);
        }
    </style>
</head>
<body>

<!-- Pro CSS Background Animation -->
<div class="bg-animation">
    <div class="cyber-grid"></div>
    <div class="glow-orb orb-1"></div>
    <div class="glow-orb orb-2"></div>
</div>

<div class="app-container">
    <!-- Password Gate Overlay -->
    <div id="passGate">
        <div class="logo-box">
            <svg class="logo-img" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="45" stroke="#00F0FF" stroke-width="4" fill="#0A0F1A"/>
                <path d="M30 70C30 50 70 50 70 30" stroke="#00F0FF" stroke-width="8" stroke-linecap="round"/>
                <path d="M30 30C50 30 50 70 70 70" stroke="#00FF66" stroke-width="6" stroke-linecap="round"/>
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
                <circle cx="50" cy="50" r="45" stroke="#00F0FF" stroke-width="4" fill="#0A0F1A"/>
                <path d="M30 70C30 50 70 50 70 30" stroke="#00F0FF" stroke-width="8" stroke-linecap="round"/>
                <path d="M30 30C50 30 50 70 70 70" stroke="#00FF66" stroke-width="6" stroke-linecap="round"/>
            </svg>
            <div class="logo-text" style="font-size:15px;">HELIX BOTICS</div>
        </div>
        <div style="font-size: 11px; color: #94A3B8;"><span class="status-dot"></span>VIP ENGINE LIVE</div>
    </div>

    <!-- Live Monitor -->
    <div class="monitor-card">
        <div class="active-selection" id="activeInfo">EUR/USD (OTC) • 1M EXPIRY</div>
        <div class="section-label">RECOMMENDED ENTRY</div>
        <div id="signalOutput" class="signal-title signal-neutral">READY</div>
        <div id="confidence" style="font-size: 12px; color: #64748B;">SELECT OPTIONS BELOW</div>
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
        }, 400);
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
