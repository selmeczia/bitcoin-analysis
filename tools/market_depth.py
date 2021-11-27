from os import listdir
import pandas as pd
import numpy as np


markets = ["binance", "bitfinex", "bitstamp", "coinbase", "kraken"]
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books"

# Create dictionary with files
markets_dict = {}
for market in markets:
    path = main_path + "/" + market
    filenames = listdir(path)
    files = [filename for filename in filenames if filename.endswith(".csv")]
    for file in files:
        # data = dask.dataframe.read_csv(path + "/" + file)
        data = pd.read_csv(path + "/" + file)
        timestamp = file.replace(market + "_", "").replace(".csv", "")
        data["timestamp"] = timestamp
        markets_dict.setdefault(market, [])
        markets_dict[market].append(data)

# Calculating market depth for each exchange at each timestamp
# market_depth = {}
# for market in markets:
#     row_list = []
#     for element in markets_dict[market]:
#         lowest_bid = element.loc[element["type"] == "buy"]["price"].min()
#         highest_ask = element.loc[element["type"] == "sell"]["price"].max()
#         bid_amount = element.loc[element["price"] == lowest_bid]["total"].iloc[0]
#         ask_amount = element.loc[element["price"] == highest_ask]["total"].iloc[0]
#         timestamp = element["timestamp"][0]
#         row_list.append((timestamp, bid_amount, ask_amount, market))
#     market_depth[market] = pd.DataFrame(row_list, columns=("timestamp", "bid_amount", "ask_amount", "market"))
#
# for market in market_depth:
#     save_path = main_path + "/market_depth/"
#     market_depth[market].to_csv(save_path + market + ".csv", index=False)


# Calculating market spread for each exchange at each timestamp
# market_spread = {}
# for market in markets:
#     row_list = []
#     for element in markets_dict[market]:
#         highest_bid = element.loc[element["type"] == "buy"]["price"].max()
#         lowest_ask = element.loc[element["type"] == "sell"]["price"].min()
#         timestamp = element["timestamp"][0]
#         row_list.append((timestamp, highest_bid, lowest_ask, market))
#     market_spread[market] = pd.DataFrame(row_list, columns=("timestamp", "highest_bid", "lowest_ask", "market"))
#
# for market in market_spread:
#     save_path = main_path + "/market_spread/"
#     market_spread[market].to_csv(save_path + market + ".csv", index=False)


# Calculating slippage for each exchange at each timestamp
slippage_limit = 1000000
market_slippage = pd.DataFrame()
for market in markets:
    row_list = []
    for element in markets_dict[market]:
        timestamp = element["timestamp"][0]

        try:
            slippage_buy = element.loc[np.logical_and(element["total"] * element["price"] < slippage_limit, element["type"] == "buy")]["price"].iloc[-1]
            slippage_percent_buy = element.iloc[0]["price"] / slippage_buy - 1
        except:
            slippage_percent_buy = 0

        try:
            slippage_sell = element.loc[np.logical_and(element["total"] * element["price"] < slippage_limit, element["type"] == "sell")]["price"].iloc[-1]
            slippage_percent_sell = 1 - (element.iloc[0]["price"] / slippage_sell)
        except:
            slippage_percent_sell = 0


        row_list.append((timestamp, slippage_percent_buy, slippage_percent_sell, market))
    market_slippage = market_slippage.append(pd.DataFrame(row_list, columns=("timestamp", "slippage_buy", "slippage_sell", "market")), ignore_index = True)

# market_slippage.to_csv(f'{main_path}/slippage.csv', index=False)


avg_order_size = pd.DataFrame()
for market in markets:
    row_list = []
    for element in markets_dict[market]:
        timestamp = element["timestamp"][0]

        avg_order_size_buy = element.loc[element["type"] == "buy", "amount"].mean()
        avg_order_size_sell = element.loc[element["type"] == "sell", "amount"].mean()

        row_list.append((timestamp, avg_order_size_buy, avg_order_size_sell, market))
    avg_order_size = avg_order_size.append(pd.DataFrame(row_list, columns=("timestamp", "avg_order_size_buy", "avg_order_size_sell", "market")), ignore_index = True)

# avg_order_size.to_csv(f'{main_path}/avg_order_size.csv', index=False)
