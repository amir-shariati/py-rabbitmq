import os
import pika
import random
from hashlib import sha256
import uuid

# import socket
# client = docker.from_env()
# network_name = "uv_atp_network"
# atp_container = client.containers.get(socket.gethostname())
# client.networks.get(network_name).connect(container=atp_container.id)


username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']
print(f'username: {username}')
print(f'password: {password}')

try:
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)

    # parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)

    connection = pika.BlockingConnection(parameters=parameters)

    channel = connection.channel()

    channel.queue_declare(queue='hello_queue')

    # rand_str = random.getrandbits(128)
    rand_str = uuid.uuid4()

    channel.basic_publish(exchange='', routing_key='hello_queue', body=f'This is {rand_str}')

    print(f" [x] Sent '{rand_str}'")

except pika.exceptions.ConnectionWrongStateError as e:
    print(f'ConnectionWrongStateError: {e}')
except pika.exceptions.AMQPConnectionError as e:
    print(f'AMQPConnectionError: {e}')
else:
    connection.close()
