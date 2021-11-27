from os import listdir
import pandas as pd
import os
from pathlib import Path
import matplotlib.transforms as mtransforms
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly


# Plot config
path = Path(os.getcwd())
plot_path = path.parent.absolute() / "plots_2"
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/"

markets = ["binance", "bitfinex", "bitstamp", "coinbase", "kraken"]

# Order book depth chart
timestamps = ["2021.10.15.19-25", "2021.10.15.20-25", "2021.10.15.21-25"]
limit = 0.005

for timestamp in timestamps:
    order_book_sn = pd.DataFrame()
    for market in markets:
        order_book = pd.read_csv(f'{main_path}/{market}/{market}_{timestamp}.csv')
        order_book["market"] = market
        order_book_sn = pd.concat([order_book_sn, order_book], ignore_index=True)

    # ECDF plot using
    plt.rcParams["figure.figsize"] = (7, 7)
    fig, ax = plt.subplots()
    i = 0
    for market in markets:

        data = order_book_sn.loc[order_book_sn["market"] == market]
        # bid side
        sns.ecdfplot(x="price", weights="amount", stat="count", complementary=True, data=data.loc[data["type"] == "buy"], ax=ax,label=market.capitalize(), color=sns.color_palette()[i])

        # ask side
        sns.ecdfplot(x="price", weights="amount", stat="count", data=data.loc[data["type"] == "sell"], ax=ax, color=sns.color_palette()[i])

        i += 1
        ax.set_xlabel("Price")
        ax.set_ylabel("Amount")
        ax.set_ylim([0, 100])
        mid_price = order_book_sn.loc[order_book_sn["market"] == "bitfinex", "price"].iloc[0]
        ax.set_xlim([mid_price * (1 - limit), mid_price * (1 + limit)])
    plt.legend()
    plt.title(f'Depth chart at {timestamp[:-6]} {timestamp[-5:].replace("-", ":")}')
    # plt.show()
    plt.savefig(plot_path / f'depth_chart_{timestamp[-5:]}.png', dpi=300)
