import datetime

from uagents import Model
from pydantic import Field


class TrackerData(Model):
    # data_item => {"Ticker": str, "Name": str, "Data": dict[date, price], "Predicted_Data": dict[date, price]}
    data_items : list