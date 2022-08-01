import biat
import config

from binance.spot import Spot

import time
import datetime
import pprint

# api key/secret are required for user data endpoints
client = Spot(key=config.api_key, secret=config.api_secret)

# Get account and balance information
print("Current USDT balance :", biat.get_balance(client))
print("Current XRP price :", biat.get_current_price(client, "ETH"))
# pprint.pprint(client.ticker_24hr("ETHUSDT"))

print("time :", datetime.datetime.fromtimestamp(client.time()['serverTime'] / 1000))

print(biat.get_ytd_ohlcv(client, "ETHUSDT"))

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