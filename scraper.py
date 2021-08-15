from selenium import webdriver
import pandas as pd
import numpy as np
import os
from datetime import datetime as dt
import time

# Webdriver config and load
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
for i in range(1, 10):
    table = browser.find_elements_by_class_name("full-book__tables")
    rows = (len(table[0].text.splitlines()) / 6)
    cut = np.array_split(table[0].text.splitlines(), rows)
    df = df.append(pd.DataFrame(cut, columns=cols).drop([0]), ignore_index=True).drop_duplicates()
    browser.execute_script("window.scrollBy(0, 1600);")

# Dataframe adjustments
for col in df.columns:
    df[col] = df[col].str.replace(",", "").astype(float)

# Save dataframe
path = os.getcwd()
name = path + "/order_book_data/" + time + ".csv"
df.to_csv(name, index=False)
