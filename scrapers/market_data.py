import requests
import pandas as pd
import datetime

# Config
path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_data/"
starttime = "1634289900000"
endtime = "1635498000000"

# Binance
# exchange_name = "binance"
# response = requests.get(f"https://api.binance.com/api/v3/klines?symbol=BTCBUSD&interval=1h&startTime={starttime}"
#                         f"&endTime={endtime}").json()
# cols = ["opentime", "open", "high", "low", "close", "volume", "closetime", "quote_volume", "trades",
#         "taker_base_vol", "taker_quote_vol", "irrelevant"]
# num_cols = ["open", "high", "low", "close", "volume", "quote_volume", "trades", "taker_base_vol", "taker_quote_vol"]
# market_data = pd.DataFrame(response, columns=cols).drop("irrelevant", 1)
# market_data["opentime"] = pd.to_datetime(market_data["opentime"], unit="ms")
# market_data["closetime"] = pd.to_datetime(market_data["closetime"], unit="ms")
# market_data[num_cols] = market_data[num_cols].astype(float)
#
# market_data_name = f'{path}/{exchange_name}.csv'
# market_data.to_csv(market_data_name, index=False)

# Bitfinex
# exchange_name = "bitfinex"
# response = requests.get(f'https://api-pub.bitfinex.com/v2/candles/trade:1h:tBTCUSD/hist?limit=10000&start={starttime}'
#                         f'&end={endtime}&sort=1').json()
# cols = ["opentime", "open", "close", "high", "low", "volume"]
# market_data = pd.DataFrame(response, columns=cols)
# market_data["opentime"] = pd.to_datetime(market_data["opentime"], unit="ms")
# market_data["closetime"] = market_data["opentime"] + pd.Timedelta(hours=1) - pd.Timedelta(milliseconds=1)
#
# market_data_name = f'{path}/{exchange_name}.csv'
# market_data.to_csv(market_data_name, index=False)

# Bitstamp
exchange_name = "bitstamp"
response = requests.get(f'https://www.bitstamp.net/api/v2/ohlc/btcusd/?start={starttime[:-3]}&end={endtime[:-3]}&step=3600&limit=336').json()
num_cols = ["open", "high", "low", "close", "volume"]
market_data = pd.DataFrame(response['data']['ohlc'])
market_data["opentime"] = pd.to_datetime(market_data["timestamp"], unit="s")
market_data["closetime"] = market_data["opentime"] + pd.Timedelta(hours=1) - pd.Timedelta(milliseconds=1)
market_data = market_data.drop("timestamp", 1)
market_data[num_cols] = market_data[num_cols].astype(float)

market_data