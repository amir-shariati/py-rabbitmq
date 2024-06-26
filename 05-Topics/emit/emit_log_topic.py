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


try:
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)
    parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.topic)

    log_topics = {
        'info.*.*': f'this is log for topic: info.*.* -> {random.randint(1,10)}',
        '*.warn.*': f'this is log for topic: *.warn.* -> {random.randint(1,10)}',
        '#.error': f'this is log for topic: #.error -> {random.randint(1,10)}',
        '*.*.error': f'this is log for topic: *.*.error -> {random.randint(1,10)}',
    }

    for k, v in log_topics.items():
        publish_msg(ch=channel, log_topic=k, log_msg=v)


except pika.exceptions as e:
    print(f'exception is: {e}')

else:
    connection.close()
