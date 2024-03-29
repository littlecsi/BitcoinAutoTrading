import biat
import config

from binance.spot import Spot

import time
import datetime

asset = "XRP"
balance = 0.0
target_price = 0.0

# api key/secret are required for user data endpoints
client = Spot(key=config.api_key, secret=config.api_secret)

def main():
    print("Binance Auto Trading Start...")

    now = datetime.datetime.utcnow()
    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    balance = biat.get_balance(client, "USDT")
    target_price = biat.get_target_price(client, asset)

    while True:
        now = datetime.datetime.utcnow()
        current_price = biat.get_current_price(client, asset)
        
        # When the day ends
        if mid < now < mid + datetime.timedelta(seconds=10):
            # Calculate new target price for the next day.
            target_price = biat.get_target_price(client, asset)

            # Update next day
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

            coin = biat.get_balance(client, asset)
            if (coin > 0) and (current_price < target_price):
                # Sell crypto
                biat.sell_crypto(client, coin, asset)

                # Update balance
                balance = biat.get_balance(client, "USDT")
            else:
                biat.post_message(config.slack_token, "#trade-alert", "NOTHING TO SELL")

        # If the current price reaches the target price
        if (current_price >= target_price) and (balance > current_price):
            # Purchase the maximum amount of crypto user can order.
            biat.buy_crypto(client, balance, target_price, asset)
            
            # Update balance
            balance = biat.get_balance(client, "USDT")

        time.sleep(2)

if __name__ == "__main__":
    main()
