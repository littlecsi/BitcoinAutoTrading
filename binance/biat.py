""""
Contains all the functions for the BinanceAutoTrading project.
"""

from binance.spot import Spot

import datetime

def get_balance(client, asset="USDT"):
    """
    Returns the account balance for a specific asset type.
    """
    assert(isinstance(client, Spot))
    assert(isinstance(asset, str))

    balances = client.account()["balances"]

    for i in range(len(balances)):
        if balances[i]["asset"] == asset:
            return balances[i]["free"]

def get_current_price(client, asset="BTCUSDT"):
    """"
    Returns the current price of a specific asset.
    Asset type is "BTC" by default.
    """
    assert(isinstance(client, Spot))
    assert(isinstance(asset, str))

    # Add "USDT" if user just inputs coin symbol
    if len(asset) <= 4: asset += "USDT"

    return client.ticker_price(asset)["price"]

def get_today():
    """
    Returns today's timestamp
    """
    today = datetime.datetime.utcnow().date()

    today = datetime.datetime(
        today.year,
        today.month,
        today.day
    )

    return datetime.datetime.timestamp(today)

def get_ytd_ohlcv(client, asset="BTCUSDT"):
    """
    Returns open, high, low, close, volume data from yesterday.
    """
    assert(isinstance(client, Spot))
    assert(isinstance(asset, str))

    # Add "USDT" if user just inputs coin symbol
    if len(asset) <= 4: asset += "USDT"

    # Receives today's timestamp and convert to "ms"
    today = int(get_today()) * 1000

    result = client.klines(asset, "1d", endTime=today)

    return result[-1][1:6]

def get_tdy_ohlcv(client, asset="BTCUSDT"):
    """
    Returns today's open, high, low, close, volume data.
    """
    assert(isinstance(client, Spot))
    assert(isinstance(asset, str))

    if len(asset) <= 4: asset += "USDT"

    today = int(get_today()) * 1000

    result = client.klines(asset, "1d", startTime=today)

    print(datetime.datetime.fromtimestamp(result[0][6]/1000))

    return result[0][1:6]

def get_target_price(client, asset="BTCUSDT"):
    """
    Returns target price of today.
    """
    assert(isinstance(client, Spot))
    assert(isinstance(asset, str))
    
    today = get_tdy_ohlcv(client, asset)
    yesterday = get_ytd_ohlcv(client, asset)

    # Volatility Breakout Target calculation
    target = today[0] + (yesterday[1] - yesterday[2]) * 0.5

    return target