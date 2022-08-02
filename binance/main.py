import biat
import config

from binance.spot import Spot

import time
import datetime

asset = "ETHUSDT"
balance = 0.0
target_price = 0.0

# api key/secret are required for user data endpoints
client = Spot(key=config.api_key, secret=config.api_secret)

def main():
    now = datetime.datetime.utcnow()
    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    target_price = biat.get_target_price(client, asset)

    while True:
        now = datetime.datetime.utcnow()
        
        # When the day ends
        if mid < now < mid + datetime.timedelta(seconds=10):
            # Calculate new target price for the next day.
            target_price = biat.get_target_price(client, asset)

            # Update next day
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

            # Sell crypto
            biat.sell_crypto(client, biat.get_balance(client, asset), asset)

        current_price = biat.get_current_price(client, asset)

        # If the current price reaches the target price
        if current_price >= target_price:
            # Get the entire balance of USDT dollars
            balance = biat.get_balance(client, "USDT")

            # Purchase the maximum amount of crypto user can order.
            biat.buy_crypto(client, balance, target_price, asset)

        time.sleep(10)

if __name__ == "__main__":
    main()