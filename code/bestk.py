import pyupbit
import numpy as np
# import matplotlib.pyplot as plt


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

    for k in np.arange(0.0, 1.0, 0.2):
        k_value.append(k)
        ror.append(get_ror(coin_name, k))

    return k_value[ror.index(max(ror))]

# Plotting
# plt.plot(k_value, ror)
# plt.xlabel("K value")
# plt.ylabel("Rate of Return")
# plt.savefig('plot.png', dpi=300, bbox_inches='tight')