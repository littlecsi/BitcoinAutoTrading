import time
import pyupbit
import datetime

import bestk

# access = "r3vDlx2fLwquOSGPM8AwA8eulChTYuSBGKarLP9o"
# secret = "lrFcol9WkkE0OBbhFIpxz3skF0sF83mESVxFKYUy"

access = "vTONc1AEzuBo8u3ixsDLMCp9n3q9umc9K0xStqtk"
secret = "FxQNWmUGpALOjTUZt8igkGOcxsQNs86yimUbnRka"

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k

    return target_price

def get_escape_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    escape_price = df.iloc[0]['close'] - (df.iloc[0]['high'] - df.iloc[0]['low']) * k

    return escape_price

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]

    return start_time

def get_balance(ticker):
    balances = upbit.get_balances()

    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# Login
upbit = pyupbit.Upbit(access, secret)
print("---Autotrade Begin---")

krw_coin = "KRW-ETC"
k = bestk.get_k(krw_coin)
buy_price = 0

# AutoTrade Begin
while True:
    try:
        now = datetime.datetime.now() + datetime.timedelta(hours=9)
        start_time = get_start_time(krw_coin)
        end_time = start_time + datetime.timedelta(days=1)

        print(now)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(krw_coin, k)
            escape_price = get_escape_price(krw_coin, k)

            current_price = get_current_price(krw_coin)

            # Volatility Breakout
            if target_price < current_price:
                krw = get_balance("KRW")

                if krw > 5000:
                    upbit.buy_market_order(krw_coin, krw*0.9995)
                    buy_price = current_price
                    print("purchased")

            # If price drops suddenly 
            elif escape_price > current_price:
                bal = get_balance(krw_coin[4:])
                
                if (bal * current_price) > 5000:
                    upbit.sell_market_order(krw_coin, bal*0.9995)
                    print("sold")

        else:
            k = bestk.get_k(krw_coin)

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)