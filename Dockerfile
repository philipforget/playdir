FROM alpine:latest

EXPOSE 8005
WORKDIR /app

RUN apk add --update \
    bash \
    build-base \
    python3-dev && \
    pip3 install -U pip

COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt

ENV PYTHONPATH=/app

COPY ./playdir /app/playdir

CMD ["gunicorn", "-c", "/app/playdir/gunicorn_config.py", "playdir.app:app"]
