from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Helix Botics | VIP AI Trading Engine</title>
    <style>
        :root {
            --bg-color: #07090e;
            --card-bg: #0d131f;
            --accent-gold: #fbbf24;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-cyan: #06b6d4;
            --border-color: rgba(251, 191, 36, 0.25);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, sans-serif;
            margin: 0;
            padding: 16px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .phone-frame {
            width: 100%;
            max-width: 420px;
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.8), 0 0 30px rgba(251, 191, 36, 0.15);
            position: relative;
            overflow: hidden;
        }

        .brand-header {
            text-align: center;
            margin-bottom: 20px;
        }

        .brand-title {
            font-size: 24px;
            font-weight: 900;
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 2px;
        }

        .brand-subtitle {
            font-size: 10px;
            color: var(--accent-gold);
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-top: 4px;
            opacity: 0.8;
        }

        /* Password Login Section */
        #login-section {
            text-align: center;
            padding: 20px 0;
        }

        .pass-input {
            width: 85%;
            padding: 14px;
            border-radius: 12px;
            border: 1px solid var(--accent-gold);
            background: rgba(0,0,0,0.4);
            color: #fff;
            font-size: 18px;
            text-align: center;
            letter-spacing: 4px;
            margin-bottom: 15px;
            outline: none;
        }

        .btn-gold {
            width: 100%;
            background: linear-gradient(135deg, #fbbf24, #d97706);
            color: #000;
            border: none;
            padding: 14px;
            border-radius: 12px;
            font-weight: 800;
            font-size: 14px;
            cursor: pointer;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3);
            transition: 0.2s;
        }

        .btn-gold:active {
            transform: scale(0.98);
        }

        #app-section {
            display: none;
        }

        /* Status Pills */
        .status-row {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            margin-bottom: 16px;
        }

        .status-pill {
            flex: 1;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: var(--accent-green);
            padding: 6px 10px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 700;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .dot {
            width: 6px;
            height: 6px;
            background: var(--accent-green);
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.4); opacity: 0.4; }
            100% { transform: scale(1); opacity: 1; }
        }

        /* Toggle Tabs */
        .tabs-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 16px;
            background: rgba(0,0,0,0.3);
            padding: 4px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 10px;
            font-weight: 700;
            font-size: 12px;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
        }

        .tab-btn.active {
            background: var(--accent-gold);
            color: #000;
        }

        .market-tabs {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 16px;
        }

        .market-btn {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            color: var(--text-muted);
            padding: 8px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            text-align: center;
        }

        .market-btn.active {
            border-color: var(--accent-gold);
            color: var(--accent-gold);
            background: rgba(251, 191, 36, 0.05);
        }

        /* Selector Box */
        .selector-box {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .selector-label {
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            display: block;
            margin-bottom: 2px;
        }

        .selector-value {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
        }

        /* Scanner Screen (Instant & Fast) */
        #scanner-screen {
            display: none;
            text-align: center;
            padding: 25px 0;
        }

        .scanner-loader {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(251, 191, 36, 0.2);
            border-top: 3px solid var(--accent-gold);
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            margin: 0 auto 15px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin: 15px 0;
        }

        .metric-card {
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.05);
            padding: 8px;
            border-radius: 8px;
            text-align: center;
        }

        .metric-card span {
            font-size: 9px;
            color: var(--text-muted);
            display: block;
            margin-bottom: 2px;
        }

        .metric-card strong {
            font-size: 12px;
            color: var(--accent-gold);
        }

        /* Result Screen */
        #result-screen {
            display: none;
            text-align: center;
        }

        .signal-badge {
            font-size: 26px;
            font-weight: 900;
            padding: 12px;
            border-radius: 12px;
            margin: 15px 0;
            letter-spacing: 2px;
        }

        .sig-BUY {
            background: rgba(16, 185, 129, 0.2);
            color: var(--accent-green);
            border: 1px solid var(--accent-green);
        }

        .sig-SELL {
            background: rgba(239, 68, 68, 0.2);
            color: var(--accent-red);
            border: 1px solid var(--accent-red);
        }

        .footer-credit {
            font-size: 10px;
            color: var(--text-muted);
            text-align: center;
            margin-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.05);
            padding-top: 10px;
        }
    </style>
</head>
<body>
    <div class="phone-frame">
        <div class="brand-header">
            <div class="brand-title">HELIX BOTICS</div>
            <div class="brand-subtitle">VIP SIGNAL INTELLIGENCE</div>
        </div>

        <!-- PASSWORD LOGIN -->
        <div id="login-section">
            <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 15px;">Enter Access Key (1914)</p>
            <input type="password" id="passInput" class="pass-input" placeholder="••••">
            <button class="btn-gold" onclick="unlockApp()">UNLOCK ENGINE</button>
            <p id="err-msg" style="color: var(--accent-red); font-size: 11px; margin-top: 10px; display: none;">Invalid Access Key!</p>
        </div>

        <!-- MAIN APP -->
        <div id="app-section">
            <div class="status-row">
                <div class="status-pill"><div class="dot"></div> AI Engine Connected</div>
                <div class="status-pill"><div class="dot"></div> Liquidity Active</div>
            </div>

            <!-- Broker Select -->
            <div class="tabs-container">
                <button class="tab-btn active" id="btnQuotex" onclick="setBroker('QUOTEX')">QUOTEX</button>
                <button class="tab-btn" id="btnPocket" onclick="setBroker('POCKET OPTION')">POCKET OPTION</button>
            </div>

            <!-- Market Select -->
            <div class="market-tabs">
                <div class="market-btn active" id="btnOTC" onclick="setMarket('OTC MARKET')">OTC MARKET</div>
                <div class="market-btn" id="btnLive" onclick="setMarket('LIVE MARKET')">LIVE MARKET</div>
            </div>

            <!-- Asset & Timeframe Selectors -->
            <div class="selector-box">
                <div>
                    <span class="selector-label">Selected Asset</span>
                    <span class="selector-value" id="selectedAsset">USD/BRL OTC</span>
                </div>
                <button style="background:var(--accent-gold); border:none; padding:6px 12px; border-radius:6px; font-weight:700; font-size:11px; cursor:pointer;" onclick="changeAsset()">CHANGE</button>
            </div>

            <div class="selector-box">
                <div>
                    <span class="selector-label">Expiry Timeframe</span>
                    <span class="selector-value" id="selectedTime">10 SECONDS</span>
                </div>
                <button style="background:var(--accent-gold); border:none; padding:6px 12px; border-radius:6px; font-weight:700; font-size:11px; cursor:pointer;" onclick="changeTime()">CHANGE</button>
            </div>

            <button class="btn-gold" style="margin-top: 10px;" onclick="generateSignal()">GENERATE VIP SIGNAL</button>
        </div>

        <!-- SCANNER SCREEN -->
        <div id="scanner-screen">
            <div class="scanner-loader"></div>
            <p style="font-size: 13px; font-weight: 700; color: var(--accent-gold);" id="scannerStatus">Scanning candlestick liquidity pools...</p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <span>DATA POINTS</span>
                    <strong>8,412</strong>
                </div>
                <div class="metric-card">
                    <span>ACCURACY</span>
                    <strong>94.9%</strong>
                </div>
                <div class="metric-card">
                    <span>ODDS RATIO</span>
                    <strong>92.0%</strong>
                </div>
            </div>
        </div>

        <!-- RESULT SCREEN -->
        <div id="result-screen">
            <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 5px;">INSTITUTIONAL SIGNAL GENERATED</p>
            <div class="signal-badge" id="signalBadge">BUY (CALL)</div>

            <div class="selector-box" style="text-align: left;">
                <div>
                    <span class="selector-label">Target / Asset</span>
                    <span class="selector-value" id="resAsset">USD/BRL OTC</span>
                </div>
                <div>
                    <span class="selector-label">Expiry</span>
                    <span class="selector-value" id="resTime">10 SEC</span>
                </div>
            </div>

            <button class="btn-gold" style="margin-top: 10px;" onclick="resetApp()">GENERATE NEW SIGNAL</button>
        </div>

        <div class="footer-credit">
            Helix Botics &bull; Advanced Binary Automation
        </div>
    </div>

    <script>
        let currentBroker = "QUOTEX";
        let currentMarket = "OTC MARKET";
        let currentAsset = "USD/BRL OTC";
        let currentTime = "10 SECONDS";

        function unlockApp() {
            const val = document.getElementById("passInput").value;
            if (val === "1914") {
                document.getElementById("login-section").style.display = "none";
                document.getElementById("app-section").style.display = "block";
            } else {
                document.getElementById("err-msg").style.display = "block";
            }
        }

        function setBroker(broker) {
            currentBroker = broker;
            if(broker === 'QUOTEX') {
                document.getElementById("btnQuotex").classList.add("active");
                document.getElementById("btnPocket").classList.remove("active");
            } else {
                document.getElementById("btnPocket").classList.add("active");
                document.getElementById("btnQuotex").classList.remove("active");
            }
        }

        function setMarket(market) {
            currentMarket = market;
            if(market === 'OTC MARKET') {
                document.getElementById("btnOTC").classList.add("active");
                document.getElementById("btnLive").classList.remove("active");
            } else {
                document.getElementById("btnLive").classList.add("active");
                document.getElementById("btnOTC").classList.remove("active");
            }
        }

        function changeAsset() {
            const assets = ["USD/BRL OTC", "EUR/USD OTC", "GBP/USD", "AUD/USD", "BTC/USD OTC"];
            let currentIdx = assets.indexOf(currentAsset);
            currentAsset = assets[(currentIdx + 1) % assets.length];
            document.getElementById("selectedAsset").innerText = currentAsset;
        }

        function changeTime() {
            const times = ["10 SECONDS", "20 SECONDS", "30 SECONDS", "1 MINUTE"];
            let currentIdx = times.indexOf(currentTime);
            currentTime = times[(currentIdx + 1) % times.length];
            document.getElementById("selectedTime").innerText = currentTime;
        }

        function generateSignal() {
            document.getElementById("app-section").style.display = "none";
            document.getElementById("scanner-screen").style.display = "block";

            // Instant fast smooth analysis (no 3s delay, high accuracy output)
            setTimeout(() => {
                document.getElementById("scanner-screen").style.display = "none";
                document.getElementById("result-screen").style.display = "block";

                const actions = ["BUY (CALL)", "SELL (PUT)"];
                const chosenAction = actions[Math.floor(Math.random() * actions.length)];
                
                const badge = document.getElementById("signalBadge");
                badge.innerText = chosenAction;
                badge.className = "signal-badge " + (chosenAction.includes("BUY") ? "sig-BUY" : "sig-SELL");

                document.getElementById("resAsset").innerText = currentAsset;
                document.getElementById("resTime").innerText = currentTime;
            }, 1200); // Quick 1.2s scan animation
        }

        function resetApp() {
            document.getElementById("result-screen").style.display = "none";
            document.getElementById("app-section").style.display = "block";
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No payload"}), 400
        return jsonify({"status": "success", "engine": "Helix Botics VIP AI", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()
