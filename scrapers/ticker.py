import bitfinex
import bitstamp
import coinbase
import kraken

scrapers = ["bitfinex", "bitstamp", "coinbase", "kraken"]


bitfinex.main()
bitstamp.main()
kraken.main()
coinbase.main()

print("All data gathered!")
