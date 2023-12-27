import logging
import json
import math
from uagents import Agent, Context
import pandas as pd
import numpy as np

from stock_predictor import config
from stock_predictor.messages import TrackerData, TrackerError
from stock_predictor.utils import predict
from .api import api

tracker = Agent(name="tracker", seed="tracker-agent-seed")
tracker._logger = logging.Logger("tracker-logger", logging.ERROR)


@tracker.on_interval(period=60 * 60)  # refresh every 60 mins
async def get_prices(ctx: Context) -> None:
    """Gets the prices of the tickers stored in the storage of the agent and
    predicts future prices for that stock."""

    data_vals = []
    try:
        with open("top-tickers.json") as f:
            data = json.load(f)
            for i in list(data.keys())[: config.NUM_STOCKS_TO_MONITOR]:
                res = predict(i + ".bo")
                non_pred = {}
                pred = {}
                for a, b in zip(res[0], res[1]):
                    a = pd.to_datetime(a).date()
                    try:
                        int(b)
                    except:
                        continue
                    non_pred[str(a)] = round(b, 2)
                for a, b in zip(res[2], res[3]):
                    a = pd.to_datetime(a).date()
                    try:
                        int(b)
                    except:
                        continue
                    pred[str(a)] = round(b, 2)
                data_vals.append(
                    {
                        "Ticker": i,
                        "Name": data[i],
                        "Data": non_pred,
                        "Predicted_Data": pred,
                    }
                )
        print("Acquired data for predefined tickers!")
        await ctx.send(api.address, message=TrackerData(data_items=data_vals))
    except Exception as e:
        await ctx.send(api.address, message=TrackerError(description=str(e)))
