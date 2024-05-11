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


def publish_msg(ch: pika.adapters.blocking_connection.BlockingChannel, log_type):
    message = {
        'log_id': uuid.uuid4().hex,
        'time': datetime.datetime.now().time().strftime("%H:%M:%S"),
        'log_type': log_type,
        'log_msg': f'this is log {random.randint(1,10)}'
    }

    ch.basic_publish(exchange='logs', routing_key='', body=json.dumps(message))

try:
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)
    parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)

    channel = connection.channel()

    exchange = channel.exchange_declare(exchange='direct_logs', exchange_type=ExchangeType.direct)
    print(f'{exchange}')

    log_type = {
        'info': 'info',
        'warn': 'warn',
        'error': 'error'
    }


except pika.exceptions as e:
    print(f'exception is: {e}')

else:
    connection.close()
