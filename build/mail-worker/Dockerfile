
ARG SILVERDOCK_PYTHON_VERSION
FROM python:${SILVERDOCK_PYTHON_VERSION}-bullseye

ARG PUBLIC_IP
ARG MAIL_DOMAIN
ARG MAIL_TOP_DOMAIN
ARG FQDN
ARG DB_DATABASE
ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_HOST
ENV DB_DATABASE ${DB_DATABASE}
ENV DB_USERNAME ${DB_USERNAME}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_HOST ${DB_HOST}

COPY . /data

# Essentials
RUN apt -y update \
    && apt -y -q install \
        vim \
        procps \
        ca-certificates \
        curl \
        openssl \
        mariadb-client \
        bsd-mailx \
        rsyslog \
    && pip install -r /data/requirements.txt \
    && cp /data/mail.py /usr/local/bin/mail.py \
    && chmod 755 /usr/local/bin/mail.py

EXPOSE 8000
