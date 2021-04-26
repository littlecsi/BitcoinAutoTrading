import pyupbit
import numpy as np
import matplotlib.pyplot as plt


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-XRP")
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

k_value = []
ror = []

for k in np.arange(0.0, 1.0, 0.05):
    k_value.append(k)
    ror.append(get_ror(k))

plt.plot(k_value, ror)
plt.xlabel("K value")
plt.ylabel("Rate of Return")
plt.show()