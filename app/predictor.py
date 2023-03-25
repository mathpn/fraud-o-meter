import json
import pandas as pd
import pickle

from pathlib import Path
from kafka import KafkaConsumer, KafkaProducer


KAFKA_HOST = "localhost:9092"
TOPICS = ['app_messages']


producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)


def predict(message) -> int:
    return 1


def publish_prediction(pred, request_id):
    producer.send(
        "app_messages",
        json.dumps({"request_id": request_id, "prediction": float(pred)}).encode("utf-8"),
    )
    producer.flush()


def start(*args, **kwargs):
    for msg in consumer:
        message = json.loads(msg.value)
        if "data" not in message:
            continue  # XXX
        request_id = message["request_id"]
        pred = predict(message["data"])
        publish_prediction(pred, request_id)


if __name__ == "__main__":
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_HOST)
    consumer.subscribe(TOPICS)
    start()
