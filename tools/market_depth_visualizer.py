from os import listdir
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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

# Market depth across exchanges

# plt.rcParams["figure.figsize"] = (15,10)
# for market in markets:
#     plt.plot(pd.to_datetime(market_depth.loc[market_depth["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
#              market_depth.loc[market_depth["market"] == market]["bid_amount"] +
#              market_depth.loc[market_depth["market"] == market]["ask_amount"],
#              label = market.capitalize())
#
# plt.title('Market depth across exchanges (sum of bid and ask volume 5%)')
# plt.ylabel("Depth")
# plt.legend()
# plt.savefig('market_depth.png', dpi=300)


# Bid-ask differences across exchanges

# plt.rcParams["figure.figsize"] = (15,15)
# fig, axs = plt.subplots(5)
# for item, ax in enumerate(axs):
#     market = markets[item]
#     ax.plot(pd.to_datetime(market_depth.loc[market_depth["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
#              market_depth.loc[market_depth["market"] == market]["bid_amount"],
#             label="Bid volume")
#     ax.plot(pd.to_datetime(market_depth.loc[market_depth["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
#              market_depth.loc[market_depth["market"] == market]["ask_amount"],
#             label="Ask volume")
#     ax.set_title(market.capitalize())
#     if item == 0:
#         box = ax.get_position()
#         ax.set_position([box.x0, box.y0 + box.height * 0.1,
#                          box.width, box.height * 0.9])
#         ax.legend(loc='upper right', bbox_to_anchor=(1, 1.2),
#                   fancybox=True, shadow=True, ncol=5)
#
# for ax in axs.flat:
#     ax.label_outer()
#
# plt.tight_layout(pad=3.0)
# plt.savefig('bid_ask_diff.png', dpi=300)


# Bid-ask spread
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook/order_books/market_spread"

market_spread = pd.DataFrame()

for market in listdir(main_path):
    path = main_path + "/" + market
    data = pd.read_csv(path)
    market_spread = market_spread.append(data, ignore_index=True)

# plt.rcParams["figure.figsize"] = (15,10)
# for market in markets:
#     plt.plot(pd.to_datetime(market_spread.loc[market_spread["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
#              market_spread.loc[market_spread["market"] == market]["lowest_ask"] -
#              market_spread.loc[market_spread["market"] == market]["highest_bid"],
#              label = market.capitalize())
# plt.title('Market spread across exchanges')
# plt.ylabel("Spread")
# plt.legend()
# plt.savefig('market_spread.png', dpi=300)


# Price differences
plt.rcParams["figure.figsize"] = (15,10)
base_currency = "kraken"
for market in markets:
    plt.plot(pd.to_datetime(market_spread.loc[market_spread["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
             ((market_spread.loc[market_spread["market"] == market]["lowest_ask"] +
               market_spread.loc[market_spread["market"] == market]["highest_bid"]) / 2).reset_index(drop=True) /
             ((market_spread.loc[market_spread["market"] == base_currency]["lowest_ask"] +
               market_spread.loc[market_spread["market"] == base_currency]["highest_bid"]) / 2).reset_index(drop=True),
             label = market.capitalize())
plt.title("")
plt.legend()
plt.gca().set_yticklabels(['{:.0f}%'.format(x) for x in plt.gca().get_yticks()])
plt.show()
# plot_name = base_currency + "_price_diff.png"
# plt.savefig(plot_name, dpi=300)