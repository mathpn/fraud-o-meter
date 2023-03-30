"""
Inference worker that uses RabbitMQ (pika).
"""

import argparse
import json
import threading
from functools import partial
from typing import Callable

from pika import BasicProperties

from utils.bridge import create_rabbitmq_client
from utils.logger import logger
from consumer.inference import create_inference


def callback(
    channel,
    method,
    properties: BasicProperties,
    body: str,
    *,
    worker_id: int,
    inference_fn: Callable,
) -> None:
    transaction_info = json.loads(body)
    result = inference_fn(transaction_info)
    logger.debug(f"inference result (worker {worker_id}): {result}")

    channel.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=BasicProperties(headers=properties.headers),
        body=result,
    )
    channel.basic_ack(delivery_tag=method.delivery_tag)


class ThreadedConsumer(threading.Thread):
    def __init__(
        self,
        worker_id: int,
        rabbitmq_creator: Callable,
        inference_fn: Callable,
    ):
        super().__init__()
        self.worker_id = worker_id
        self.rabbitmq_client, *_ = rabbitmq_creator()
        self.callback = partial(
            callback,
            worker_id=worker_id,
            inference_fn=inference_fn,
        )
        logger.debug(f"consumer worker {worker_id} ready")

    def run(self):
        self.rabbitmq_client.basic_qos(prefetch_count=1)
        self.rabbitmq_client.basic_consume(
            queue="fraudometer_queue", on_message_callback=self.callback
        )
        self.rabbitmq_client.start_consuming()
        logger.info(f"consumer worker {self.worker_id} - starting to consume")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--n-workers", type=int, default=2, help="number of consumer workers.")
    args = parser.parse_args()

    inference = create_inference("/home/models/baseline_lgbm.txt", "/home/models/encoders.json")

    for i in range(args.n_workers):
        logger.info(f"launching consumer worker {i}")
        consumer = ThreadedConsumer(i, create_rabbitmq_client, inference)
        consumer.start()


if __name__ == "__main__":
    main()
