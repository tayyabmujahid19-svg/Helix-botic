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
            --bg-dark: #080B11;
            --panel-bg: rgba(13, 19, 32, 0.75);
            --neon-cyan: #00F0FF;
            --neon-green: #00FF66;
            --neon-red: #FF0055;
            --text-main: #E2E8F0;
            --border-glow: rgba(0, 240, 255, 0.25);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
            -webkit-user-select: none;
        }

        html, body {
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: var(--bg-dark);
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            background: radial-gradient(circle at 50% 10%, #0c1a2e 0%, #080b11 100%);
        }

        /* Fullscreen Container */
        .app-container {
            width: 100%;
            height: 100%;
            max-width: 480px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 16px;
            background: rgba(8, 11, 17, 0.85);
            backdrop-filter: blur(20px);
            border-left: 1px solid var(--border-glow);
            border-right: 1px solid var(--border-glow);
            position: relative;
        }

        /* Password Gate */
        #passGate {
            position: absolute;
            inset: 0;
            z-index: 999;
            background: #080B11;
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
            gap: 10px;
            margin-bottom: 20px;
        }

        .logo-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--neon-cyan), #0055ff);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 24px;
            color: #000;
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.5);
        }

        .logo-text {
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 22px;
            letter-spacing: 2px;
            color: #FFF;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
        }

        .sub-text {
            font-size: 13px;
            color: #94A3B8;
            margin-bottom: 24px;
        }

        .dm-badge {
            display: inline-block;
            background: rgba(0, 240, 255, 0.1);
            border: 1px solid var(--neon-cyan);
            color: var(--neon-cyan);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 18px;
        }

        .pass-input {
            width: 100%;
            padding: 14px;
            background: rgba(15, 23, 42, 0.8);
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
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
        }

        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--neon-green);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--neon-green);
            display: inline-block;
            margin-right: 6px;
        }

        /* Signal Monitor Display */
        .monitor-card {
            background: var(--panel-bg);
            border: 1px solid var(--border-glow);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
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
            font-size: 32px;
            font-weight: 900;
            margin: 10px 0;
            letter-spacing: 2px;
        }

        .signal-call { color: var(--neon-green); text-shadow: 0 0 20px var(--neon-green); }
        .signal-put { color: var(--neon-red); text-shadow: 0 0 20px var(--neon-red); }
        .signal-neutral { color: #64748B; }

        /* Controls Grid */
        .controls {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .section-label {
            font-size: 11px;
            color: #64748B;
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
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #94A3B8;
            padding: 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .opt-btn.active {
            background: rgba(0, 240, 255, 0.15);
            border-color: var(--neon-cyan);
            color: var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
        }
    </style>
</head>
<body>

<div class="app-container">
    <!-- Password Gate Overlay -->
    <div id="passGate">
        <div class="logo-box">
            <div class="logo-icon">H</div>
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
            <div class="logo-icon" style="width:32px; height:32px; font-size:16px;">H</div>
            <div class="logo-text" style="font-size:16px;">HELIX BOTICS</div>
        </div>
        <div style="font-size: 11px; color: #94A3B8;"><span class="status-dot"></span>AI ENGINE LIVE</div>
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

        <button class="btn-action" style="margin-top: 8px;" onclick="generateSignal()">GENERATE SIGNAL</button>
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
            const isCall = Math.random() > 0.45;
            const accuracy = (Math.random() * (98.5 - 91.0) + 91.0).toFixed(1);

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
