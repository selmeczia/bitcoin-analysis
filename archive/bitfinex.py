from selenium import webdriver
import pandas as pd
import numpy as np
import os
from datetime import datetime as dt
import time

# Config
top_percent = 0.05

# Webdriver config and load
exchange_name = "bitfinex"
chromedriver = "C:\Program Files (x86)\chromedriver.exe"
link = "https://www.bitfinex.com/order-book/"
browser = webdriver.Chrome(chromedriver)
browser.get(link)
time.sleep(2)

# Create dataframe
time = dt.now().strftime("%Y.%m.%d.%H-%M")
cols = ["amount_buy", "total_buy", "price_buy", "amount_sell", "total_sell", "price_sell"]
df = pd.DataFrame(columns=cols)

# Scraping
for i in range(1, 15):
    table = browser.find_elements_by_class_name("full-book__tables")
    rows = (len(table[0].text.splitlines()) / 6)
    cut = np.array_split(table[0].text.splitlines(), rows)
    df = df.append(pd.DataFrame(cut, columns=cols).drop([0]), ignore_index=True).drop_duplicates()
    browser.execute_script("window.scrollBy(0, 1600);")
browser.close()

# Dataframe adjustments
for col in df.columns:
    df[col] = df[col].str.replace(",", "").astype(float)
middle_price = (df["price_buy"][0] + df["price_sell"][0])/2

long_df_buy = pd.DataFrame(columns=["amount", "total", "price"])
cols = long_df_buy.columns
for col in cols:
    long_df_buy[col] = df[col + "_buy"]
long_df_buy["type"] = "buy"
if long_df_buy["price"].min() > long_df_buy["price"][0] * (1 - top_percent):
    print(exchange_name + " has fewer values than necessary!")
long_df_buy = long_df_buy.loc[long_df_buy["price"] > long_df_buy["price"][0] * (1 - top_percent)]

long_df_sell = pd.DataFrame(columns=["amount", "total", "price"])
cols = long_df_sell.columns
for col in cols:
    long_df_sell[col] = df[col + "_sell"]
long_df_sell["type"] = "sell"
if long_df_sell["price"].max() < long_df_sell["price"][0] * (1 - top_percent):
    print(exchange_name + " has fewer values than necessary!")
long_df_sell = long_df_sell.loc[long_df_sell["price"] < long_df_sell["price"][0] * (1 + top_percent)]
long_df = pd.concat([long_df_buy, long_df_sell])

# Save dataframes
parent = os.path.dirname(os.getcwd())
os.chdir(parent)
path = os.getcwd()
name_df = path + "/order_book_data/" + time + ".csv"
df.to_csv(name_df, index=False)
name_long_df = path + "/order_books/bitfinex/" + exchange_name + "_" + time + ".csv"
long_df.to_csv(name_long_df, index=False)
