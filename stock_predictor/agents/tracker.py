import logging
from uagents import Agent, Context

from stock_predictor.messages import TrackerData, TrackerError, TrackerAddTicker
from .api import api

tracker = Agent(name="tracker", seed="tracker-agent-seed")
tracker._logger = logging.Logger("tracker-logger", logging.ERROR)


@tracker.on_interval(period=60 * 60)  # refresh every 60 mins
async def get_prices(ctx: Context) -> None:
    """Gets the prices of the tickers stored in the storage of the agent and
    predicts future prices for that stock."""

    # TODO :)
    pass


@tracker.on_message(TrackerAddTicker)
async def add_ticker(ctx: Context, _sender: str, msg: TrackerAddTicker) -> None:
    """Adds a ticker to the storage of the agent."""

    # TODO :)
    pass
