import pika
import sys
import os


def on_message_callback_fcn(channel, method, properties, body):
    print(f' [x] Received {body}')


def main():
    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username='admin', password='1234')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)

    # connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost', port=5672))
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello_queue')

    channel.basic_consume(queue='hello_queue', on_message_callback=on_message_callback_fcn, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()

