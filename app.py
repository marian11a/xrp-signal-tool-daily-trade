from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

REVOLUT_TICKERS_URL = "https://revx.revolut.com/api/1.0/public/tickers"
REGION = "EEA"
TIMEOUT = 10


def normalize_symbol(symbol: str) -> str:
    symbol = (symbol or "XRP/USD").strip().upper().replace("-", "/")
    if "/" not in symbol:
        # If user types XRPUSD, default to USD quote for convenience.
        if symbol.endswith("USD") and len(symbol) > 3:
            symbol = symbol[:-3] + "/USD"
        else:
            symbol = symbol + "/USD"
    return symbol


def fetch_ticker(symbol: str):
    symbol = normalize_symbol(symbol)
    response = requests.get(
        REVOLUT_TICKERS_URL,
        params={"symbols": symbol, "region": REGION},
        timeout=TIMEOUT,
        headers={"User-Agent": "Crypto-Price-Watcher/1.0"},
    )
    response.raise_for_status()
    payload = response.json()
    rows = payload.get("data", [])

    if not rows:
        raise ValueError(f"No Revolut X ticker found for {symbol}")

    ticker = rows[0]

    def num(*keys):
        for key in keys:
            value = ticker.get(key)
            if value is not None:
                try:
                    return float(value)
                except (TypeError, ValueError):
                    pass
        return None

    # Revolut X exposes bid/ask/mid/last. Last is preferred for the displayed
    # market price, then mid, then bid/ask midpoint as a defensive fallback.
    bid = num("bid", "best_bid", "bestBid")
    ask = num("ask", "best_ask", "bestAsk")
    mid = num("mid", "mid_price", "midPrice")
    last = num("last", "last_price", "lastPrice")

    if last is not None:
        price = last
        source = "last"
    elif mid is not None:
        price = mid
        source = "mid"
    elif bid is not None and ask is not None:
        price = (bid + ask) / 2
        source = "bid/ask midpoint"
    else:
        raise ValueError(f"Ticker for {symbol} did not contain a usable price")

    return {
        "symbol": ticker.get("symbol", symbol),
        "price": price,
        "bid": bid,
        "ask": ask,
        "mid": mid,
        "last": last,
        "price_source": source,
        "timestamp": payload.get("metadata", {}).get("timestamp"),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/price")
def api_price():
    symbol = normalize_symbol(request.args.get("symbol", "XRP/USD"))
    try:
        data = fetch_ticker(symbol)
        return jsonify({"ok": True, **data})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc), "symbol": symbol}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
