import pyupbit
import numpy as np

import datetime

def get_ror(coin_name, k = 0.5):
    df = pyupbit.get_ohlcv(coin_name)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]

    return ror

def get_k(coin_name):
    k_value = []
    ror = []

    for k in np.arange(0.1, 1.0, 0.05):
        k_value.append(k)
        ror.append(get_ror(coin_name, k))

    return k_value[ror.index(max(ror))]

access = "r3vDlx2fLwquOSGPM8AwA8eulChTYuSBGKarLP9o"
secret = "lrFcol9WkkE0OBbhFIpxz3skF0sF83mESVxFKYUy"

upbit = pyupbit.Upbit(access, secret)

start = datetime.datetime.now()

get_k("KRW-ETC")

print(datetime.datetime.now() - start)