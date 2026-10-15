"""HELIX BOTIC - Vercel serverless function (one-shot Quotex tick fetch + signal).

Flow per request: connect -> handshake -> authorize -> subscribe -> read 1-2 ticks
-> run strategy once -> return JSON -> close.

Env vars (set in Vercel > Settings > Environment Variables, never in GitHub):
  QUOTEX_SSID     your own session token (required)
  QUOTEX_WS_URL   optional override, default wss://ws.quotex.io/socket.io/?EIO=3&transport=websocket
  QUOTEX_ORIGIN   optional Origin header, default https://qxbroker.com
  BOT_API_KEY     optional; if set, callers must send it as ?key=... or X-API-Key header

Usage: GET /api?asset=EURUSD_otc

NOTE: Quotex has no official public API. The protocol below follows the format you
gave; the tick parser is tolerant because the real frame layout can change.
Results are informational only, not financial advice.
"""
import json
import os
import re
import time
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

WS_URL = os.environ.get("QUOTEX_WS_URL", "wss://ws.quotex.io/socket.io/?EIO=3&transport=websocket")
ORIGIN = os.environ.get("QUOTEX_ORIGIN", "https://qxbroker.com")
TOTAL_BUDGET = 8.0          # seconds, stays under Vercel's 10s limit
ASSET_RE = re.compile(r"^[A-Z0-9]{3,12}_otc$")


# ----------------------------- data helpers -----------------------------
def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def extract(obj, ticks, candles):
    """Walk any JSON structure and collect ticks [asset, ts, price] and OHLC dicts."""
    if isinstance(obj, dict):
        keys = set(obj)
        if {"open", "high", "low", "close"} <= keys and all(_num(obj[k]) for k in ("open", "high", "low", "close")):
            candles.append({
                "timestamp": obj.get("timestamp", obj.get("time")),
                "open": obj["open"], "high": obj["high"], "low": obj["low"], "close": obj["close"],
            })
        elif _num(obj.get("price")):
            ticks.append({"asset": obj.get("asset"), "timestamp": obj.get("timestamp", obj.get("time")), "price": obj["price"]})
        for v in obj.values():
            if isinstance(v, (dict, list)):
                extract(v, ticks, candles)
    elif isinstance(obj, list):
        if len(obj) >= 3 and isinstance(obj[0], str) and _num(obj[1]) and _num(obj[2]):
            ticks.append({"asset": obj[0], "timestamp": obj[1], "price": obj[2]})
        else:
            for v in obj:
                if isinstance(v, (dict, list)):
                    extract(v, ticks, candles)


def fetch_live(asset, ssid):
    import websocket  # websocket-client

    t0 = time.time()
    deadline = t0 + TOTAL_BUDGET
    ticks, candles = [], []
    ws = websocket.create_connection(
        WS_URL, timeout=3, origin=ORIGIN,
        header=["User-Agent: Mozilla/5.0 (compatible; HelixBotic/1.0)"],
    )
    try:
        authed_sent = False
        subscribed = False
        auth_time = 0.0
        pending_binary = False
        while time.time() < deadline and len(ticks) < 2:
            # subscribe once auth acknowledged, or after a short grace period
            if authed_sent and not subscribed and time.time() - auth_time > 1.5:
                ws.send('42["subscribe",{"asset":"%s"}]' % asset)
                subscribed = True
            try:
                msg = ws.recv()
            except websocket.WebSocketTimeoutException:
                continue
            if isinstance(msg, bytes):
                try:
                    extract(json.loads(msg.decode("utf-8", "ignore")), ticks, candles)
                except ValueError:
                    pass
                pending_binary = False
                continue
            if msg == "2":                       # engine.io ping -> pong
                ws.send("3")
            elif msg.startswith("40") and not authed_sent:   # namespace connected
                ws.send('42["authorization",%s]' % json.dumps({"session": ssid}))
                authed_sent, auth_time = True, time.time()
            elif msg.startswith("451-") or msg.startswith("45"):
                pending_binary = True            # next frame is binary payload
            elif msg.startswith("42"):
                try:
                    data = json.loads(msg[2:])
                except ValueError:
                    continue
                name = str(data[0]).lower() if isinstance(data, list) and data else ""
                if "authoriz" in name and authed_sent and not subscribed:
                    ws.send('42["subscribe",{"asset":"%s"}]' % asset)
                    subscribed = True
                extract(data, ticks, candles)
        return ticks, candles
    finally:
        try:
            ws.close()
        except Exception:
            pass


# ----------------------------- strategy -----------------------------
def ema(a, n):
    k, e, out = 2 / (n + 1), a[0], []
    for v in a:
        e = v * k + e * (1 - k)
        out.append(e)
    return out


def rsi(a, n=14):
    g = l = 0.0
    for i in range(1, n + 1):
        d = a[i] - a[i - 1]
        g += max(d, 0); l += max(-d, 0)
    g /= n; l /= n
    for i in range(n + 1, len(a)):
        d = a[i] - a[i - 1]
        g = (g * (n - 1) + max(d, 0)) / n
        l = (l * (n - 1) + max(-d, 0)) / n
    return 100.0 if l == 0 else 100 - 100 / (1 + g / l)


def strategy(closes):
    """Runs once. Needs >= 30 closes; otherwise says so instead of guessing."""
    if len(closes) < 30:
        return {"signal": "NONE", "reason": "not_enough_history",
                "detail": "Need at least 30 candles for RSI/MACD/Bollinger; got %d." % len(closes)}
    px = closes[-1]
    r = rsi(closes, 14)
    e5, e13 = ema(closes, 5)[-1], ema(closes, 13)[-1]
    macd = ema(closes, 12)[-1] - ema(closes, 26)[-1]
    w = closes[-20:]
    m = sum(w) / 20
    sd = (sum((x - m) ** 2 for x in w) / 20) ** 0.5
    pb = (px - (m - 2 * sd)) / (4 * sd) if sd else 0.5
    h, lo = max(closes[-14:]), min(closes[-14:])
    st = 50.0 if h == lo else (px - lo) / (h - lo) * 100
    votes = {
        "rsi": 1 if r < 40 else -1 if r > 60 else 0,
        "ema_5_13": 1 if e5 > e13 else -1,
        "macd": 1 if macd > 0 else -1,
        "bollinger_pb": 1 if pb < 0.3 else -1 if pb > 0.7 else 0,
        "stochastic": 1 if st < 25 else -1 if st > 75 else 0,
    }
    up = sum(1 for v in votes.values() if v > 0)
    dn = sum(1 for v in votes.values() if v < 0)
    sig = "CALL" if up >= 4 else "PUT" if dn >= 4 else "NONE"
    return {"signal": sig, "agree": max(up, dn), "of": 5, "votes": votes,
            "values": {"rsi": round(r, 2), "macd": macd, "pb": round(pb, 3), "stoch": round(st, 1)}}


# ----------------------------- HTTP handler -----------------------------
class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        need = os.environ.get("BOT_API_KEY")
        if need and (q.get("key", [""])[0] != need and self.headers.get("X-API-Key") != need):
            return self._send(401, {"ok": False, "error": "unauthorized"})

        ssid = os.environ.get("QUOTEX_SSID")
        if not ssid:
            return self._send(500, {"ok": False, "error": "QUOTEX_SSID env var is not set"})

        asset = q.get("asset", ["EURUSD_otc"])[0]
        asset = asset.split("_")[0].upper() + "_otc" if "_" in asset else asset.upper() + "_otc"
        if not ASSET_RE.match(asset):
            return self._send(400, {"ok": False, "error": "invalid asset, example: EURUSD_otc"})

        try:
            ticks, candles = fetch_live(asset, ssid)
        except Exception as e:
            return self._send(502, {"ok": False, "error": "connection_failed",
                                    "detail": type(e).__name__ + ": " + str(e)[:160],
                                    "hint": "Server may have rejected the session, blocked this IP, or changed protocol."})
        if not ticks and not candles:
            return self._send(504, {"ok": False, "error": "no_data_received", "asset": asset})

        if candles:
            c = candles[-1]
            live = {"price": c["close"], "open": c["open"], "high": c["high"], "low": c["low"],
                    "close": c["close"], "timestamp": c.get("timestamp")}
            closes = [x["close"] for x in candles]
        else:
            p = [t["price"] for t in ticks]
            live = {"price": p[-1], "open": p[0], "high": max(p), "low": min(p), "close": p[-1],
                    "timestamp": ticks[-1].get("timestamp")}
            closes = []   # ticks alone cannot give indicator history

        return self._send(200, {
            "ok": True, "asset": asset, "live": live,
            "ticks_received": len(ticks), "candles_received": len(candles),
            "analysis": strategy(closes),
            "disclaimer": "Informational only. Not financial advice; no accuracy is claimed.",
        })
