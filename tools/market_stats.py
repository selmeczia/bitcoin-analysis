from os import listdir
import pandas as pd

markets = ["binance", "bitfinex", "bitstamp", "coinbase", "kraken"]
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_data"

markets_data_dict = {}
for market in markets:
    file = f'{main_path}/{market}.csv'
    data = pd.read_csv(file)
    markets_data_dict[market] = data

for market in markets:
    data = markets_data_dict[market]
    data["return"] = data["close"] / data["open"] - 1
    data["dollar_vol"] = data["volume"] * data["close"] / 1000000
    data["amihud"] = data["return"].abs() / data["dollar_vol"]
    data["first"] = (data["close"] - data["close"].shift(1)) / data["close"].shift(1)
    data["second"] = (data["close"].shift(1) - data["close"].shift(2)) / data["close"].shift(2)
    data["avg_trade_size"] = data["volume"] / data["trades"]

# Descriptive statistics
desc_stat = pd.DataFrame()
for market in markets:
    row = {}
    row["market"] = market
    row["avg_vol"] = markets_data_dict[market]["volume"].mean()
    row["min_vol"] = markets_data_dict[market]["volume"].min()
    row["q1_vol"] = markets_data_dict[market]["volume"].quantile(.25)
    row["med_vol"] = markets_data_dict[market]["volume"].median()
    row["q3_vol"] = markets_data_dict[market]["volume"].quantile(.75)
    row["max_vol"] = markets_data_dict[market]["volume"].max()
    row["sum_vol"] = markets_data_dict[market]["volume"].sum()
    row["stdev_vol"] = markets_data_dict[market]["volume"].std()
    desc_stat = desc_stat.append(row, ignore_index=True)


    # row["avg_dollar_vol"] = markets_data_dict[market]["dollar_vol"].mean()
    # row["sum_amihud"] = markets_data_dict[market]["amihud"].sum()
    # row["cov"] = markets_data_dict[market][["first", "second"]].cov().iloc[0,1]
    # row["avg_num_of_trades"] = markets_data_dict[market]["trades"].mean()
    # row["avg_trade_size"] = (markets_data_dict[market]["volume"] / markets_data_dict[market]["trades"]).mean()



desc_stat

desc_stat = pd.DataFrame()
for market in markets:
    row = {}
    row["market"] = market
    row["avg_trades"] = markets_data_dict[market]["trades"].mean()
    row["min_trades"] = markets_data_dict[market]["trades"].min()
    row["q1_trades"] = markets_data_dict[market]["trades"].quantile(.25)
    row["med_trades"] = markets_data_dict[market]["trades"].median()
    row["q3_trades"] = markets_data_dict[market]["trades"].quantile(.75)
    row["max_trades"] = markets_data_dict[market]["trades"].max()
    row["sum_trades"] = markets_data_dict[market]["trades"].sum()
    row["stdev_trades"] = markets_data_dict[market]["trades"].std()
    desc_stat = desc_stat.append(row, ignore_index=True)
desc_stat

desc_stat = pd.DataFrame()
for market in markets:
    row = {}
    row["market"] = market
    row["avg_trades"] = markets_data_dict[market]["avg_trade_size"].mean()
    row["min_trades"] = markets_data_dict[market]["avg_trade_size"].min()
    row["q1_trades"] = markets_data_dict[market]["avg_trade_size"].quantile(.25)
    row["med_trades"] = markets_data_dict[market]["avg_trade_size"].median()
    row["q3_trades"] = markets_data_dict[market]["avg_trade_size"].quantile(.75)
    row["max_trades"] = markets_data_dict[market]["avg_trade_size"].max()
    row["sum_trades"] = markets_data_dict[market]["avg_trade_size"].sum()
    row["stdev_trades"] = markets_data_dict[market]["avg_trade_size"].std()
    desc_stat = desc_stat.append(row, ignore_index=True)
desc_stat