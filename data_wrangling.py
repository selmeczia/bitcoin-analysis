import matplotlib.pyplot as plt
import pandas as pd
import datetime

#live data
# data_url = "http://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"
# data = request.get(data_url)




bitflyerJPY = "data/bitflyerJPY.csv.gz"
bitstampUSD = "data/bitstampUSD.csv.gz"
krakenEUR = "data/krakenEUR.csv.gz"
krakenUSD = "data/krakenUSD.csv.gz"



bitflyerJPY_df = pd.read_csv(bitflyerJPY, compression='gzip', error_bad_lines=False, names = ["timestamp", "price", "amount"])
bitstampUSD_df = pd.read_csv(bitstampUSD, compression='gzip', error_bad_lines=False, names = ["timestamp", "price", "amount"])
krakenEUR_df = pd.read_csv(krakenEUR, compression='gzip', error_bad_lines=False, names = ["timestamp", "price", "amount"])
krakenUSD_df = pd.read_csv(krakenUSD, compression='gzip', error_bad_lines=False, names = ["timestamp", "price", "amount"])

exchanges = [bitflyerJPY_df, bitstampUSD_df, krakenEUR_df, krakenUSD_df]




for df in exchanges:

    df["date"] = pd.to_datetime(df['timestamp'], unit="s").dt.date
    df = df.groupby(['date']).agg({'price': "mean", 'amount': "sum"})
    df.index.name = 'date'
    df.reset_index(inplace=True)
    df = df.loc[df["date"] > datetime.date(2020, 1, 1)]
    output_path = "data/short/" + str(i) + ".csv"
    df.to_csv(output_path ,index = False)



