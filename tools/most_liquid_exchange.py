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
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_depth"
market_depth = pd.DataFrame()
for market in listdir(main_path):
    path = main_path + "/" + market
    data = pd.read_csv(path)
    data["depth"] = data["bid_amount"] + data["ask_amount"]
    data["timestamp"] = pd.to_datetime(data["timestamp"], format="%Y.%m.%d.%H-%M")
    market_depth = market_depth.append(data, ignore_index=True)

# Bid-ask spread data
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_spread"
market_spread = pd.DataFrame()
for market in listdir(main_path):
    path = main_path + "/" + market
    data = pd.read_csv(path)
    data["spread"] = (data["lowest_ask"] - data["highest_bid"])/\
                     ((data["lowest_ask"] + data["highest_bid"])/2) * 10000
    data["timestamp"] = pd.to_datetime(data["timestamp"], format="%Y.%m.%d.%H-%M")
    market_spread = market_spread.append(data, ignore_index=True)

# Transaction data
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_data"
markets_data_dict = {}
for market in markets:
    file = f'{main_path}/{market}.csv'
    data = pd.read_csv(file)
    data["hour"] = pd.to_datetime(data["opentime"]).dt.hour
    markets_data_dict[market] = data
market_data = pd.concat(markets_data_dict).rename_axis(["market", "step"]).reset_index()

# Spread plot
# for market in markets:
#     plt.plot(market_spread.loc[market_spread["market"] == market]["timestamp"],
#              market_spread.loc[market_spread["market"] == market]["spread"],
#              label=market.capitalize())
# plt.legend()
# plt.show()

# Depth plot
# for market in markets:
#     plt.plot(market_depth.loc[market_depth["market"] == market]["timestamp"],
#              market_depth.loc[market_depth["market"] == market]["depth"],
#              label=market.capitalize())
# plt.legend()
# plt.show()

measures = ["spread", "depth", "volume", "trades"]
req_cols = ["timestamp", "market"] + measures
mle_data_full = pd.concat([market_depth, market_spread, market_data], axis=1)[req_cols]
mle_data_full = mle_data_full.loc[:, ~mle_data_full.columns.duplicated()]
mle_data_aggr = {}
mle_data_aggr["timestamp"] = mle_data_full.loc[mle_data_full["market"] == "binance"]["timestamp"]
for market in markets:
    mle_values = {}
    for measure in measures:
        current_value = mle_data_full.loc[mle_data_full["market"] == market].reset_index()[measure].copy()
        max_value = \
            mle_data_full[["timestamp", "market", measure]].groupby("timestamp").max().reset_index()[measure].copy()
        min_value = \
            mle_data_full[["timestamp", "market", measure]].groupby("timestamp").min().reset_index()[measure].copy()
        value_name = f'{measure}_mle'
        if measure in ["spread"]:
            mle_values[value_name] = ((current_value - min_value) / (max_value - min_value)) ** 2
        else:
            mle_values[value_name] = ((current_value - max_value) / (min_value - max_value)) ** 2

    col_name = f'{market}_mle'
    mle_data_aggr[col_name] = pd.concat(mle_values, axis=1).sum(axis=1)
mle_data = pd.concat(mle_data_aggr, axis=1)
mle_data["best_mle"] = mle_data[[s + "_mle" for s in markets]].min(axis=1)

# MLE plot no aggregation
# plt.rcParams["figure.figsize"] = (15, 7)
# fig, ax = plt.subplots()
# for market in markets:
#     ax.plot(mle_data["timestamp"],
#              mle_data[f'{market}_mle'],
#              label=market.capitalize())
#     ax.fill_between(mle_data["timestamp"], 0, 100, where=mle_data[f'{market}_mle'] == mle_data["best_mle"], alpha=0.1, interpolate=True)
#
# axes = plt.gca()
# axes.set_ylim([0,4.1])
# plt.title("MLE values for the different exchanges (no aggregation)")
# plt.legend(loc="upper right", bbox_to_anchor=(1.11, 1))
# trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
# plt.show()
# plt.savefig(plot_path / 'mle_hourly.png', dpi=300)



mle_data_daily_dict = np.split(mle_data, 14)
mle_data_daily = {}
mle_daily = pd.DataFrame()
for day in mle_data_daily_dict:
    for market in markets:
        mle_data_daily["timestamp"] = day.reset_index()["timestamp"][0]
        market_col = f'{market}_mle'
        mle_data_daily[market_col] = day[market_col].mean()
    mle_daily = mle_daily.append(mle_data_daily, ignore_index=True)

mle_daily["best_mle"] = mle_daily[[s + "_mle" for s in markets]].min(axis=1)
mle_daily

# MLE plot daily aggregation
# plt.rcParams["figure.figsize"] = (10, 7)
# fig, ax = plt.subplots()
# for market in markets:
#     ax.plot(mle_daily["timestamp"],
#              mle_daily[f'{market}_mle'],
#              label=market.capitalize())
#     ax.fill_between(mle_daily["timestamp"], 0, 10000, step="mid", where=mle_daily[f'{market}_mle'] == mle_daily["best_mle"] , alpha=0.1, interpolate=True)
#
# axes = plt.gca()
# axes.set_ylim([0,4.1])
# plt.title("MLE values for the different exchanges (daily aggregation)")
# plt.legend(loc="upper right")
# trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
# plt.show()
# plt.savefig(plot_path / 'mle_daily.png', dpi=300)

hourly_vol = market_data.groupby(by=["market", "hour"]).mean()[["volume", "trades"]]

hourly_vol = pd.concat([hourly_vol.reset_index(), pd.DataFrame(list(hourly_vol.index), columns=["market", "hour"])])

for market in markets:
    plt.plot(hourly_vol.loc[hourly_vol["market"] == market, "hour"],
             hourly_vol.loc[hourly_vol["market"] == market, "volume"],
             label=market.capitalize())
plt.show()