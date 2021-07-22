import time
import pyupbit
import datetime

import bestk

access = "r3vDlx2fLwquOSGPM8AwA8eulChTYuSBGKarLP9o"
secret = "lrFcol9WkkE0OBbhFIpxz3skF0sF83mESVxFKYUy"

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

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
print("autotrade start")

k = bestk.get_k()
coin_name = "XRP"

# AutoTrade Begin
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-"+coin_name) # 9:00
        end_time = start_time + datetime.timedelta(days=1) # 9:00 + 1 day

        # 9:00 < Present < 8:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=30):
            target_price = get_target_price("KRW-"+coin_name, k)
            current_price = get_current_price("KRW-"+coin_name)

            if target_price < current_price:
                krw = get_balance("KRW")

                if krw > 5000:
                    upbit.buy_market_order("KRW-"+coin_name, krw*0.9995)

        elif end_time - datetime.timedelta(seconds=30) < now < end_time - datetime.timedelta(seconds=20):
            coin = get_balance(coin_name)

            if (coin * get_current_price("KRW-"+coin_name)) > 5000:
                upbit.sell_market_order("KRW-"+coin_name, coin*0.9995)

        else:
            k = bestk.get_k()

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)