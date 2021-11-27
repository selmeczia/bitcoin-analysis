from os import listdir
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
import matplotlib.transforms as mtransforms
import numpy as np

# Plot config
path = Path(os.getcwd())
plot_path = path.parent.absolute() / "plots_2"

markets = ["binance", "bitfinex", "bitstamp", "coinbase", "kraken"]


# Market depth data
slippage_df = pd.read_csv("C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/slippage.csv")
# plt.rcParams["figure.figsize"] = (15, 7)
# for market in markets:
#     plt.plot(pd.to_datetime(slippage_df.loc[slippage_df["market"] == market, "timestamp"], format="%Y.%m.%d.%H-%M"),
#              slippage_df.loc[slippage_df["market"] == market, "slippage_sell"],
#              label=market.capitalize())
# plt.title("Slippage for a $1.000.000 sell order")
# plt.ylabel("Price slippage (%)")
# plt.legend()
# # plt.show()
# plt.savefig(plot_path / '1mil_sell_price_slippage.png', dpi=300)

plt.rcParams["figure.figsize"] = (15, 7)
for market in markets:
    plt.plot(pd.to_datetime(slippage_df.loc[slippage_df["market"] == market, "timestamp"], format="%Y.%m.%d.%H-%M"),
             slippage_df.loc[slippage_df["market"] == market, "slippage_buy"],
             label=market.capitalize())
plt.title("Slippage for a $1.000.000 buy order")
plt.ylabel("Price slippage (%)")
plt.legend()
plt.show()
# plt.savefig(plot_path / '1mil_buy_price_slippage.png', dpi=300)

# slippage_df.loc[slippage_df.groupby("timestamp").slippage_sell.idxmax()][["market"]].value_counts()