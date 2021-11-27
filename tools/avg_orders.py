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
avg_order_size = pd.read_csv("C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/avg_order_size.csv")
plt.rcParams["figure.figsize"] = (15, 7)
for market in markets:
    plt.plot(pd.to_datetime(avg_order_size.loc[avg_order_size["market"] == market, "timestamp"], format="%Y.%m.%d.%H-%M"),
             avg_order_size.loc[avg_order_size["market"] == market, "avg_order_size_sell"],
             label=market.capitalize())
plt.title("Average order sizes")
plt.ylabel("BTC")
plt.legend()
plt.show()
# plt.savefig(plot_path / 'average_order_size.png', dpi=300)

