from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt
import time

cols = ["amount_buy", "total_buy", "price_buy", "amount_sell", "total_sell", "price_sell"]
df = pd.DataFrame(columns=cols)

chromedriver = "C:\Program Files (x86)\chromedriver.exe"
link = "https://www.bitfinex.com/order-book/"
browser = webdriver.Chrome(chromedriver)
browser.get(link)

time.sleep(2)

time = dt.now().strftime("%H:%M:%S")
for round in range(1, 10):
    table = browser.find_elements_by_class_name("full-book__tables")
    rows = (len(table[0].text.splitlines()) / 6)
    cut = np.array_split(table[0].text.splitlines(), rows)
    df = df.append(pd.DataFrame(cut, columns=cols).drop([0]), ignore_index=True).drop_duplicates()
    browser.execute_script("window.scrollBy(0, 1600);")

for col in df.columns:
    df[col] = df[col].astype(float)
fig, ax = plt.subplots()
ax.set_title('BTC/USD order book on Bitfinex exchange at ' + time)
sns.ecdfplot(x="price_buy", weights="amount_buy", stat="count", complementary=True, data=df, ax=ax, color='g')



