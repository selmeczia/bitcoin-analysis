import bitfinex
import os
import bitstamp
import logging
import coinbase
import kraken
import binance
from datetime import datetime as dt

# Global config
parent = os.path.dirname(os.getcwd())
os.chdir(parent)
path = os.getcwd() + "/order_books/"
top_percent = 0.05
timestamp = dt.now().strftime("%Y.%m.%d.%H-%M")
log_path = os.getcwd() + "/log/ticker.log"
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(levelname)s - %(asctime)s : %(message)s")

# Running functions
bitfinex.main(path, top_percent, timestamp, log_path)
bitstamp.main(path, top_percent, timestamp, log_path)
kraken.main(path, top_percent, timestamp, log_path)
binance.main(path, top_percent, timestamp, log_path)
coinbase.main(path, top_percent, timestamp, log_path)

logging.info("All data gathered!")
