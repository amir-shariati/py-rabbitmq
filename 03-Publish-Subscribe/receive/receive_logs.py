import json
import os
import pika
from pika.exchange_type import ExchangeType
from typing import TypedDict


class BodyType(TypedDict):
    log_id: str
    time: str
    log_msg: str


username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']


def on_message_callback_func(
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
):
    # print(f' [x] Received {body.decode()}')
    body: BodyType = json.loads(body)
    print(f' [x] Received {body}')
    # time.sleep(body['delay'])
    # ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f' [x] LogID: {body["log_id"]}, log message {body["log_msg"]} ')




