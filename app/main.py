"""
Main API endpoints.
"""

import asyncio
import json
import uuid
from functools import partial

import aio_pika
from fastapi import FastAPI, Request

from app.bridge import async_connect_rabbitmq
from app.logger import logger
from app.utils import timed

api = FastAPI()


@api.on_event("startup")
async def startup() -> None:
    loop = asyncio.get_event_loop()
    conn = await async_connect_rabbitmq(loop)
    api.state.rabbit_conn = conn
