import biat
import config

from binance.spot import Spot

import time
import datetime
import pprint

asset = "ETHUSDT"
target_price = 0.0

# api key/secret are required for user data endpoints
client = Spot(key=config.api_key, secret=config.api_secret)

def main():
    # Get account and balance information
    print("Current USDT balance :", biat.get_balance(client))
    print("Current ETH price :", biat.get_current_price(client, "ETH"))

    print(biat.get_ytd_ohlcv(client, asset))
    biat.get_tdy_ohlcv(client, asset)

    now = datetime.datetime.utcnow()
    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    target_price = biat.get_target_price(client, asset)

    while True:
        now = datetime.datetime.utcnow()
        
        if mid < now < mid + datetime.timedelta(seconds=10):
            target_price = biat.get_target_price(client, asset)
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

        current_price = biat.get_current_price(client, asset)

        time.sleep(10)

if __name__ == "__main__":
    main()
    
"""# Post a new order
params = {
    'symbol': 'BTCUSDT',
    'side': 'SELL',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': 0.002,
    'price': 9500
}

response = client.new_order(**params)
print(response)""" 