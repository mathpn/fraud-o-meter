import logging
import os

import uvicorn


logger = logging.getLogger("uvicorn.access")
logger.setLevel(logging.DEBUG if "DEBUG" in os.environ else logging.INFO)
console_formatter = uvicorn.logging.ColourizedFormatter(
    "{asctime} {levelprefix} : {message}", style="{", use_colors=True
)
logger.handlers[0].setFormatter(console_formatter)
