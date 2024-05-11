import json
import os
import pika
from pika.exchange_type import ExchangeType
from typing import TypedDict


class BodyType(TypedDict):
    log_id: str
    time: str
    log_type: str
    log_msg: str


username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']

log_levels = os.environ['LOG_LEVELS']

exchange_name = 'direct_logs'


