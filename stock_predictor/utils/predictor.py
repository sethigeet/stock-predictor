import datetime

import pandas as pd
import numpy as np
from sklearn import preprocessing, svm
import yfinance as yf

from stock_predictor import config


def get_data(ticker: str) -> pd.DataFrame:
    df = yf.Ticker(ticker).history(
        period=config.STOCKS_DATA_PERIOD, interval=config.STOCKS_DATA_INTERVAL
    )
    return df


def split_data(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    df = df.copy()
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df["HL_PCT"] = (df["High"] - df["Low"]) / df["Close"] * 100.0
    df["PCT_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100.0

    df = df[["Close", "HL_PCT", "PCT_change", "Volume"]]
    predict_col = "Close"
    df.fillna(value=-99999, inplace=True)
    predict_out = config.STOCKS_NUM_PREDICTIONS

    df["label"] = df[predict_col].shift(-predict_out)

    X = np.array(df.drop(["label"], axis=1))
    X = preprocessing.scale(X)
    X_predict = X[-predict_out:]  # type: ignore
    X = X[:-predict_out]  # type: ignore

    df.dropna(inplace=True)

    y = np.array(df["label"])

    return (X, X_predict, y)


def train_model(X: np.ndarray, y: np.ndarray) -> svm.SVR:
    clf = svm.SVR(kernel="linear")
    clf.fit(X, y)
    return clf


def get_predictions(clf: svm.SVR, X_lately: np.ndarray) -> np.ndarray:
    predictions = clf.predict(X_lately)
    return predictions


def get_predicted_dates(
    df: pd.DataFrame, num_predictions: int
) -> list[datetime.datetime]:
    last_date = df.iloc[-1].name
    last_unix = last_date.timestamp()  # type: ignore
    one_day = 86400
    next_unix = last_unix + one_day

    predicted_dates = []

    for _ in range(num_predictions):
        next_date = datetime.datetime.fromtimestamp(next_unix).astimezone()
        predicted_dates.append(next_date)
        next_unix += 86400

    return predicted_dates


def predict(
    ticker: str,
) -> tuple[list[datetime.datetime], np.ndarray, list[datetime.datetime], np.ndarray]:
    data = get_data(ticker)
    X, X_lately, y = split_data(data)
    clf = train_model(X, y)
    predictions = get_predictions(clf, X_lately)
    predicted_dates = get_predicted_dates(data, config.STOCKS_NUM_PREDICTIONS)
    return (data.index.values, data["Close"].values, predicted_dates, predictions)  # type: ignore
