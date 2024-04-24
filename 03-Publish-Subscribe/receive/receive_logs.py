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


try:
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)
    parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type=ExchangeType.fanout)

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(queue=queue_name, exchange='logs')

    channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback_func, auto_ack=True)


except pika.exceptions as e:
    print(f'exception is: {e}')
