# pull official base image
FROM python:3.12.2-slim

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

#RUN apt-get update \
#  # dependencies for building Python packages
#  && apt-get install -y build-essential \
#  # psycopg2 dependencies
#  && apt-get install -y libpq-dev \
#  # Translations dependencies
#  && apt-get install -y gettext \
#  # cleaning up unused files
#  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
#  && rm -rf /var/lib/apt/lists/*

#WORKDIR /app
## Requirements are installed here to ensure they will be cached.
#COPY ./requirements/common.txt common.txt
#COPY ./requirements/dev.txt requirements.txt
#RUN pip install -r requirements.txt
#
#COPY ./sender/dev/entrypoint entrypoint
#RUN sed -i 's/\r$//g' entrypoint
#RUN chmod +x entrypoint
#
##COPY ./compose/develop/python/start /start
#COPY ./sender/dev/start start
#RUN sed -i 's/\r$//g' start
#RUN chmod +x start

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