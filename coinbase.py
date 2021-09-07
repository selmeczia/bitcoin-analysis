import cbpro, time
import pandas as pd

order_book = cbpro.OrderBook(product_id='BTC-USD')
order_book.start()
time.sleep(5)

asks = list(order_book._asks.items())
ask_df = pd.DataFrame([i[1][0] for i in asks])[["side", "price", "size"]]
bids = list(order_book._bids.items())
bids_df = pd.DataFrame([i[1][0] for i in bids])[["side", "price", "size"]]



ask_df
bids_df