import pyupbit

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# access = "vTONc1AEzuBo8u3ixsDLMCp9n3q9umc9K0xStqtk"
# secret = "FxQNWmUGpALOjTUZt8igkGOcxsQNs86yimUbnRka"

access = "r3vDlx2fLwquOSGPM8AwA8eulChTYuSBGKarLP9o"
secret = "lrFcol9WkkE0OBbhFIpxz3skF0sF83mESVxFKYUy"

upbit = pyupbit.Upbit(access, secret)

# print(upbit.get_balance("KRW-XRP"))
# print(upbit.get_balance("KRW"))

print(get_balance("XRP") * get_current_price("KRW-XRP"))