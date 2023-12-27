import logging
from uagents import Agent, Context

from stock_predictor import config
from stock_predictor.messages import TrackerData, TrackerError
from .api import api

tracker = Agent(name="tracker", seed="tracker-agent-seed")
tracker._logger = logging.Logger("tracker-logger", logging.ERROR)


@tracker.on_interval(period=config.REFRESH_INTERVAL)
async def get_prices(ctx: Context) -> None:
    """Gets the prices of the tickers stored in the storage of the agent and
    predicts future prices for that stock."""

    # TODO :)
    pass
