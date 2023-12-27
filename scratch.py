import pandas as pd
import yfinance as yf
import math
import numpy as np
from sklearn import preprocessing, model_selection, svm
import datetime
import matplotlib.pyplot as plt

tickers = ["HINDALCO", "SUVENPHAR", "QUESS", "LICHSGFIN", "ADANIENT"]
tickers = [ticker + ".NS" for ticker in tickers]

# yf.Ticker(tickers[0]).history(period="1y").to_csv("data.csv")
# df = yf.Ticker(tickers[0]).history()
df = pd.read_csv("data.csv", parse_dates=True, index_col=0)


df = df[["Open", "High", "Low", "Close", "Volume"]]
df["HL_PCT"] = (df["High"] - df["Low"]) / df["Close"] * 100.0
df["PCT_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100.0

df = df[["Close", "HL_PCT", "PCT_change", "Volume"]]
forecast_col = "Close"
df.fillna(value=-99999, inplace=True)
forecast_out = int(math.ceil(0.1 * len(df)))  # 10% of the data

df["label"] = df[forecast_col].shift(-forecast_out)

X = np.array(df.drop(["label"], axis=1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]  # type: ignore
X = X[:-forecast_out]  # type: ignore

df.dropna(inplace=True)

y = np.array(df["label"])

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)
clf = svm.SVR(kernel="linear")
clf.fit(X_train, y_train)

print(clf.score(X_test, y_test))

forecast_set = clf.predict(X_lately)
df["Forecast"] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()  # type: ignore
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix).astimezone()
    next_unix += 86400
    df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]  # type: ignore

df["Close"].plot()
df["Forecast"].plot()
plt.legend(loc=4)
plt.xlabel("Date")
plt.ylabel("Price")
plt.savefig("plot.png")
