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

exchange_name = 'direct_logs'


def publish_msg(ch: pika.adapters.blocking_connection.BlockingChannel, log_type, log_msg):
    message = {
        'log_id': uuid.uuid4().hex,
        'time': datetime.datetime.now().time().strftime("%H:%M:%S"),
        'log_type': log_type,
        'log_msg': log_msg
    }

    ch.basic_publish(exchange=exchange_name, routing_key=log_type, body=json.dumps(message))
    # print(f'publish ')

try:
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)
    parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.direct)

    log_type = {
        'info': f'this is log info {random.randint(1,10)}',
        'warn': f'this is log warn{random.randint(1,10)}',
        'error': f'this is log error{random.randint(1,10)}'
    }

    for k, v in log_type.items():
        publish_msg(ch=channel, log_type=k, log_msg=v)


except pika.exceptions as e:
    print(f'exception is: {e}')

else:
    connection.close()
