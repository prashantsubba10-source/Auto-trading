
import time
import requests
import json
from datetime import datetime

# COINDCX PAPER TRADING BOT
# Virtual balance only - NO REAL ORDERS

STARTING_BALANCE = 100.0
balance = STARTING_BALANCE
coin = 0.0

BUY_PERCENT = 0.20
TRADE_INTERVAL = 60

def get_price():
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()

    btc = next(
        item for item in data
        if item["market"] == "BTCINR"
    )
    return float(btc["last_price"])

def log(message):
    print(datetime.now(), message)

def run_bot():
    global balance, coin

    log("CoinDCX Paper Bot Started")
    log(f"Virtual balance: Rs {balance}")

    while True:
        try:
            price = get_price()
            log(f"BTC price: Rs {price:,.2f}")

            if coin == 0 and balance > 0:
                investment = balance * BUY_PERCENT
                coin = investment / price
                balance -= investment
                log(f"PAPER BUY: Rs {investment:.2f}")

            elif coin > 0:
                current_value = coin * price
                profit = current_value - (STARTING_BALANCE * BUY_PERCENT)

                if profit >= STARTING_BALANCE * 0.02:
                    balance += current_value
                    coin = 0
                    log(f"PAPER SELL: Profit Rs {profit:.2f}")

            total = balance + coin * price
            log(f"Portfolio value: Rs {total:.2f}")

        except Exception as error:
            log(f"Error: {error}")

        time.sleep(TRADE_INTERVAL)

if __name__ == "__main__":
    run_bot()

import json
import os
import urllib.request
from datetime import datetime, timezone

STATE_FILE = "state.json"
STARTING_BALANCE = 100.0
BUY_PERCENT = 0.20
TAKE_PROFIT = 0.02

def get_price():
    url = "https://api.coindcx.com/exchange/ticker"
    request = urllib.request.Request(
        url, headers={"User-Agent": "PaperTradingBot"}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.loads(response.read())

    btc = next(x for x in data if x["market"] == "BTCINR")
    return float(btc["last_price"])

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)

    return {
        "cash": STARTING_BALANCE,
        "btc": 0.0,
        "entry_price": 0.0,
        "trades": 0
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def main():
    state = load_state()
    price = get_price()

    if state["btc"] == 0:
        investment = state["cash"] * BUY_PERCENT
        if investment > 0:
            state["btc"] = investment / price
            state["cash"] -= investment
            state["entry_price"] = price
            print("PAPER BUY:", price)

    elif price >= state["entry_price"] * (1 + TAKE_PROFIT):
        value = state["btc"] * price
        state["cash"] += value
        state["btc"] = 0
        state["entry_price"] = 0
        state["trades"] += 1
        print("PAPER SELL:", price)

    portfolio = state["cash"] + state["btc"] * price

    print("Time:", datetime.now(timezone.utc))
    print("BTC price:", price)
    print("Virtual cash:", round(state["cash"], 2))
    print("Portfolio:", round(portfolio, 2))
    print("Completed trades:", state["trades"])

    save_state(state)

if __name__ == "__main__":
    main()
