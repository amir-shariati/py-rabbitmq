import datetime
import json
import os
import pika
import uuid
import random

username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']

try:
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)

    parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)

    connection = pika.BlockingConnection(parameters=parameters)

    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    message = {
        'task_id': uuid.uuid4().hex,
        'time': datetime.datetime.now().time().strftime("%H:%M:%S"),
        'delay': random.randint(2, 5)
    }

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
    )

    print(f" [x] Sent {message}")

except pika.exceptions as e:
    print(f'exception is: {e}')

else:
    connection.close()
