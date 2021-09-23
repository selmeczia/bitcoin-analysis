import pandas as pd
import numpy as np
import os
from datetime import datetime as dt
import requests


# Config
exchange_name = "bitstamp"
timestamp = dt.now().strftime("%Y.%m.%d.%H-%M")
top_percent = 0.05

# Get response
response = requests.get("https://www.bitstamp.net/api/v2/order_book/btcusd/").json()

# Bid (buy) side
bids_df = pd.DataFrame(response["bids"], columns=["price", "amount"])
bids_df["price"] = bids_df["price"].astype(float)
bids_df["amount"] = bids_df["amount"].astype(float)
bids_df["total"] = bids_df["amount"].cumsum()
bids_df = bids_df.loc[bids_df["price"] > bids_df["price"][0] * (1 - top_percent)]
bids_df["type"] = "buy"
bids_df = bids_df[["amount", "total", "price", "type"]]

# Ask (sell) side
asks_df = pd.DataFrame(response["asks"], columns=["price", "amount"])
asks_df["price"] = asks_df["price"].astype(float)
asks_df["amount"] = asks_df["amount"].astype(float)
asks_df["total"] = asks_df["amount"].cumsum()
asks_df = asks_df.loc[asks_df["price"] < asks_df["price"][0] * (1 + top_percent)]
asks_df["type"] = "sell"
asks_df = asks_df[["amount", "total", "price", "type"]]

# Concatenate
long_df = pd.concat([bids_df, asks_df])

# Save dataframe
parent = os.path.dirname(os.getcwd())
os.chdir(parent)
path = os.getcwd()
name_long_df = path + "/order_books/bitstamp/" + exchange_name + "_" + timestamp + ".csv"
long_df.to_csv(name_long_df, index=False)



