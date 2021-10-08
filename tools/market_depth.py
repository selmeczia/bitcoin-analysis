from os import listdir
import pandas as pd


markets = ["binance", "bitfinex", "bitstamp", "coinbase", "kraken"]
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook/order_books"

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
market_depth = {}
for market in markets:
    row_list = []
    for element in markets_dict[market]:
        lowest_bid = element.loc[element["type"] == "buy"]["price"].min()
        highest_ask = element.loc[element["type"] == "sell"]["price"].max()
        bid_amount = element.loc[element["price"] == lowest_bid]["total"].iloc[0]
        ask_amount = element.loc[element["price"] == highest_ask]["total"].iloc[0]
        timestamp = element["timestamp"][0]
        row_list.append((timestamp, bid_amount, ask_amount, market))
    market_depth[market] = pd.DataFrame(row_list, columns=("timestamp", "bid_amount", "ask_amount", "market"))

for market in market_depth:
    save_path = main_path + "/market_depth/"
    market_depth[market].to_csv(save_path + market + ".csv", index=False)





