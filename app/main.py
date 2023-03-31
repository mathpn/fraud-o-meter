"""
Main API endpoints.
"""

import asyncio
import json
import uuid
from functools import partial

import aio_pika
from fastapi import FastAPI, Request

from utils.bridge import async_connect_rabbitmq
from utils.logger import logger
from app.utils import timed
from app.models import TransactionDTO, ClassificationDTO

api = FastAPI()


@api.on_event("startup")
async def startup() -> None:
    """Startup event."""
    loop = asyncio.get_event_loop()
    conn = await async_connect_rabbitmq(loop)
    api.state.rabbit_conn = conn


async def result_callback(message: aio_pika.abc.AbstractIncomingMessage, queue, inference_id: str):
    """Callback to put results in the output queue."""
    if message.headers["inference_id"] != inference_id:
        logger.warning(
            "message with different ID on exclusive queue: uuid = %s",
            message.headers["inference_id"],
        )
        return

    logger.debug("received result in callback (uuid %s)", inference_id)
    await queue.put(message)
    await message.ack()


@api.post("/detect_fraud", status_code=200)
@timed
async def detect_fraud(request: Request, body: TransactionDTO) -> ClassificationDTO:
    """Return the probability that the provided transaction is a fraud."""
    state = request.app.state
    inference_id = str(uuid.uuid4())

    out_queue = asyncio.Queue()
    channel = await state.rabbit_conn.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(name="fraudometer_queue", durable=True)
    result = await channel.declare_queue(name=inference_id, exclusive=True, auto_delete=True)
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(body.dict()).encode("utf-8"),
            headers={"inference_id": inference_id},
            reply_to=result.name,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=queue.name,
    )
    logger.info(inference_id)
    logger.info("added request to queue (%s)", inference_id)

    callback = partial(result_callback, queue=out_queue, inference_id=inference_id)
    task = asyncio.create_task(result.consume(callback))
    out = await out_queue.get()
    task.cancel()
    await channel.close()
    logger.debug("received result (uuid %s)", inference_id)

    return ClassificationDTO(fraud_probability=float(out.body.decode("utf-8")))
