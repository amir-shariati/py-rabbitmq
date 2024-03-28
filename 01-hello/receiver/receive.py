import pika
import sys
import os


def on_message_callback_fcn(channel, method, properties, body):
    print(f' [x] Received {body}')

