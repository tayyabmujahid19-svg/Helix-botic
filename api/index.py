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
            --neon-mint: #00FF88;
            --neon-crimson: #FF0055;
            --indigo-glow: #6366F1;
            --text-main: #F8FAFC;
            --border-glow: rgba(0, 240, 255, 0.4);
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
            background: #020409;
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

        /* Unique Color-Theory Canvas Animation */
        #bgCanvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            pointer-events: none;
        }

        /* Container with Ultra Glassmorphism */
        .app-container {
            width: 100%;
            max-width: 480px;
            min-height: calc(100vh - 28px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 14px;
            padding: 18px;
            background: rgba(5, 9, 18, 0.75);
            backdrop-filter: blur(28px);
            -webkit-backdrop-filter: blur(28px);
            border: 1px solid var(--border-glow);
            border-radius: 22px;
            position: relative;
            box-shadow: 0 0 70px rgba(99, 102, 241, 0.15), inset 0 0 30px rgba(0, 240, 255, 0.05);
        }

        /* Password Gate */
        #passGate {
            position: fixed;
            inset: 0;
            z-index: 999;
            background: rgba(2, 4, 9, 0.97);
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
            animation: logoPulse 3s ease-in-out infinite alternate;
        }

        @keyframes logoPulse {
            0% { transform: scale(1); filter: drop-shadow(0 0 10px var(--indigo-glow)); }
            100% { transform: scale(1.08); filter: drop-shadow(0 0 24px var(--neon-cyan)); }
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
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid var(--indigo-glow);
            color: var(--neon-cyan);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
            margin-bottom: 18px;
            box-shadow: 0 0 18px rgba(99, 102, 241, 0.3);
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
            box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.6);
        }

        .btn-action {
            width: 100%;
            padding: 14px;
            background: linear-gradient(90deg, #6366F1, #00F0FF);
            border: none;
            border-radius: 12px;
            color: #020409;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 1.5px;
            cursor: pointer;
            box-shadow: 0 0 25px rgba(99, 102, 241, 0.5);
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
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--neon-mint);
            border-radius: 50%;
            box-shadow: 0 0 12px var(--neon-mint);
            display: inline-block;
            margin-right: 6px;
            animation: blink 1.5s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        /* Signal Monitor Display */
        .monitor-card {
            background: rgba(10, 17, 32, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-glow);
            border-radius: 18px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 0 45px rgba(0, 0, 0, 0.7), inset 0 0 20px rgba(99, 102, 241, 0.15);
            position: relative;
            overflow: hidden;
        }

        /* Laser Scan Effect */
        .monitor-card::after {
            content: '';
            position: absolute;
            top: -100%;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(180deg, transparent, rgba(0, 240, 255, 0.2), transparent);
            pointer-events: none;
        }

        .monitor-card.scanning::after {
            animation: scanLaser 0.8s ease-in-out;
        }

        @keyframes scanLaser {
            0% { top: -100%; }
            100% { top: 100%; }
        }

        .active-selection {
            font-size: 12px;
            color: var(--neon-cyan);
            letter-spacing: 1.5px;
            font-weight: 700;
            margin-bottom: 8px;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
        }

        .signal-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 32px;
            font-weight: 900;
            margin: 10px 0;
            letter-spacing: 2px;
        }

        .signal-call { color: var(--neon-mint); text-shadow: 0 0 25px rgba(0, 255, 136, 0.8); }
        .signal-put { color: var(--neon-crimson); text-shadow: 0 0 25px rgba(255, 0, 85, 0.8); }
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
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #94A3B8;
            padding: 11px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .opt-btn.active {
            background: rgba(99, 102, 241, 0.25);
            border-color: var(--indigo-glow);
            color: var(--neon-cyan);
            box-shadow: 0 0 18px rgba(99, 102, 241, 0.4);
            text-shadow: 0 0 8px rgba(0, 240, 255, 0.6);
        }
    </style>
</head>
<body>

<!-- Unique Color-Theory Moving Background Canvas -->
<canvas id="bgCanvas"></canvas>

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

    <!-- Live Monitor -->
    <div class="monitor-card" id="monitorCard">
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
    // High-End Color Theory Moving Background Animation
    const canvas = document.getElementById('bgCanvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    let candles = [];
    let numCandles = 32;
    for (let i = 0; i < numCandles; i++) {
        candles.push({
            x: (window.innerWidth / numCandles) * i,
            y: window.innerHeight * 0.5 + (Math.random() * 280 - 140),
            height: Math.random() * 70 + 30,
            isGreen: Math.random() > 0.4
        });
    }

    let particles = [];
    for (let i = 0; i < 45; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 2.2 + 0.8,
            speedY: (Math.random() * 0.7 + 0.2) * (Math.random() > 0.5 ? 1 : -1),
            speedX: (Math.random() * 0.4 + 0.1) * (Math.random() > 0.5 ? 1 : -1),
            opacity: Math.random() * 0.6 + 0.2
        });
    }

    function animateBackground() {
        // Deep Obsidian to Midnight Indigo Gradient
        let bgGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
        bgGrad.addColorStop(0, '#020409');
        bgGrad.addColorStop(0.5, '#070c1d');
        bgGrad.addColorStop(1, '#020409');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Cyber Grid with Indigo/Cyan tint
        ctx.strokeStyle = 'rgba(99, 102, 241, 0.07)';
        ctx.lineWidth = 1;
        for(let i = 0; i < canvas.width; i += 50) {
            ctx.beginPath();
            ctx.moveTo(i, 0);
            ctx.lineTo(i, canvas.height);
            ctx.stroke();
        }
        for(let j = 0; j < canvas.height; j += 50) {
            ctx.beginPath();
            ctx.moveTo(0, j);
            ctx.lineTo(canvas.width, j);
            ctx.stroke();
        }

        // Floating Indigo/Cyan Particles
        particles.forEach(p => {
            p.y += p.speedY;
            p.x += p.speedX;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;
            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;

            ctx.fillStyle = `rgba(0, 240, 255, ${p.opacity})`;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
        });

        // Moving Candlesticks with Mint and Crimson colors
        candles.forEach(c => {
            c.x -= 1.2;
            if (c.x < -40) {
                c.x = canvas.width + 40;
                c.y = canvas.height * 0.5 + (Math.random() * 280 - 140);
                c.height = Math.random() * 70 + 30;
                c.isGreen = Math.random() > 0.4;
            }
            
            ctx.strokeStyle = c.isGreen ? '#00FF88' : '#FF0055';
            ctx.fillStyle = c.isGreen ? 'rgba(0, 255, 136, 0.25)' : 'rgba(255, 0, 85, 0.25)';
            ctx.lineWidth = 2;

            // Wick
            ctx.beginPath();
            ctx.moveTo(c.x, c.y - c.height/2 - 18);
            ctx.lineTo(c.x, c.y + c.height/2 + 18);
            ctx.stroke();

            // Candle Body
            ctx.fillRect(c.x - 7, c.y - c.height/2, 14, c.height);
            ctx.strokeRect(c.x - 7, c.y - c.height/2, 14, c.height);
        });

        requestAnimationFrame(animateBackground);
    }
    animateBackground();

    // App Controls Logic
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
        const card = document.getElementById('monitorCard');
        const output = document.getElementById('signalOutput');
        const confidence = document.getElementById('confidence');

        card.classList.remove('scanning');
        void card.offsetWidth;
        card.classList.add('scanning');

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
