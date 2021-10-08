from os import listdir
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import seaborn


markets = ["binance", "bitfinex", "bitstamp", "coinbase", "kraken"]
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook/order_books/market_depth"

market_depth = pd.DataFrame()

for market in listdir(main_path):
    path = main_path + "/" + market
    data = pd.read_csv(path)
    market_depth = market_depth.append(data, ignore_index=True)

plt.rcParams["figure.figsize"] = (15,10)

for market in markets:
    plt.plot(pd.to_datetime(market_depth.loc[market_depth["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
             market_depth.loc[market_depth["market"] == market]["bid_amount"] +
             market_depth.loc[market_depth["market"] == market]["ask_amount"],
             label = market.capitalize())

plt.title('Market depth across exchanges (sum of bid and ask volume 5%)')
plt.ylabel("Depth")
plt.legend()
plt.savefig('market_depth.png', dpi=300)