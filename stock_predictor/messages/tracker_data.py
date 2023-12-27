import datetime

from uagents import Model
from pydantic import Field


class TrackerData(Model):
    ticker: str = Field(description="The ticker of the stock that was tracked.")
    dates: list[datetime.datetime] = Field(description="The dates of the close prices")
    close_prices: list[float] = Field(description="The close prices of the stock")
    dates_predicted: list[datetime.datetime] = Field(
        description="The dates of the predicted close prices"
    )
    close_prices_predicted: list[float] = Field(
        description="The predicted close prices of the stock"
    )
