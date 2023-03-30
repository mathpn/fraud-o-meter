import logging
import os

import uvicorn


logger = logging.getLogger()
logger.setLevel(logging.DEBUG if "DEBUG" in os.environ else logging.INFO)
logger.f
    "{asctime} {levelprefix} : {message}", style="{", use_colors=True
)
logger.handlers[0].setFormatter(console_formatter)
