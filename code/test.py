import pyupbit
import datetime

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

access = "vTONc1AEzuBo8u3ixsDLMCp9n3q9umc9K0xStqtk"
secret = "FxQNWmUGpALOjTUZt8igkGOcxsQNs86yimUbnRka"

# access = "r3vDlx2fLwquOSGPM8AwA8eulChTYuSBGKarLP9o"
# secret = "lrFcol9WkkE0OBbhFIpxz3skF0sF83mESVxFKYUy"

upbit = pyupbit.Upbit(access, secret)