import pandas as pd
import requests
import datetime
import numpy as np

trades_file = "C:/Users/Adam/Documents/bitcoin-transactions/bitcoinity_data.csv"
starttime = "1634289900000"
endtime = "1635498000000"
markets = ["bitfinex", "bitstamp", "coinbase", "kraken"]

raw_trades = pd.read_csv(trades_file)
raw_trades["timestamp"] = (pd.to_datetime(raw_trades["Time"]).astype(int) / 10**9)
trades = raw_trades.loc[np.logical_and(raw_trades["timestamp"] > int(starttime[:-3]),
                                       raw_trades["timestamp"] <= int(endtime[:-3]))].copy()
trades["timestamp"] = pd.to_datetime(trades["timestamp"], unit="s")
trades[markets] = round(trades[markets] * 60)

trades_data_name = 'C:/Users/Adam/Documents/bitcoin-transactions/trades.csv'
column_order = ["timestamp"] + markets
trades[column_order].to_csv(trades_data_name, index=False)

