from os import listdir
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import seaborn as sns


markets = ["binance", "bitfinex", "bitstamp", "coinbase", "kraken"]
markets_data_dict = {}
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_data"
path = Path(os.getcwd())
plot_path = path.parent.absolute() / "plots_2"

# Data
for market in markets:
    file = f'{main_path}/{market}.csv'
    data = pd.read_csv(file)
    markets_data_dict[market] = data

# Volume plot
# plt.rcParams["figure.figsize"] = (17, 7)
# for market in markets:
#     data = markets_data_dict[market]
#     plt.plot(pd.to_datetime(data["opentime"]),
#              data["volume"],
#              label=market.capitalize())
# plt.title('Volume per hour')
# plt.ylabel("Volume")
# plt.legend(loc='upper right')
# plt.show()
# plt.savefig(plot_path / 'vol_timeline.png', dpi=300)

# Number of trades plot
# plt.rcParams["figure.figsize"] = (17, 7)
# for market in markets:
#     data = markets_data_dict[market]
#     plt.plot(pd.to_datetime(data["opentime"]),
#              data["trades"],
#              label=market.capitalize())
# plt.title('Number of trades')
# plt.legend(loc='upper right')
# plt.show()
# plt.savefig(plot_path / 'vol_timeline.png', dpi=300)


# Hourly average trade sizes
# plt.rcParams["figure.figsize"] = (17, 7)
# for market in markets:
#     data = markets_data_dict[market]
#     plt.plot(pd.to_datetime(data["opentime"]),
#              data["trades"] / data["volume"],
#              label=market.capitalize())
# plt.title('Hourly average trade sizes')
# plt.legend(loc='upper right')
# plt.show()
# plt.savefig(plot_path / 'vol_timeline.png', dpi=300)


# Volume correlation
# plt.rcParams["figure.figsize"] = (8, 6)
# vol_corr = {}
# for market in markets:
#     vol_corr[market] = markets_data_dict[market]["volume"]
#
# vol_corr_df = pd.DataFrame(vol_corr)
# corrMatrix = vol_corr_df.corr()
# sn.heatmap(corrMatrix, annot=True, xticklabels=[each_string.capitalize() for each_string in markets],
#            yticklabels=[each_string.capitalize() for each_string in markets])
# plt.show()
# plt.savefig(plot_path / 'vol_correlation.png', dpi=300)

# Price
# plt.rcParams["figure.figsize"] = (17, 7)
# for market in markets:
#     data = markets_data_dict[market]
#     plt.plot(pd.to_datetime(data["opentime"]),
#              data["close"],
#              label=market.capitalize())
# plt.title('Number of trades')
# plt.legend(loc='upper right')
# plt.show()
# plt.savefig(plot_path / 'vol_timeline.png', dpi=300)

# Prices differences
# plt.rcParams["figure.figsize"] = (15, 10)
# base_currency = "bitfinex"
# for market in markets:
#     data = markets_data_dict[market]
#     plt.plot(pd.to_datetime(data["opentime"]),
#              data["open"] / markets_data_dict[base_currency]["open"],
#              label=market.capitalize())
# plt.title("Price differences comapred to " + base_currency.capitalize())
# plt.legend()
# current_values = plt.gca().get_yticks().tolist()
# plt.gca().set_yticks(current_values)
# plt.gca().set_yticklabels(['{:.2%}'.format(x-1) for x in current_values])
# plot_name = base_currency + "_price_diff.png"
# plt.show()
# plt.savefig(plot_path / plot_name, dpi=300)

# Distributions
# sns.displot(markets_data_dict["binance"]["trades"])
# plt.show()

# Price deviations
reference = "binance"
rest_market = markets[:markets.index(reference)] + markets[markets.index(reference) + 1:]
col_names = [s + "_dev" for s in rest_market]

price_dev = {}

for market in rest_market:
    price_dev[market] = pd.DataFrame(columns=["timestamp", "open_dev", "high_dev", "low_dev", "close_dev"])

for market in rest_market:
    ref_data = markets_data_dict[reference]
    curr_data = markets_data_dict[market]
    price_dev[market]["timestamp"] = curr_data["opentime"]
    price_dev[market]["open_dev"] = ((curr_data["open"] - ref_data["open"])/(curr_data["open"] + ref_data["open"]).mean()).abs()
    price_dev[market]["high_dev"] = ((curr_data["high"] - ref_data["high"])/(curr_data["high"] + ref_data["high"]).mean()).abs()
    price_dev[market]["low_dev"] = ((curr_data["low"] - ref_data["low"])/(curr_data["low"] + ref_data["low"]).mean()).abs()
    price_dev[market]["close_dev"] = ((curr_data["close"] - ref_data["close"])/(curr_data["close"] + ref_data["close"]).mean()).abs()

    plt.plot(pd.to_datetime(price_dev[market]["timestamp"]),
             price_dev[market]["open_dev"],
             label=market)
price_dev
plt.legend()
plt.show()
