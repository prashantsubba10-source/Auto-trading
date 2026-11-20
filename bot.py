
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
