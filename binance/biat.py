""""
Contains all the functions for the BinanceAutoTrading project.
"""
import config

from binance.spot import Spot

import datetime
import requests

def get_balance(client: Spot, asset: str="USDT") -> float:
    """
    Returns the account balance for a specific asset type.
    """
    assert isinstance(client, Spot)
    assert isinstance(asset, str)

    try:
        balances = client.account()["balances"]
    except:
        msg = "get_balance() - cannot get " + asset + " information."
        post_message(config.slack_token, "#debug", msg)

    for i in range(len(balances)):
        if balances[i]["asset"] == asset:
            free = balances[i]["free"]
            if free == None:
                return 0.0
            else:
                return float(free)

def get_current_price(client: Spot, asset: str) -> float:
    """"
    Returns the current price of a specific asset.
    Asset type is "BTC" by default.
    """
    assert isinstance(client, Spot)
    assert isinstance(asset, str)

    # Add "USDT" if user just inputs coin symbol
    if len(asset) <= 5: 
        asset += "USDT"

    try:
        data = client.ticker_price(asset)["price"]
    except:
        msg = "get_current_price() - cannot get " + asset + " "
        post_message(config.slack_token, "#debug", msg)

    return float(data)

def get_today() -> datetime.datetime:
    """
    Returns today's timestamp
    """
    today = datetime.datetime.utcnow().date()

    today = datetime.datetime(today.year, today.month, today.day)

    return datetime.datetime.timestamp(today)

def get_ytd_ohlcv(client: Spot, asset: str) -> list:
    """
    Returns open, high, low, close, volume data from yesterday.
    """
    assert isinstance(client, Spot)
    assert isinstance(asset, str)

    # Add "USDT" if user just inputs coin symbol
    if len(asset) <= 5: 
        asset += "USDT"

    # Receives today's timestamp and convert to "ms"
    today = int(get_today()) * 1000

    try:
        result = client.klines(asset, "1d", endTime=today)
    except:
        msg = "get_ytd_ohlcv() - cannot get " + asset + " information."
        post_message(config.slack_token, "#debug", msg)

    return result[-1][1:6]

def get_target_price(client: Spot, asset: str) -> float:
    """
    Returns target price of today.
    """
    assert isinstance(client, Spot)
    assert isinstance(asset, str)

    # Add "USDT" if user just inputs coin symbol
    if len(asset) <= 5: asset += "USDT"
    
    # today = get_tdy_ohlcv(client, asset)
    yesterday = get_ytd_ohlcv(client, asset)

    # Volatility Breakout Target calculation
    target = float(yesterday[3]) + (float(yesterday[1]) - float(yesterday[2])) * 0.5

    msg = "TARGET " + asset + " " + str(target)

    post_message(config.slack_token, "#target", msg)

    return float(round(target, 4))

def buy_crypto(client: Spot, balance: float, price: float, asset: str) -> dict:
    """
    Attemps to purchase crypto at target price.
    """
    assert isinstance(client, Spot)
    assert isinstance(balance, float)
    assert isinstance(price, float)
    assert isinstance(asset, str)

    # Add "USDT" if user just inputs coin symbol
    if len(asset) <= 5: asset += "USDT"

    # Calculate the quantity of crypto to buy
    if balance < price:
        quantity = round((balance / price), 3)
    else:
        quantity = balance // price
        
    msg = "BUY " + asset + " " + str(quantity) + " unit(s)"

    try:
        response = client.new_order(asset, "BUY", "MARKET", quantity=quantity)
    except:
        response = {}
        msg = "FAILED " + msg
        post_message(config.slack_token, '#debug', msg)
        raise Exception("Order not successful.\nPlease try again.")
    
    post_message(config.slack_token, "#trade-alert", msg)
    return response

def sell_crypto(client: Spot, quantity: float, asset: str) -> dict:
    """
    Attempts to sell crypto at market price.
    """
    assert isinstance(client, Spot)
    assert isinstance(quantity, float)
    assert isinstance(asset, str)

    # Add "USDT" if user just inputs coin symbol
    if len(asset) <= 5: asset += "USDT"

    msg = "SELL " + asset + " " + str(quantity) + " unit(s)"

    try:
        response = client.new_order(asset, "SELL", "MARKET", quantity=quantity)
    except:
        response = {}
        msg = "FAILED " + msg
        post_message(config.slack_token, '#debug', msg)
        raise Exception("Order not successful.\nPlease try again.")

    post_message(config.slack_token, "#trade-alert", msg)
    return response

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel,"text": text}
    )
    print(response)
