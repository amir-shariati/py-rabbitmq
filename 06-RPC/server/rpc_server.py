import json
import os
import time
import datetime
import pika
from pika.exchange_type import ExchangeType
from typing import Optional, NotRequired, TypedDict


class BodyType(TypedDict):
    time: str
    correlation_id: str
    request: int
    response: Optional[int]


username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']

queue_name = 'rpc_queue'


def increment(n):
    return n + 1


def publish_msg(ch: pika.adapters.blocking_connection.BlockingChannel, correlation_id, reply_to, delivery_tag, data):
    ch.basic_publish(
        exchange='',
        routing_key=reply_to,
        properties=pika.BasicProperties(correlation_id=correlation_id),
        body=json.dumps(data)
    )
    print(f' [x] Sent {data}')
    ch.basic_ack(delivery_tag=delivery_tag)


