import pika
import sys
import os


def on_message_callback_fcn(channel, method, properties, body):
    print(f' [x] Received {body}')


def main():
    username = os.environ['RABBITMQ_DEFAULT_USER']
    password = os.environ['RABBITMQ_DEFAULT_PASS']
    print(f'username: {username}')
    print(f'password: {password}')

    # Set the connection parameters to connect to localhost on port 5672
    credentials = pika.PlainCredentials(username=username, password=password)

    # parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)

    connection = pika.BlockingConnection(parameters=parameters)

    channel = connection.channel()

    channel.queue_declare(queue='hello_queue')

    channel.basic_consume(queue='hello_queue', on_message_callback=on_message_callback_fcn, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()


if __name__ == '__main__':
    print('receiver is running ...')
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            exit(0)
