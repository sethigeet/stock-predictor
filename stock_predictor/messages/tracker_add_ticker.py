from uagents import Model
from pydantic import Field


class TrackerAddTicker(Model):
    ticker: str = Field(description="The ticker of the stock that should be tracked.")
    name: str = Field(description="The name of the stock that should be tracked.")
