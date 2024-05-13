import datetime
import time
import json
import uuid
import random
import os
import pika
from pika.exchange_type import ExchangeType

username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']

log_topic = os.environ['LOG_TOPIC']

exchange_name = 'topic_logs'


def publish_msg(ch: pika.adapters.blocking_connection.BlockingChannel, log_topic, log_msg):
    message = {
        'log_id': uuid.uuid4().hex,
        'time': datetime.datetime.now().time().strftime("%H:%M:%S"),
        'log_topic': log_topic,
        'log_msg': log_msg
    }

    ch.basic_publish(exchange=exchange_name, routing_key=log_topic, body=json.dumps(message))


