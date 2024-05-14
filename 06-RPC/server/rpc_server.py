import json
import os
import time
import datetime
import pika
from pika.exchange_type import ExchangeType
from typing import Optional, NotRequired, TypedDict


class BodyType(TypedDict):
    time: str
    correlation_id: str
    request: int
    response: Optional[int]


