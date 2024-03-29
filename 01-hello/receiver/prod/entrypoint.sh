#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

postgres_ready() {
python << END

import sys
import os
import pika

try:
  credentials = pika.PlainCredentials(username="${RABBITMQ_DEFAULT_USER}", password="${RABBITMQ_DEFAULT_PASS}")
  parameters = pika.ConnectionParameters(host='rabbitmq_server', port=5672, credentials=credentials)
  connection = pika.BlockingConnection(parameters=parameters)

except pika.exceptions.ConnectionWrongStateError:
  sys.exit(-1)
except pika.exceptions.AMQPConnectionError:
  sys.exit(-1)

sys.exit(0)

END
}
until postgres_ready; do
  >&2 echo 'Waiting for RabbitMQ to become available...'
  sleep 1
done
>&2 echo 'RabbitMQ is available'

exec "$@"
