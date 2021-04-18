import pyupbit

access = "V3kfwvQHgY4K5sTOQpZ0C343SCecF1uBtdpqQC2g"          # 본인 값으로 변경
secret = "4BcaUXpVHGqqAcY1SIVLIBBxh8PGPbsBHyPxWIx5"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))  