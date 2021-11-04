import datetime as dt
import requests
import pandas as pd
import numpy as np

data_path = "C:/Users/Adam/Documents/bitcoin-transactions"

# Bitfinex

# 8-9
# start_ms = "1635321600000"
# end_ms = "1635325200000"
#
# trades_df = pd.DataFrame()
# last_ts = end_ms
# while int(last_ts)-46 >= int(start_ms):
#     url = f"https://api-pub.bitfinex.com/v2/trades/tBTCUSD/hist?limit=10000&start={start_ms}&end={last_ts}&sort=-1"
#     df = pd.DataFrame(requests.get(url).json(), columns=["id", "timestamp", "amount", "price"])
#     last_ts = df["timestamp"].iloc[-1]
#     df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
#     trades_df = trades_df.append(df, ignore_index=True)
# trades_df_1 = trades_df.sort_values(by="timestamp")
#
# trades_df_name = f'{data_path}/bitfinex_8_9_trades.csv'
# trades_df_1.to_csv(trades_df_name, index=False)
#
#
# # 7-8
# start_ms = "1635318000000"
# end_ms = "1635321600000"
#
# trades_df = pd.DataFrame()
# last_ts = end_ms
# while int(last_ts)-6303 >= int(start_ms):
#     url = f"https://api-pub.bitfinex.com/v2/trades/tBTCUSD/hist?limit=10000&start={start_ms}&end={last_ts}&sort=-1"
#     df = pd.DataFrame(requests.get(url).json(), columns=["id", "timestamp", "amount", "price"])
#     last_ts = df["timestamp"].iloc[-1]
#     df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
#     trades_df = trades_df.append(df, ignore_index=True)
# trades_df_2 = trades_df.sort_values(by="timestamp")
#
# trades_df_name = f'{data_path}/bitfinex_7_8_trades.csv'
# trades_df_2.to_csv(trades_df_name, index=False)

# Coinbase
# 8-9

trades_df = pd.DataFrame()
from_id = "227210560"
last_id = "227266875"
start_ms = "1635321600000"
end_ms = "1635325200000"

i = 1
while int(from_id) <= int(last_id):

    url = f"https://api.exchange.coinbase.com/products/btc-usd/trades?after={int(from_id)+1000}"
    df = pd.DataFrame(requests.get(url).json(), columns=["time", "trade_id", "price", "size", "side"])
    from_id = df["trade_id"].iloc[0]
    df = df.sort_values(by="trade_id")
    df["time"] = pd.to_datetime(df["time"]).dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    trades_df = trades_df.append(df, ignore_index=True)

    print(i)
    i += 1

start_date = dt.datetime.utcfromtimestamp(int(start_ms[:-3])).strftime("%Y-%m-%d %H:%M:%S.%f")
end_date = dt.datetime.utcfromtimestamp(int(end_ms[:-3])).strftime("%Y-%m-%d %H:%M:%S.%f")

trades_df_1 = trades_df.loc[np.logical_and(trades_df["time"] > start_date,
                                       trades_df["time"] <= end_date)].rename(columns={"time": "timestamp",
                                                                                       "size": "amount",
                                                                                       "trade_id": "id"})
trades_df_1["amount"] = trades_df_1["amount"].astype(float)
trades_df_1.loc[trades_df_1["side"] == "buy", "amount"] = (trades_df_1.loc[trades_df_1["side"] == "buy"]["amount"] * -1)
trades_df_1 = trades_df_1.drop_duplicates()

trades_df_1 = trades_df_1[["id", "timestamp","amount", "price"]]
trades_df_name = f'{data_path}/coinbase_8_9_trades.csv'
trades_df_1.to_csv(trades_df_name, index=False, float_format='%.8f')
