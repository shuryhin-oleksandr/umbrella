FROM python:3.8
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -yyq netcat

# install psycopg2 dependencies


# Allows docker to cache installed dependencies between builds
RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8000

# Run the production server

CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - umbrella.wsgi:application


# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
RUN chmod +x entrypoint.sh