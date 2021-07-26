import time
import pyupbit
import datetime
import schedule
from fbprophet import Prophet

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

predicted_close_price = 0
def predict_price(ticker):
    global predicted_close_price

    df = pyupbit.get_ohlcv(ticker, interval="minute60")
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds','y']]

    model = Prophet()
    model.fit(data)

    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]

    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]

    closeValue = closeDf['yhat'].values[0]
    predicted_close_price = closeValue

predict_price("KRW-BTC")
schedule.every().hour.do(lambda: predict_price("KRW-BTC"))

# Login
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

coin_name = "XRP"

# AutoTrade Begins
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-" + coin_name)
        end_time = start_time + datetime.timedelta(days=1)
        schedule.run_pending()

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-" + coin_name, 0.5)
            current_price = get_current_price("KRW-" + coin_name)

            if target_price < current_price and current_price < predicted_close_price:
                krw = get_balance("KRW")

                if krw > 5000:
                    upbit.buy_market_order("KRW-" + coin_name, krw*0.9995)
        else:
            coin = get_balance(coin_name)
            curr_coin = get_current_price("KRW-" + coin_name)

            if (coin * curr_coin) > 0.00008:
                upbit.sell_market_order("KRW-" + coin_name, coin*0.9995)

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)