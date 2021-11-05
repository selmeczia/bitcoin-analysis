import datetime as dt
import requests
import pandas as pd
import numpy as np

data_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_price"

end_date = int(dt.datetime.timestamp(dt.datetime(2020,9,1)))
start_date = int(dt.datetime.timestamp(dt.datetime.now()))
price_df = pd.DataFrame()
last_date = start_date

while last_date > end_date:
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000&toTs={last_date}&e=Bitfinex"
    response = requests.get(url).json()
    data = pd.DataFrame(response["Data"]["Data"])
    data["time"] = pd.to_datetime(data["time"], unit="s")
    last_date = int(dt.datetime.timestamp(data["time"][0]))
    data = data.sort_values(by="time", ascending=False)
    price_df = price_df.append(data)
    print(f'last date: {data["time"][0]}')

price_df_name = f'{data_path}/market_price_hourly.csv'
price_df.to_csv(price_df_name, index=False)

