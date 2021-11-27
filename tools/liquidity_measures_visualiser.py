from os import listdir
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import os
from pathlib import Path
from datetime import datetime, timedelta

markets = ["binance", "bitfinex", "bitstamp", "coinbase", "kraken"]
main_path = "C:/Users/Adam/Documents/bitcoin-orderbook_2/order_books/market_data"
path = Path(os.getcwd())
plot_path = path.parent.absolute() / "plots_2"

markets_data_dict = {}
for market in markets:
    file = f'{main_path}/{market}.csv'
    data = pd.read_csv(file)
    markets_data_dict[market] = data

# Liquidity measures

# Number of hours interval
start_date = datetime.strptime(markets_data_dict["binance"]["opentime"][0], '%Y-%m-%d %H:%M:%S.%f') - timedelta(hours=1)
interval_len = 24

aggr_df = {}
for market in markets:
    data = markets_data_dict[market]
    full_len = len(data)
    intervals = int(full_len/interval_len)
    data["interval"] = [i+1 for i in range(intervals) for _ in range(interval_len)]
    aggr_df[market] = pd.DataFrame()
    date = start_date

    for interval in range(1, intervals + 1):

        # Generic
        int_df = data.loc[data["interval"] == interval]
        ret_series = (int_df["close"] / int_df["open"]) - 1
        dol_vol_series = int_df["volume"] * int_df["close"] / 1000000
        date = date + timedelta(hours=interval_len)

        # Bigger number -> more liquid

        # Number of transactions
        tx = int_df["trades"].mean()


        # Dollar volume
        dol_vol = dol_vol_series.mean()


        # Amihud
        amihud = (ret_series.abs()/dol_vol_series).mean()


        # Roll serial covariance estimator
        #TODO: fix
        roll = 2 * math.sqrt(-min(0, np.cov(ret_series, ret_series.shift(1))[0][0]))


        # Kyle and Obizhaeva estimator
        #TODO: fix
        kyle = ((ret_series - ret_series.mean())**2).var() / dol_vol


        # Corwin and Schultz estimator
        gamma = (np.log(pd.concat((int_df["high"], int_df["high"].shift(1)), axis=1).max(axis=1)[1:] /
                       pd.concat((int_df["low"], int_df["low"].shift(1)), axis=1).min(axis=1)[1:]))**2
        beta = (np.log(int_df["high"] / int_df["low"])) ** 2 +\
               np.log(int_df["high"].shift(1) / int_df["low"].shift(1)) ** 2
        alpha = (np.sqrt(2*beta) - np.sqrt(beta)) / (3-2*np.sqrt(2)) - np.sqrt(gamma / (3-2*np.sqrt(2)))
        cs = (2*(np.exp(alpha)-1) / (1+np.exp(alpha))).clip(lower=0).mean()


        # Abdi and Ranaldo
        p_hat = (np.log(int_df["high"]) + np.log(int_df["low"])) / 2
        p_hat_shift = ((pd.concat([np.log(int_df["high"]), np.log(int_df["high"]).shift(1)], axis=1)).max(axis=1)[1:] +
                       (pd.concat([np.log(int_df["low"]), np.log(int_df["low"]).shift(1)], axis=1)).min(axis=1)[1:]) / 2
        ar = np.sqrt((4 *
                      (np.log(int_df["close"]) - p_hat) *
                      (np.log(int_df["close"])-p_hat_shift)[1:]).clip(lower=0)).mean()


        # Relativ change in volume
        avv = int_df["volume"].mean()
        rdcv = (int_df["volume"]-int_df["volume"].shift(1)).abs() / avv
        rcv = rdcv.mean()


        # Coefficient of elastic trading
        cet = (np.log(int_df["volume"] / int_df["volume"].shift(1)) /
               np.log(int_df["close"] / int_df["close"].shift(1))).sum()
        cet_abs = abs(cet)


        # Index of Martin
        mli = (((int_df["close"] - int_df["close"].shift(1))**2) / int_df["volume"]).sum()


        # Append estimators
        row = {"date": date,
               "interval": interval,
               "tx": tx,
               "dol_vol": dol_vol,
               "amihud": amihud,
               # "roll": roll,
               # "kyle": kyle,
               "cs": cs,
               "ar": ar,
               "cet": cet,
               "cet_abs": cet_abs,
               "mli": mli,
               "rcv": rcv}
        aggr_df[market] = aggr_df[market].append(row, ignore_index=True)


aggr_df

measures = {
    "tx": "Number of transactions",
    "dol_vol": "Dollar volume",
    "amihud": "Amihud illiquidity measure",
    # "roll": roll,
    # "kyle": kyle,
    "cs": "Corwin and Schultz estimator",
    "ar": "Abdi and Ranaldo estimator",
    "cet": "Coefficient of Elasticity of Trading",
    "cet_abs": "Absolute of Coefficient of Elasticity of Trading",
    "mli": "The Index of Martin",
    "rcv": "Relative Change in Volume"
}


# Ordered liquidity measures
result_df = pd.concat(aggr_df).copy()
result_df.index.name = 'newhead'
result_df.reset_index(inplace=True)
result_df = result_df.rename(columns={"level_0": "market"})
for measure in measures:
    if measure in ["cs", "ar", "rcv"]: # The smaller the more liquid
        result_df.loc[result_df.sort_values(["interval", measure], ascending=[True, True]).index, f'{measure}_order'] = list(range(1, 6)) * intervals
    else:
        result_df.loc[result_df.sort_values(["interval", measure], ascending=[True, False]).index, f'{measure}_order'] = list(range(1, 6)) * intervals
result_df
cet

# Liquidity measure plot (TX, $Vol)
# plt.rcParams["figure.figsize"] = (15, 10)
# fig, axs = plt.subplots(2, 1)
#
# for market in markets:
#     axs[0].plot(aggr_df[market]["date"],
#                       aggr_df[market]["tx"],
#                       label=market.capitalize())
#     axs[0].set_title("Number of transactions (TX)")
#     axs[1].plot(aggr_df[market]["date"],
#                       aggr_df[market]["dol_vol"],
#                       label=market.capitalize())
#     axs[1].set_title("Dollar volume ($Vol)")
# axs[0].legend()
# plt.show()
# plt.savefig(plot_path / "liq_tx-vol.png", dpi=300)

# Liquidity measure plot (Amihud, MLI)
# plt.rcParams["figure.figsize"] = (15, 10)
# fig, axs = plt.subplots(2, 1)
#
# for market in markets:
#     axs[0].plot(aggr_df[market]["date"],
#                       aggr_df[market]["amihud"],
#                       label=market.capitalize())
#     axs[0].set_title("Amihud illiquidity measure")
#     axs[1].plot(aggr_df[market]["date"],
#                       aggr_df[market]["mli"],
#                       label=market.capitalize())
#     axs[1].set_title("The Index of Martin")
# axs[0].legend()
# plt.show()
# plt.savefig(plot_path / "liq_amihud-mli.png", dpi=300)

# Liquidity measure plot (CS, AR)
# plt.rcParams["figure.figsize"] = (15, 10)
# fig, axs = plt.subplots(2, 1)
#
# for market in markets:
#
#     axs[0].plot(aggr_df[market]["date"],
#                       aggr_df[market]["cs"],
#                       label=market.capitalize())
#     axs[0].set_title("Corwin and Schultz estimator")
#
#     if market != "kraken":
#         axs[1].plot(aggr_df[market]["date"],
#                           aggr_df[market]["ar"],
#                           label=market.capitalize())
#         axs[1].set_title("Abdi and Ranaldo estimator")
# axs[0].legend(loc="upper right")
# plt.show()
# plt.savefig(plot_path / "liq_cs-ar.png", dpi=300)


# Liquidity measure plot (CET, RCV)
plt.rcParams["figure.figsize"] = (15, 10)
fig, axs = plt.subplots(2, 1)
#
for market in markets:

    if market != "kraken":
        axs[0].plot(aggr_df[market]["date"],
                          aggr_df[market]["cet"],
                          label=market.capitalize())
        axs[0].set_title("Coefficient of Elasticity of Trading")

    axs[1].plot(aggr_df[market]["date"],
                      aggr_df[market]["rcv"],
                      label=market.capitalize())
    axs[1].set_title("Relative Change in Volume")
axs[0].legend(loc="upper right")
# plt.show()
plt.savefig(plot_path / "liq_cet-rcv.png", dpi=300)
