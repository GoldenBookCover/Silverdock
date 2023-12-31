
ARG SILVERDOCK_PYTHON_VERSION
FROM python:${SILVERDOCK_PYTHON_VERSION}-buster

ARG SILVERDOCK_PYTHON_VERSION
LABEL maintainer MonstreCharmant
ENV PYTHONUNBUFFERED 1

# Update all packages
RUN apt update \
    && apt -yqq install \
        vim \
    && pip install \
        python-dotenv \
        click \
        pytest \
        Flask-WTF \
        Flask-SQLAlchemy \
        Flask \
    ;

# Install Google API client
ARG PYTHON_INSTALL_GOOGLEAPI=false
RUN if [ ${PYTHON_INSTALL_GOOGLEAPI} = true ]; then \
        pip install \
            google-api-python-client \
            google-auth-httplib2 \
            google-auth-oauthlib \
    ;fi

# Install Redis
# apt install redis-tools \
ARG PYTHON_INSTALL_REDIS=false
RUN if [ ${PYTHON_INSTALL_REDIS} = true ]; then \
        echo pip install \
            django-redis \
    ;fi

# Install Celery
ARG PYTHON_INSTALL_CELERY=false
RUN if [ ${PYTHON_INSTALL_CELERY} = true ]; then \
        echo pip install \
            celery \
            django-celery-results \
    ;fi

# Install django-treebeard
ARG PYTHON_INSTALL_TREEBEARD=false
RUN if [ ${PYTHON_INSTALL_TREEBEARD} = true ]; then \
        echo pip install \
            django-treebeard \
    ;fi

# Install django-wkhtmltopdf
ARG PYTHON_INSTALL_WKHTMLTOPDF=false
RUN if [ ${PYTHON_INSTALL_WKHTMLTOPDF} = true ]; then \
        echo pip install \
            django-wkhtmltopdf \
    ;fi

# Install production utils
ARG PYTHON_IS_PRODUCTION=false
ENV PYTHON_IS_PRODUCTION ${PYTHON_IS_PRODUCTION}
RUN if [ ${PYTHON_IS_PRODUCTION} = true ]; then \
        pip install \
            uwsgi \
    ;fi

# Install nmap & extension
ARG PYTHON_INSTALL_NMAP=false
RUN if [ ${PYTHON_INSTALL_NMAP} = true ]; then \
        apt -yqq install \
            libpcap-dev \
        && curl -LO https://nmap.org/dist/nmap-7.90.tgz \
        && tar -zxf nmap-7.90.tgz \
        && cd nmap-7.90 \
        && ./configure \
        && make -j 2 \
        && make install \
        && cd .. \
        && rm -rf nmap-7.90 \
        && pip install python-nmap \  
    ;fi

# Install ansible
ARG PYTHON_INSTALL_ANSIBLE=false
RUN if [ ${PYTHON_INSTALL_ANSIBLE} = true ]; then \
        apt -yqq install \
            sshpass \
        && pip install \
            ansible \
            ansible-runner \
    ;fi

# Install elasticsearch
ARG PYTHON_INSTALL_ELASTICSEARCH=false
RUN if [ ${PYTHON_INSTALL_ELASTICSEARCH} = true ]; then \
        echo pip install \
            django-elasticsearch-dsl \
    ;fi

# Install pytest
ARG PYTHON_INSTALL_PYTEST=false
RUN if [ ${PYTHON_INSTALL_PYTEST} = true ]; then \
        pip install \
            pytest \
    ;fi

# Install Channels
ARG PYTHON_INSTALL_CHANNELS=false
RUN if [ ${PYTHON_INSTALL_CHANNELS} = true ]; then \
        echo pip install \
            django-redis \
            channels \
            channels-redis \
    ;fi

ARG PROJECT_NAME=html
ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}
ARG ENABLE_CRONJOB=false
ENV ENABLE_CRONJOB=${ENABLE_CRONJOB}

# Import entrypoint script to control startup
COPY entrypoint.sh /usr/local/bin/entrypoint

# Modify user
RUN apt update \
    && apt install gosu -yqq \
    && chmod 755 /usr/local/bin/entrypoint \
    && groupmod -o -g ${PGID} www-data \
    && usermod -o -u ${PUID} -g www-data www-data \
    && chmod 755 /usr/local/bin/entrypoint \
    && echo "#SilverDock cron job\n#* * * * * www-data python /var/www/main.py schedule &> /tmp/test.log" | tee -a /etc/crontab \
    && mkdir -p /var/www

WORKDIR /var/www
CMD [ "/usr/local/bin/entrypoint" ]

EXPOSE 8000
