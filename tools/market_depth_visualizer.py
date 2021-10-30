from os import listdir
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Plot config
path = Path(os.getcwd())
plot_path = path.parent.absolute() / "plots_2"

# Market depth
markets = ["binance", "bitfinex", "bitstamp", "coinbase", "kraken"]
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_depth"
market_depth = pd.DataFrame()
for market in listdir(main_path):
    path = main_path + "/" + market
    data = pd.read_csv(path)
    market_depth = market_depth.append(data, ignore_index=True)

# Bid-ask spread
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_spread"
market_spread = pd.DataFrame()
for market in listdir(main_path):
    path = main_path + "/" + market
    data = pd.read_csv(path)
    market_spread = market_spread.append(data, ignore_index=True)


# Market depth across exchanges
# plt.rcParams["figure.figsize"] = (15, 10)
# fig,axs = plt.subplots(2)
# for market in markets:
#     axs[0].plot(pd.to_datetime(market_depth.loc[market_depth["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
#             market_depth.loc[market_depth["market"] == market]["bid_amount"] +
#             market_depth.loc[market_depth["market"] == market]["ask_amount"],
#             label=market.capitalize())
# axs[0].legend()
# axs[0].set(ylabel="Depth")
# axs[0].set_title('Market depth across exchanges (sum of bid and ask volume 5%)')
#
# axs[1].plot(pd.to_datetime(market_depth.loc[market_depth["market"] == "binance"]["timestamp"], format="%Y.%m.%d.%H-%M"),
#          market_spread.loc[market_spread["market"] == "binance"][["highest_bid", "lowest_ask"]].mean(axis=1),
#          color="black", linestyle="dashed")
# axs[1].set(ylabel="Price")
# axs[1].set_title('BTC-USD price')
# for ax in fig.get_axes():
#     ax.label_outer()
# plt.show()
# plt.savefig(plot_path / 'market_depth.png', dpi=300)


# Bid-ask differences across exchanges

# plt.rcParams["figure.figsize"] = (12, 12)
# fig, axs = plt.subplots(5)
# for item, ax in enumerate(axs):
#     market = markets[item]
#     ax.plot(pd.to_datetime(market_depth.loc[market_depth["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
#             market_depth.loc[market_depth["market"] == market]["bid_amount"],
#             label="Bid volume")
#     ax.plot(pd.to_datetime(market_depth.loc[market_depth["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
#             market_depth.loc[market_depth["market"] == market]["ask_amount"],
#             label="Ask volume")
#     ax.set_title(market.capitalize())
#     if item == 0:
#         box = ax.get_position()
#         ax.set_position([box.x0, box.y0 + box.height * 0.1,
#                          box.width, box.height * 0.9])
#         ax.legend(loc='upper right', bbox_to_anchor=(1, 1.25),
#                   fancybox=True, shadow=True, ncol=5)
#
# for ax in axs.flat:
#     ax.label_outer()
# plt.tight_layout(pad=3.0)
# plt.show()
# plt.savefig(plot_path / 'bid_ask_diff.png', dpi=300)


# Market spreads across exchanges

# plt.rcParams["figure.figsize"] = (18, 5)
# for market in markets:
#     plt.plot(pd.to_datetime(market_spread.loc[market_spread["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
#              market_spread.loc[market_spread["market"] == market]["lowest_ask"] -
#              market_spread.loc[market_spread["market"] == market]["highest_bid"],
#              label=market.capitalize())
# plt.title('Market spread across exchanges')
# plt.ylabel("Spread ($)")
# plt.legend()
# plt.show()
# plt.savefig(plot_path / 'market_spread.png', dpi=300)


# Price differences

# plt.rcParams["figure.figsize"] = (15, 10)
# base_currency = "bitfinex"
# for market in markets:
#     plt.plot(pd.to_datetime(market_spread.loc[market_spread["market"] == market]["timestamp"], format="%Y.%m.%d.%H-%M"),
#              ((market_spread.loc[market_spread["market"] == market]["lowest_ask"] +
#                market_spread.loc[market_spread["market"] == market]["highest_bid"]) / 2).reset_index(drop=True) /
#              ((market_spread.loc[market_spread["market"] == base_currency]["lowest_ask"] +
#                market_spread.loc[market_spread["market"] == base_currency]["highest_bid"]) / 2).reset_index(drop=True),
#              label=market.capitalize())
# plt.title("Price differences comapred to " + base_currency.capitalize())
# plt.legend()
# current_values = plt.gca().get_yticks().tolist()
# plt.gca().set_yticks(current_values)
# plt.gca().set_yticklabels(['{:.2%}'.format(x-1) for x in current_values])
# plot_name = base_currency + "_price_diff.png"
# plt.show()
# plt.savefig(plot_path / plot_name, dpi=300)


# Hour aggregation
# market_depth["timestamp"] = pd.to_datetime(market_depth["timestamp"], format="%Y.%m.%d.%H-%M")
# market_depth["hour"] = market_depth["timestamp"].dt.hour
#
# plt.rcParams["figure.figsize"] = (8, 11)
# fig, axs = plt.subplots(5)
# for item, ax in enumerate(axs):
#     market = markets[item]
#
#     ax.bar(market_depth.loc[market_depth["market"] == market].groupby("hour")["bid_amount"].mean().index.tolist(),
#            market_depth.loc[market_depth["market"] == market].groupby("hour")["bid_amount"].mean(),
#            label='Bid volume')
#     ax.bar(market_depth.loc[market_depth["market"] == market].groupby("hour")["ask_amount"].mean().index.tolist(),
#            market_depth.loc[market_depth["market"] == market].groupby("hour")["ask_amount"].mean(),
#            bottom=market_depth.loc[market_depth["market"] == market].groupby("hour")["bid_amount"].mean(),
#            label='Ask volume')
#     ax.set_title(market.capitalize())
#     if item == 0:
#         box = ax.get_position()
#         ax.set_position([box.x0, box.y0 + box.height * 0.1,
#                          box.width, box.height * 0.9])
#         ax.legend(loc='upper right', bbox_to_anchor=(1.01, 1.25),
#                   fancybox=True, shadow=True, ncol=5)
#     if item == 4:
#         ax.set_xlabel('Bid and ask volumes in each hour (UTC)')
#
# for ax in axs.flat:
#     ax.label_outer()
# plt.tight_layout(pad=1.0)
# plt.xticks(range(0, 24))
# plt.show()
# plt.savefig(plot_path / 'hour_volumes.png', dpi=300)

#TODO: x amount of bitcoin sold - price change