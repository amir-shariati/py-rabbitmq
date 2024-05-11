import json
import os
import pika
from pika.exchange_type import ExchangeType
from typing import TypedDict


class BodyType(TypedDict):
    log_id: str
    time: str
    log_type: str
    log_msg: str


username = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']

log_levels = os.environ['LOG_LEVELS']

exchange_name = 'direct_logs'


def on_message_callback_func(
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
):
    body: BodyType = json.loads(body)
    print(f' [x] Received {body}')
    print(f' [x] Routing_key {method.routing_key}')
    print(f' [x] LogID: {body["log_id"]}, log message {body["log_msg"]} ')


try:
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)
    parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.direct)

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    if not log_levels:
        # sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        print('set env LOG_LEVELS to [info] [warn] [error]')
        sys.exit(1)

    binding_keys = log_levels.split(',')
    print(f'log_levels {log_levels}')
    print(f'binding_keys {binding_keys}')

    # binding_keys = ('info', 'warn', 'error')
    #
    for binding_key in binding_keys:
        print(f'bing  queue:{queue_name} to exchange:{exchange_name} by binding_key:{binding_key}')
        channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=binding_key)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback_func, auto_ack=True)

    channel.start_consuming()

except pika.exceptions as e:
    print(f'exception is: {e}')
