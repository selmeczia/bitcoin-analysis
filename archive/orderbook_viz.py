import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots()
ax.set_title('BTC/USD order book on Bitfinex exchange at ' + time)
sns.ecdfplot(x="price_buy", weights="amount_buy", stat="count", complementary=True, data=df, ax=ax, color='g')

ax.set_xlabel("Price")
ax.set_ylabel("Amount")

plt.show()