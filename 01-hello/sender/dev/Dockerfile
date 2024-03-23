# pull official base image
FROM python:3.12.2-slim

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements/common.txt /common.txt
COPY ./requirements/dev.txt /requirements.txt
RUN pip install -r /requirements.txt

#COPY ./compose/develop/python/entrypoint /entrypoint
COPY ./sender/dev/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

#COPY ./compose/develop/python/start /start
COPY ./sender/dev/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
#
## start command
#CMD [ "python", "send.py" ]