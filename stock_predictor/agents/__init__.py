import logging
from uagents import Bureau

from .api import api as api_agent
from .tracker import tracker as tracker_agent

bureau = Bureau()
bureau.add(api_agent)
bureau.add(tracker_agent)
bureau._logger = logging.Logger("bureau-logger", logging.ERROR)
