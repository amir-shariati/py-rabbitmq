from __future__ import annotations
import datetime
import json
import os
import time
import uuid
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


class Client(object):
    def __init__(self):
        credentials = pika.PlainCredentials(username=username, password=password)
        parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters=parameters)

        self.channel: pika.adapters.blocking_connection.BlockingChannel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

        self.response: BodyType | None = None
        self.corr_id = None

    def on_response(
            self,
            ch: pika.adapters.blocking_connection.BlockingChannel,
            method: pika.spec.Basic.Deliver,
            props: pika.spec.BasicProperties,
            body: bytes
    ):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def publish_msg(self, data):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(correlation_id=self.corr_id, reply_to=self.callback_queue),
            body=data
        )

    def call(self, num: int) -> BodyType | None:
        self.response = None
        self.corr_id = str(uuid.uuid4())
        message = {
            'time': datetime.datetime.now().time().strftime("%H:%M:%S"),
            'correlation_id': self.corr_id,
            'request': num,
        }
        self.publish_msg(data=json.dumps(message))




