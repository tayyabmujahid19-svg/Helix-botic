from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

# Global storage for the latest signal
latest_signal = {
    "action": "WAITING",
    "symbol": "EUR/USD (OTC)",
    "duration": "30s",
    "broker": "QUOTEX / POCKET OPTION",
    "timestamp": "No signals received yet"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Helix Botics | Live Signal Engine</title>
    <style>
        :root {
            --bg-color: #080c14;
            --card-bg: #0f172a;
            --accent-cyan: #00f2fe;
            --accent-purple: #7928ca;
            --buy-green: #10b981;
            --sell-red: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            width: 100%;
            max-width: 480px;
            background: var(--card-bg);
            border: 1px solid rgba(0, 242, 254, 0.25);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(0, 242, 254, 0.15);
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .container::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
        }

        .brand-title {
            font-size: 28px;
            font-weight: 900;
            background: linear-gradient(135deg, var(--accent-cyan), #4f46e5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 2px;
            margin-bottom: 4px;
        }

        .subtitle {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 22px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }

        /* Password Modal Styling */
        #login-box {
            display: block;
        }

        #dashboard-content {
            display: none;
        }

        input[type="password"] {
            width: 80%;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid var(--accent-cyan);
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            font-size: 16px;
            text-align: center;
            margin-bottom: 15px;
            outline: none;
        }

        button.btn-access {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            color: #fff;
            border: none;
            padding: 12px 28px;
            border-radius: 10px;
            font-weight: 700;
            cursor: pointer;
            font-size: 14px;
        }

        .signal-box {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 20px;
        }

        .signal-direction {
            font-size: 22px;
            font-weight: 800;
            padding: 8px 18px;
            border-radius: 10px;
            letter-spacing: 1px;
        }

        .dir-BUY, .dir-CALL, .dir-UP {
            background: rgba(16, 185, 129, 0.2);
            color: var(--buy-green);
            border: 1px solid var(--buy-green);
        }

        .dir-SELL, .dir-PUT, .dir-DOWN {
            background: rgba(239, 68, 68, 0.2);
            color: var(--sell-red);
            border: 1px solid var(--sell-red);
        }

        .dir-WAITING {
            background: rgba(148, 163, 184, 0.1);
            color: var(--text-muted);
            border: 1px solid var(--text-muted);
        }

        .time-pill {
            background: rgba(0, 242, 254, 0.1);
            color: var(--accent-cyan);
            border: 1px solid var(--accent-cyan);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
        }

        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 20px;
        }

        .info-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 12px;
            border-radius: 12px;
            font-size: 13px;
            text-align: left;
        }

        .info-card span {
            display: block;
            color: var(--text-muted);
            font-size: 10px;
            margin-bottom: 4px;
            text-transform: uppercase;
        }

        .info-card strong {
            color: #ffffff;
            font-size: 14px;
        }

        .footer {
            font-size: 11px;
            color: var(--text-muted);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="brand-title">HELIX BOTICS</div>
        <div class="subtitle">Protected Signal Dashboard</div>

        <!-- LOGIN / PASSWORD SCREEN -->
        <div id="login-box">
            <p style="font-size:13px; color:var(--text-muted); margin-bottom:15px;">Enter Password to Access Live Signals</p>
            <input type="password" id="passInput" placeholder="Enter Access Code">
            <br>
            <button class="btn-access" onclick="verifyPassword()">UNLOCK SYSTEM</button>
            <p id="error-msg" style="color:var(--sell-red); font-size:12px; margin-top:10px; display:none;">Incorrect Password!</p>
        </div>

        <!-- DASHBOARD CONTENT -->
        <div id="dashboard-content">
            <div class="signal-box">
                <div>
                    <span style="display:block; font-size:10px; color:var(--text-muted); margin-bottom:4px;">LIVE SIGNAL</span>
                    <div id="sig-action" class="signal-direction dir-WAITING">WAITING</div>
                </div>
                <div>
                    <span style="display:block; font-size:10px; color:var(--text-muted); margin-bottom:4px;">EXPIRY TIMING</span>
                    <div id="sig-duration" class="time-pill">30s</div>
                </div>
            </div>

            <div class="info-grid">
                <div class="info-card">
                    <span>SYMBOL</span>
                    <strong id="sig-symbol">EUR/USD</strong>
                </div>
                <div class="info-card">
                    <span>TARGET BROKER</span>
                    <strong id="sig-broker">QUOTEX</strong>
                </div>
            </div>

            <p style="font-size:10px; color:var(--text-muted);" id="sig-time">Updated: Waiting for signal...</p>

            <div class="footer">
                Helix Botics &copy; Protected Live Engine
            </div>
        </div>
    </div>

    <script>
        function verifyPassword() {
            const pass = document.getElementById("passInput").value;
            if (pass === "1914") {
                document.getElementById("login-box").style.display = "none";
                document.getElementById("dashboard-content").style.display = "block";
                startLiveFeed();
            } else {
                document.getElementById("error-msg").style.display = "block";
            }
        }

        function startLiveFeed() {
            fetchSignal();
            setInterval(fetchSignal, 2000); // Poll for new signal every 2 seconds
        }

        function fetchSignal() {
            fetch('/api/latest-signal')
                .then(res => res.json())
                .then(data => {
                    const actionEl = document.getElementById("sig-action");
                    actionEl.innerText = data.action;
                    actionEl.className = "signal-direction dir-" + data.action;

                    document.getElementById("sig-duration").innerText = data.duration;
                    document.getElementById("sig-symbol").innerText = data.symbol;
                    document.getElementById("sig-broker").innerText = data.broker;
                    document.getElementById("sig-time").innerText = "Last Received: " + data.timestamp;
                })
                .catch(err => console.log(err));
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/latest-signal', methods=['GET'])
def get_latest_signal():
    return jsonify(latest_signal), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Empty signal payload"}), 400

        raw_action = str(data.get("action", "BUY")).upper()
        action = "BUY" if raw_action in ["BUY", "CALL", "UP"] else "SELL"
        
        symbol = data.get("symbol", "EURUSD_OTC")
        duration = str(data.get("duration", "30s")).lower()
        broker = str(data.get("broker", "QUOTEX")).upper()

        # Update global live signal state
        latest_signal = {
            "action": action,
            "symbol": symbol,
            "duration": duration,
            "broker": broker,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify({
            "status": "success",
            "engine": "Helix Botics AI",
            "message": "Signal updated live on web dashboard"
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()
