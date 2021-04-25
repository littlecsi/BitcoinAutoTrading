import pyupbit
import numpy as np

k = 0.5

# OHLCV(open, high, low, close, volume)
df = pyupbit.get_ohlcv("KRW-XRP", count=7)

# Volatility Breakout -> (high - low) * k
df['range'] = (df['high'] - df['low']) * k
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005

# ror(Rate of Return), 
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

# cumulative product => accumulated ror
df['hpr'] = df['ror'].cumprod()

# Draw Down calculation (cummax - hpr / cummax * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# Max Draw Down
print("MDD(%): ", df['dd'].max())

# Excel
df.to_excel("dd.xlsx")