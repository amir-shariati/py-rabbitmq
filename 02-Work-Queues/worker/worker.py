import json
import os
import time
import pika
import uuid
from typing import TypedDict


class BodyType(TypedDict):
    task_id: str
    time: str
    delay: int

username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']

def on_message_callback_func(
        channel: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
):
    # print(f' [x] Received {body.decode()}')
    body: BodyType = json.loads(body)
    print(f' [x] Received {body}')
    time.sleep(body['delay'])
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print(f' [x] Task: {body["task_id"]}, Done after {body["delay"]}\'s ')

try:
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)

except pika.exceptions as e:
    print(f'exception is: {e}')
