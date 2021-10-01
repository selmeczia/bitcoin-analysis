import matplotlib.pyplot as plt
import pandas as pd
import datetime
import pandas_datareader.data as web


#live data
# data_url = "http://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"
# data = request.get(data_url)


bitflyerJPY = pd.read_csv("data/short/bitflyerJYP.csv")
bitstampUSD = pd.read_csv("data/short/bitstampUSD.csv")
krakenEUR = pd.read_csv("data/short/krakenEUR.csv")
krakenUSD = pd.read_csv("data/short/krakenUSD.csv")

exchanges = [bitflyerJPY, bitstampUSD, krakenEUR, krakenUSD]


plt.plot(bitflyerJPY["amount"])
plt.plot(bitstampUSD["amount"])
plt.plot(krakenEUR["amount"])
plt.plot(krakenUSD["amount"])

for df in exchanges:
    vol_mean = df["amount"].mean()
    vol_std = df["amount"].std()
    vol_min = df["amount"].min()
    vol_max = df["amount"].max()

    price_mean = df["price"].mean()
    price_std = df["price"].std()
    price_min = df["price"].min()
    price_max = df["price"].max()

    print(price_mean, price_std, price_min, price_max)


start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2021, 5, 12)

SP500 = web.DataReader(['sp500'], 'fred', start, end)


fig, ax1 = plt.subplots(figsize=(15, 10))
ax2 = ax1.twinx()

a = bitstampUSD[["date", "amount"]]
b = bitstampUSD[["date", "price"]]
a.plot(kind = "bar", ax = ax1)
b.plot(kind = "line", ax = ax2)

ax1.yaxis.tick_right()
ax2.yaxis.tick_left()

plt.show()


