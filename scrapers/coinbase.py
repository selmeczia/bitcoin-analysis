import cbpro
import time
import os
import pandas as pd
import logging


def main(path, top_percent, timestamp, log_path):
    # Config
    exchange_name = "coinbase"
    _timestamp = timestamp
    _top_percent = top_percent
    _path = path
    logging.basicConfig(filename=log_path, level=logging.INFO, format="%(levelname)s - %(asctime)s : %(message)s")

    # API
    order_book = cbpro.OrderBook(product_id='BTC-USD')
    order_book.start()
    time.sleep(5)

    # Bid (buy) side
    bids = list(order_book._bids.items())
    bids_df = pd.DataFrame([i[1][0] for i in bids])[["side", "price", "size"]].rename(columns={"side": "type", "size": "amount"})
    bids_df["price"] = bids_df["price"].astype(float)
    bids_df["amount"] = bids_df["amount"].astype(float)
    bids_df = bids_df.sort_values("price", ascending=False, ignore_index=True)
    bids_df["total"] = bids_df["amount"].cumsum()
    if bids_df["price"].min() > bids_df["price"][0] * (1 - _top_percent):
        logging.warning(exchange_name + " has fewer values than necessary on the BID side! " +
                        "{:.4f}%".format(bids_df["price"].min() / bids_df["price"].max() * 100))
    bids_df = bids_df.loc[bids_df["price"] > float(bids_df["price"].max()) * (1 - top_percent)]
    bids_df = bids_df[["amount", "total", "price", "type"]]

    # Ask (sell) side
    asks = list(order_book._asks.items())
    asks_df = pd.DataFrame([i[1][0] for i in asks])[["side", "price", "size"]].rename(columns={"side": "type", "size": "amount"})
    asks_df["price"] = asks_df["price"].astype(float)
    asks_df["amount"] = asks_df["amount"].astype(float)
    asks_df = asks_df.sort_values("price", ascending=True)
    asks_df["total"] = asks_df["amount"].cumsum()
    if asks_df["price"].max() < asks_df["price"][0] * (1 + _top_percent):
        logging.warning(exchange_name + " has fewer values than necessary on the ASK side! " +
                        "{:.4f}%".format(bids_df["price"].max() / bids_df["price"].min() * 100))
    asks_df = asks_df.loc[asks_df["price"] < float(asks_df["price"][0]) * (1 + top_percent)]
    asks_df = asks_df[["amount", "total", "price", "type"]]

    # Concate
    long_df = pd.concat([bids_df, asks_df])

    # Save dataframe
    name_long_df = _path + "/" + exchange_name + "/" + exchange_name + "_" + _timestamp + ".csv"
    long_df.to_csv(name_long_df, index=False)

    # Alert
    logging.info(exchange_name + " scraping done!")

if __name__ == "__main__":
    main()