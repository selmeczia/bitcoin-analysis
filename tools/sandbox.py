import datetime as dt
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

data_path = "C:/Users/Adam/Documents/bitcoin-transactions"
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_data"
price_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_price"
path = Path(os.getcwd())
plot_path = path.parent.absolute() / "plots_2"


# Hour compare Bitfinex
# bitfinex_trades_7_8 = pd.read_csv(f"{data_path}/bitfinex_7_8_trades.csv")
# bitfinex_trades_8_9 = pd.read_csv(f"{data_path}/bitfinex_8_9_trades.csv")
#
# trades_list = [bitfinex_trades_7_8, bitfinex_trades_8_9]
#
# for df in trades_list:
#     df["cumsum"] = df["amount"].cumsum()
#     df["timestamp"] = pd.to_datetime(df["timestamp"])
#
# plt.rcParams["figure.figsize"] = (17, 7)
# i = 0
# for df in trades_list:
#     if i == 0:
#         label = "7:00 - 8:00"
#     else:
#         label = "8:00 - 9:00"
#         df["timestamp"] = df["timestamp"] - pd.Timedelta(hours=1)
#     plt.plot(df["timestamp"],
#              df["cumsum"],
#              label=label)
#     i = 1
# plt.title('Cumulative sum of trade amounts on 2021-10-27 on Bitfinex')
# plt.ylabel("Cumulative volume")
# plt.legend(loc='upper right')
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(':%M'))
# plt.show()
# plt.savefig(plot_path / 'cum_vol_bitfinex_7-9.png', dpi=300)


# 2 exchange compare

# coinbase_trades_8_9 = pd.read_csv(f"{data_path}/coinbase_8_9_trades.csv")
# bitfinex_trades_8_9 = pd.read_csv(f"{data_path}/bitfinex_8_9_trades.csv")
#
# trades_list = [coinbase_trades_8_9, bitfinex_trades_8_9]
#
# for df in trades_list:
#     df["cumsum"] = df["amount"].cumsum()
#     df["timestamp"] = pd.to_datetime(df["timestamp"])
#
# plt.rcParams["figure.figsize"] = (17, 7)
#
# i = 0
# for df in trades_list:
#     if i == 0:
#         label = "Coinbase"
#     else:
#         label = "Bitfinex"
#     plt.plot(df["timestamp"],
#              df["cumsum"],
#              label=label)
#     i = 1
# plt.title('Cummulative sum of trade amounts on 2021-10-27 between 08:00 and 9:00')
# plt.ylabel("Cumulative volume")
# plt.legend(loc='upper right')

# plt.show()
# plt.savefig(plot_path / 'cum_vol_bitfinex_coinbase.png', dpi=300)


# price
# df = pd.read_csv(f"{data_path}/coinbase_8_9_trades.csv")
# plt.rcParams["figure.figsize"] = (17, 7)
# plt.plot(pd.to_datetime(df["timestamp"]),
#          df["price"])
# plt.show()

# price
start_date = dt.datetime(2021, 10, 2)
end_date = dt.datetime(2021, 11, 1)

df = pd.read_csv(f"{price_path}/market_price_hourly.csv").sort_values(by="time", ascending=True)
df["time"] = pd.to_datetime(df["time"])
df["ma"] = df["close"].rolling(window=480, min_periods=1).mean()
df["indicator"] = np.where(df["ma"] > df["close"], "sell", "buy")
df = df.loc[np.logical_and(df["time"] > start_date,
                           df["time"] < end_date)]

# plt.rcParams["figure.figsize"] = (12, 7)
# plt.plot(pd.to_datetime(df["time"]),
#          df["close"],
#          label="Price")
# plt.plot(pd.to_datetime(df["time"]),
#          df["ma"],
#          label="Moving average (20 day)")
# plt.bar(pd.to_datetime(df["time"]),
#          df["volumefrom"])
#
# plt.title("Price of BTC-USD and its 20-day moving average")
# plt.legend(loc='upper right')
#
# axes2 = plt.twinx()
# axes2.plot(x, y, color='k', label='Sine')
# axes2.set_ylim(-1, 1)
# axes2.set_ylabel('Line plot')
#
# # plt.show()
# plt.savefig(plot_path / 'moving_average_price.png', dpi=300)
#

# Price and volume (same graph)
# plt.rcParams["figure.figsize"] = (12, 7)
# fig, ax1 = plt.subplots()
# ax1.plot(pd.to_datetime(df["time"]),
#                df["close"],
#                label="Price")
# ax1.plot(pd.to_datetime(df["time"]),
#          df["ma"],
#          label="Moving average (20 day)")
# ax1.set_ylabel("Price")
# ax1.set_ylim(ymin=35000)
#
# ax2 = ax1.twinx()
# ax2.bar(pd.to_datetime(df["time"]),
#          df["volumefrom"],
#         width=0.05,
#         color='C2')
# ax2.set_ylabel("Volume")
# plt.title("Price of BTC-USD and its 20-day simple moving average (left axis) \n"
#           "Volume by hour (right axis)")
# plt.show()
# plt.savefig(plot_path / 'moving_average_price_volume.png', dpi=300)

# Price and volume (different graph)
# plt.rcParams["figure.figsize"] = (15, 10)
# fig, axs = plt.subplots(2)
# axs[0].plot(pd.to_datetime(df["time"]),
#                df["close"],
#                label="Price")
# axs[0].plot(pd.to_datetime(df["time"]),
#          df["ma"],
#          label="Moving average (20 day)")
# axs[0].set_ylabel("Price")
# axs[0].legend()
# axs[0].set_title('Price of BTC-USD and its 20-day simple moving average with volume')
#
#
# axs[1].bar(pd.to_datetime(df["time"]),
#          df["volumefrom"],
#         width=0.05,
#         color='C2')
# axs[1].set_ylabel("Volume")
# for ax in fig.get_axes():
#     ax.label_outer()
# plt.show()
# plt.savefig(plot_path / 'moving_average_price_volume_2.png', dpi=300)