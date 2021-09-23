import cbpro
import time
import os
from datetime import datetime as dt
import pandas as pd
import sys

# Config
exchange_name = "coinbase"
top_percent = 0.05
timestamp = dt.now().strftime("%Y.%m.%d.%H-%M")

# API
order_book = cbpro.OrderBook(product_id='BTC-USD')
order_book.start()
time.sleep(5)

# Ask (sell) side
asks = list(order_book._asks.items())
ask_df = pd.DataFrame([i[1][0] for i in asks])[["side", "price", "size"]].rename(columns={"side": "type", "size": "amount"})
ask_df["total"] = ask_df["amount"].cumsum()
ask_df = ask_df[["amount", "total", "price", "type"]]
ask_df = ask_df.loc[ask_df["price"] < float(ask_df["price"][0]) * (1 + top_percent)]


# Bid (buy) side
bids = list(order_book._bids.items())
bids_df = pd.DataFrame([i[1][0] for i in bids])[["side", "price", "size"]].rename(columns={"side": "type", "size": "amount"})
bids_df = bids_df.sort_values("price", ascending=False)
bids_df["total"] = bids_df["amount"].cumsum()
bids_df = bids_df[["amount", "total", "price", "type"]]
bids_df = bids_df.loc[bids_df["price"] > float(bids_df["price"].max()) * (1 - top_percent)]


# Concate
long_df = pd.concat([bids_df, ask_df])

# Save dataframe
parent = os.path.dirname(os.getcwd())
os.chdir(parent)
path = os.getcwd()
name_long_df = path + "/order_books/coinbase/" + exchange_name + "_" + timestamp + ".csv"
long_df.to_csv(name_long_df, index=False)
print("Coinbase scrape done!")
sys.exit()
# order_book.on_close()
# Todo: end program after run
