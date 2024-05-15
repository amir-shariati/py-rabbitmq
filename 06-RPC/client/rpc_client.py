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


        self.response: BodyType | None = None

