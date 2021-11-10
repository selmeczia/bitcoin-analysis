import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time

first_starttime = "1634814000000000000"
second_starttime= '1634815925481983794'
until_id = "1634817600000000000"
last_id = first_starttime
full_df = pd.DataFrame()
i = 1

while last_id < until_id:

    cols = ["price", "volume", "time", "buy/sell", "market/limit", "miscellaneous"]
    num_cols = ["price", "volume"]
    base_url = f"https://api.kraken.com/0/public/Trades?pair=xbtusd&since={last_id}"
    response = requests.get(base_url).json()
    last_id = response["result"]["last"]
    market_data = pd.DataFrame(response['result']['XXBTZUSD'], columns=cols)
    market_data = market_data.loc[market_data["time"] < int(until_id)]
    market_data["time"] = pd.to_datetime(market_data["time"], unit="s")
    market_data[num_cols] = market_data[num_cols].astype(float)

    full_df = full_df.append(market_data)
    print(i)
    i += 1
    time.sleep(1)


market_data_name = 'C:/Users/Adam/Documents/bitcoin-transactions/kraken_flash_crash.csv'
full_df.to_csv(market_data_name, index=False)

