from websocket import create_connection
import json
import sys
import pandas as pd
import logging

def main(path, top_percent, timestamp, log_path):
    # Config
    exchange_name = "kraken"
    _timestamp = timestamp
    _top_percent = top_percent
    _path = path
    logging.basicConfig(filename=log_path, level=logging.INFO, format="%(levelname)s - %(asctime)s : %(message)s")
    api_feed = "book"
    api_symbol = "XBT/USD"
    api_depth = "1000"
    api_domain = "wss://ws.kraken.com/"
    api_book = {"bid":{}, "ask":{}}

    def dicttofloat(keyvalue):
        return float(keyvalue[0])

    def api_update_book(side, data):
        for x in data:
            price_level = x[0]
            if float(x[1]) != 0.0:
                api_book[side].update({price_level:float(x[1])})
            else:
                if price_level in api_book[side]:
                    api_book[side].pop(price_level)
            if side == "bid":
                api_book["bid"] = dict(sorted(api_book["bid"].items(), key=dicttofloat, reverse=True)[:int(api_depth)])
            elif side == "ask":
                api_book["ask"] = dict(sorted(api_book["ask"].items(), key=dicttofloat)[:int(api_depth)])

    ws = create_connection(api_domain)
    api_data = '{"event":"subscribe", "subscription":{"name":"%(feed)s", "depth":%(depth)s}, "pair":["%(symbol)s"]}' %\
               {"feed":api_feed, "depth":api_depth, "symbol":api_symbol}
    ws.send(api_data)

    signal = True
    while signal:
        try:
            api_data = ws.recv()
        except KeyboardInterrupt:
            ws.close()
            sys.exit(0)
        except Exception as error:
            print("WebSocket message failed (%s)" % error)
            ws.close()
            sys.exit(1)
        api_data = json.loads(api_data)
        if type(api_data) == list:
            if "as" in api_data[1]:
                api_update_book("ask", api_data[1]["as"])
                api_update_book("bid", api_data[1]["bs"])
                # signal.alarm(1)
            elif "a" in api_data[1] or "b" in api_data[1]:
                for x in api_data[1:len(api_data[1:])-1]:
                    if "a" in x:
                        api_update_book("ask", x["a"])
                    elif "b" in x:
                        api_update_book("bid", x["b"])
            signal = False

    # Bid (buy) side
    bids_df = pd.DataFrame([k for k in api_book["bid"].items()], columns=["price", "amount"])
    bids_df["price"] = bids_df["price"].astype(float)
    bids_df["total"] = bids_df["amount"].cumsum()
    if bids_df["price"].min() > bids_df["price"][0] * (1 - _top_percent):
        logging.warning(exchange_name + " has fewer values than necessary on the BID side! " +
                        "{:.4f}%".format(bids_df["price"].min() / bids_df["price"].max() * 100))
    bids_df = bids_df.loc[bids_df["price"] > bids_df["price"][0] * (1 - _top_percent)]
    bids_df["type"] = "buy"
    bids_df = bids_df[["amount", "total", "price", "type"]]

    # Ask (sell) side
    asks_df = pd.DataFrame([k for k in api_book["ask"].items()], columns=["price", "amount"])
    asks_df["price"] = asks_df["price"].astype(float)
    asks_df["total"] = asks_df["amount"].cumsum()
    if asks_df["price"].max() < asks_df["price"][0] * (1 + _top_percent):
        logging.warning(exchange_name + " has fewer values than necessary on the ASK side! " +
                        "{:.4f}%".format(bids_df["price"].max() / bids_df["price"].min() * 100))
    asks_df = asks_df.loc[asks_df["price"] < asks_df["price"][0] * (1 + _top_percent)]
    asks_df["type"] = "sell"
    asks_df = asks_df[["amount", "total", "price", "type"]]

    # Concatenate
    long_df = pd.concat([bids_df, asks_df])

    # Save dataframe
    name_long_df = _path + "/" + exchange_name + "/" + exchange_name + "_" + _timestamp + ".csv"
    long_df.to_csv(name_long_df, index=False)

    # Alert
    logging.info(exchange_name + " scraping done!")


if __name__ == "__main__":
    main()