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


def publish_msg(ch: pika.adapters.blocking_connection.BlockingChannel):
    message = {
        'log_id': uuid.uuid4().hex,
        'time': datetime.datetime.now().time().strftime("%H:%M:%S"),
        'log_msg': f'this is log {random.randint(1,10)}'
    }


    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type=ExchangeType.fanout)

    time.sleep(1)
    publish_msg(ch=channel)
    time.sleep(2)
    publish_msg(ch=channel)
    time.sleep(2)
    publish_msg(ch=channel)


except pika.exceptions as e:
    print(f'exception is: {e}')

else:
    connection.close()
