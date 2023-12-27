import logging

from uagents import Agent, Context
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stock_predictor.messages import TrackerData, TrackerError

import datetime

api = Agent(name="api", seed="api-agent-seed")
api._logger = logging.Logger("api-logger", logging.ERROR)

app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]
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
    ctx.logger.error(msg= msg.description)


@app.get("/top-tickers")
async def get_top_tickers_data(date: datetime.date = None):
    global OLD_VALUES

    if date is None:
        date = datetime.datetime.now() + datetime.timedelta(days=30)

    future_date = datetime.datetime.now() + datetime.timedelta(days = 30)
    desc_list = []
    desc_num = [i in range(0, len(OLD_VALUES))]

    today = datetime.now()
    for old_value in OLD_VALUES:
        current_price = old_value['Data'][today]
        future_price = old_value['Predicted_Data'][future_date]
        perc_growth = (future_price-current_price)/current_price*100
        desc_list.append(perc_growth)
        old_value['Perc_Growth'] = perc_growth

    n = len(OLD_VALUES)
    for i in range(n):
        for j in range(0, n-i-1):
            if desc_list[j] < desc_list[j+1]:
                desc_list[j], desc_list[j+1] = desc_list[j+1], desc_list[j]
                desc_num[j], desc_num[j+1] = desc_num[j+1], desc_num[j]
    
    list_to_return = []
    for i in range(0, 10):
        list_to_return.append(OLD_VALUES[desc_num[i]])

    return list_to_return


@app.get("/ticker/{ticker}")
async def get_ticker_data(ticker: str):
    for i in OLD_VALUES:
        if i['Ticker'] == ticker:
            return OLD_VALUES[i]

    return None
