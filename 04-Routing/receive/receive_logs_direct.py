import json
import os
import pika
from pika.exchange_type import ExchangeType
from typing import TypedDict



username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']
