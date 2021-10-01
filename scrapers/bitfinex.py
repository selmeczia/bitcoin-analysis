import pandas as pd
import requests
import logging

def main(path, top_percent, timestamp, log_path):
    # Config
    exchange_name = "bitfinex"
    _timestamp = timestamp
    _top_percent = top_percent
    _path = path
    logging.basicConfig(filename=log_path, level=logging.INFO, format="%(levelname)s - %(asctime)s : %(message)s")

    # Get response
    response = requests.get("https://api.bitfinex.com/v1/book/BTCUSD?limit_asks=10000&limit_bids=10000").json()

    # Bid (buy) side
    bids_df = pd.DataFrame(response["bids"], columns=["price", "amount"])
    bids_df["price"] = bids_df["price"].astype(float)
    bids_df["amount"] = bids_df["amount"].astype(float)
    bids_df["total"] = bids_df["amount"].cumsum()
    if bids_df["price"].min() > bids_df["price"][0] * (1 - _top_percent):
        logging.warning(exchange_name + " has fewer values than necessary on the BID side! " +
                        "{:.4f}%".format(bids_df["price"].min() / bids_df["price"].max() * 100))
    bids_df = bids_df.loc[bids_df["price"] > bids_df["price"][0] * (1 - _top_percent)]
    bids_df["type"] = "buy"
    bids_df = bids_df[["amount", "total", "price", "type"]]

    # Ask (sell) side
    asks_df = pd.DataFrame(response["asks"], columns=["price", "amount"])
    asks_df["price"] = asks_df["price"].astype(float)
    asks_df["amount"] = asks_df["amount"].astype(float)
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
