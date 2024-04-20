import json
import os
import time
import pika
import uuid
from typing import TypedDict



username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']

try:
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)

except pika.exceptions as e:
    print(f'exception is: {e}')
