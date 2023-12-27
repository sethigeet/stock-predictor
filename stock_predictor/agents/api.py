import logging

from uagents import Agent, Context
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stock_predictor.messages import TrackerData, TrackerError

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


@api.on_message(TrackerData)
async def on_tracker_data_msg(_ctx: Context, _sender: str, msg: TrackerData) -> None:
    # TODO :)

    pass


@api.on_message(TrackerError)
async def on_tracker_error_msg(_ctx: Context, _sender: str, msg: TrackerError) -> None:
    # TODO :)

    pass


@app.get("/top-tickers")
async def get_top_tickers_data():
    # TODO :)

    pass


@app.get("/ticker/{ticker}")
async def get_ticker_data(ticker: str):
    # TODO :)

    pass
