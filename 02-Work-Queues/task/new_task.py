import os
import pika
import uuid

username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']

try:

except pika.exceptions as e:
    print(f'exception is: {e}')