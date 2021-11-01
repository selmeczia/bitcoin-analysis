import requests
import pandas as pd
import datetime
import urllib.parse

# Config
path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_data/"
starttime = "1634289900000"
endtime = "1635498000000"
column_order = ["opentime", "closetime", "open", "high", "low", "close", "volume"]


def get_binance_market_data():
    exchange_name = "binance"
    response = requests.get(f"https://api.binance.com/api/v3/klines?symbol=BTCBUSD&interval=1h&startTime={starttime}"
                            f"&endTime={endtime}").json()
    cols = ["opentime", "open", "high", "low", "close", "volume", "closetime", "quote_volume", "trades",
            "taker_base_vol", "taker_quote_vol", "irrelevant"]
    num_cols = ["open", "high", "low", "close", "volume", "quote_volume", "trades", "taker_base_vol", "taker_quote_vol"]
    market_data = pd.DataFrame(response, columns=cols).drop("irrelevant", 1)
    market_data["opentime"] = pd.to_datetime(market_data["opentime"], unit="ms")
    market_data["closetime"] = pd.to_datetime(market_data["closetime"], unit="ms")
    market_data[num_cols] = market_data[num_cols].astype(float)

    market_data_name = f'{path}/{exchange_name}.csv'
    market_data[column_order].to_csv(market_data_name, index=False)

def get_bitfinex_market_data():
    exchange_name = "bitfinex"
    base_url = "https://api-pub.bitfinex.com/v2/candles/trade:1h:tBTCUSD/hist?limit=10000"
    response = requests.get(f'{base_url}&start={starttime}'
                            f'&end={endtime}&sort=1').json()
    cols = ["opentime", "open", "close", "high", "low", "volume"]
    market_data = pd.DataFrame(response, columns=cols)
    market_data["opentime"] = pd.to_datetime(market_data["opentime"], unit="ms")
    market_data["closetime"] = market_data["opentime"] + pd.Timedelta(hours=1) - pd.Timedelta(milliseconds=1)

    market_data_name = f'{path}/{exchange_name}.csv'
    market_data[column_order].to_csv(market_data_name, index=False)


def get_bitstamp_market_data():
    exchange_name = "bitstamp"
    base_url = "https://www.bitstamp.net/api/v2/ohlc/btcusd/"
    response = requests.get(f'{base_url}?start={starttime[:-3]}&end={endtime[:-3]}&step=3600&limit=336').json()
    num_cols = ["open", "high", "low", "close", "volume"]
    market_data = pd.DataFrame(response['data']['ohlc'])
    market_data["opentime"] = pd.to_datetime(market_data["timestamp"], unit="s")
    market_data["closetime"] = market_data["opentime"] + pd.Timedelta(hours=1) - pd.Timedelta(milliseconds=1)
    market_data = market_data.drop("timestamp", 1)
    market_data[num_cols] = market_data[num_cols].astype(float)

    market_data_name = f'{path}/{exchange_name}.csv'
    market_data[column_order].to_csv(market_data_name, index=False)


def get_coinbase_market_data():
    exchange_name = "coinbase"
    startdate_url = urllib.parse.quote_plus("2021-10-15T10:00:00+00:00")
    middate_url = urllib.parse.quote_plus("2021-10-22T10:00:00+00:00")
    enddate_url = urllib.parse.quote_plus("2021-10-29T09:00:00+00:00")
    base_url = "https://api.pro.coinbase.com/products/BTC-USD/candles"
    response_1 = requests.get(f"{base_url}?start={startdate_url}&end={middate_url}&granularity=3600").json()
    response_2 = requests.get(f"{base_url}?start={middate_url}&end={enddate_url}&granularity=3600").json()

    cols = ["opentime", "low", "high", "open", "close", "volume"]
    market_data_1 = pd.DataFrame(response_1, columns=cols)
    market_data_2 = pd.DataFrame(response_2, columns=cols)
    market_data = pd.concat([market_data_2, market_data_1], ignore_index=True)
    market_data["opentime"] = pd.to_datetime(market_data["opentime"], unit="s")
    market_data["closetime"] = market_data["opentime"] + pd.Timedelta(hours=1) - pd.Timedelta(milliseconds=1)
    market_data = market_data.sort_values(by="opentime").drop_duplicates()

    market_data_name = f'{path}/{exchange_name}.csv'
    market_data[column_order].to_csv(market_data_name, index=False)


def get_kraken_market_data():
    exchange_name = "kraken"
    cols = ["opentime", "open", "high", "low", "close", "vwap", "volume", "count"]
    num_cols = ["open", "high", "low", "close", "vwap", "volume", "count"]
    base_url = "https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=60"
    response = requests.get(f"{base_url}&since={starttime[:-3]}").json()
    market_data = pd.DataFrame(response['result']['XXBTZUSD'], columns=cols)
    market_data["opentime"] = pd.to_datetime(market_data["opentime"], unit="s")
    market_data["closetime"] = market_data["opentime"] + pd.Timedelta(hours=1) - pd.Timedelta(milliseconds=1)
    market_data = market_data.loc[market_data["opentime"] < datetime.datetime(2021, 10, 29, 10)]
    market_data[num_cols] = market_data[num_cols].astype(float)

    market_data_name = f'{path}/{exchange_name}.csv'
    market_data[column_order].to_csv(market_data_name, index=False)


if __name__ == "__main__":
    get_binance_market_data()
    get_bitfinex_market_data()
    get_bitstamp_market_data()
    get_coinbase_market_data()
    get_kraken_market_data()
