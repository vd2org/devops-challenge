FROM python:3.7-alpine

COPY app/requirements.txt /opt/app/requirements.txt

RUN apk update && \
    apk add --no-cache ca-certificates alpine-sdk yaml-dev linux-headers libffi-dev openssl-dev && \
    pip install --upgrade pip && \
    pip install -r /opt/app/requirements.txt --no-use-pep517 --no-cache-dir -q --compile --no-binary pyyaml && \
    apk del alpine-sdk linux-headers libffi-dev openssl-dev && \
    rm -rf /var/cache/apk/*

COPY app/ /opt/app/

WORKDIR /opt/app

RUN adduser -D -H -s sbin/nologin application

CMD uwsgi --uid application --gid application --master --need-app --chdir /opt/app/ --wsgi-file main.py --callable app --http 0.0.0.0:5000 --processes 5 --threads 2