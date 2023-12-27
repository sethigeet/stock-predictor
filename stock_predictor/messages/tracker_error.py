from uagents import Model
from pydantic import Field


class TrackerError(Model):
    description: str = Field(
        description="The detailed description of the error that occurred."
    )
