from typing import Optional
import logging

from uagents import Agent, Context
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stock_predictor.messages import TrackerData, TrackerError

import datetime

api = Agent(name="api", seed="api-agent-seed")
api._logger = logging.Logger("api-logger", logging.ERROR)

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLD_VALUES = []


@api.on_message(TrackerData)
async def on_tracker_data_msg(_ctx: Context, _sender: str, msg: TrackerData) -> None:
    global OLD_VALUES
    OLD_VALUES = msg.data_items


@api.on_message(TrackerError)
async def on_tracker_error_msg(ctx: Context, _sender: str, msg: TrackerError) -> None:
    ctx.logger.error(msg=msg.description)


@app.get("/top-tickers")
async def get_top_tickers_data(future_date: Optional[str] = None):
    global OLD_VALUES

    if future_date is None:
        future_date = str(
            (datetime.datetime.now() + datetime.timedelta(days=30)).date()
        )

    desc_list = []
    desc_num = [i for i in range(0, len(OLD_VALUES))]

    yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).date())
    for old_value in OLD_VALUES:
        current_price = old_value["Data"][yesterday]
        future_price = old_value["Predicted_Data"][future_date]
        perc_growth = (future_price - current_price) / current_price * 100
        desc_list.append(perc_growth)
        old_value["Pct_Growth"] = int(perc_growth)

    n = len(OLD_VALUES)
    for i in range(n):
        for j in range(0, n - i - 1):
            if desc_list[j] < desc_list[j + 1]:
                desc_list[j], desc_list[j + 1] = desc_list[j + 1], desc_list[j]
                desc_num[j], desc_num[j + 1] = desc_num[j + 1], desc_num[j]

    list_to_return = []
    for i in range(0, 10):
        list_to_return.append(OLD_VALUES[desc_num[i]])

    # print(list_to_return)
    return list_to_return


@app.get("/ticker/{ticker}")
async def get_ticker_data(ticker: str):
    for old_value in OLD_VALUES:
        if old_value["Ticker"] == ticker:
            return old_value

    return None
