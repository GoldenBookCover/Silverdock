
ARG SILVERDOCK_PYTHON_VERSION
FROM python:${SILVERDOCK_PYTHON_VERSION}-buster

ARG SILVERDOCK_PYTHON_VERSION
LABEL maintainer MonstreCharmant
ENV PYTHONUNBUFFERED 1

# Update all packages
RUN apt update \
    && apt -yqq install \
        curl \
        vim \
    && pip install \
        django-dotenv \
        django-redis \
        daphne \
        Django

ARG PROJECT_NAME=html
ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

# Modify user
RUN groupmod -o -g ${PGID} www-data \
    && usermod -o -u ${PUID} -g www-data www-data \
    && mkdir -p /usr/share/nginx/${PROJECT_NAME}

USER www-data
WORKDIR /usr/share/nginx/${PROJECT_NAME}
CMD [ "daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application" ]
