
ARG SILVERDOCK_PYTHON_VERSION
FROM python:${SILVERDOCK_PYTHON_VERSION}-buster

ARG SILVERDOCK_PYTHON_VERSION
LABEL maintainer MonstreCharmant
ENV PYTHONUNBUFFERED 1

# Update all packages
RUN apt update \
    && apt -yqq install \
        vim \
        sudo \
        man-db \
        bash-completion \
    && pip install \
        django-debug-toolbar \
        django-dotenv \
        Pillow \
        django-crispy-forms \
        django-ckeditor \
        django-markdownx \
        Django \
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
        pip install \
            django-redis \
        && apt install -yqq \
            redis-tools \
    ;fi

# Install Celery
ARG PYTHON_INSTALL_CELERY=false
RUN if [ ${PYTHON_INSTALL_CELERY} = true ]; then \
        pip install \
            celery \
            django-celery-results \
    ;fi

# Install django-suit
ARG PYTHON_INSTALL_DJANGO_SUIT=false
RUN if [ ${PYTHON_INSTALL_DJANGO_SUIT} = true ]; then \
        pip install \
            https://github.com/darklow/django-suit/tarball/v2 \
    ;fi

# Install django-treebeard
ARG PYTHON_INSTALL_TREEBEARD=false
RUN if [ ${PYTHON_INSTALL_TREEBEARD} = true ]; then \
        pip install \
            django-treebeard \
    ;fi

# Install django-wkhtmltopdf
ARG PYTHON_INSTALL_WKHTMLTOPDF=false
RUN if [ ${PYTHON_INSTALL_WKHTMLTOPDF} = true ]; then \
        pip install \
            django-wkhtmltopdf \
    ;fi

# Install production utils
ARG PYTHON_IS_PRODUCTION=false
ENV PYTHON_IS_PRODUCTION ${PYTHON_IS_PRODUCTION}
RUN if [ ${PYTHON_IS_PRODUCTION} = true ]; then \
        pip install \
            uwsgi \
            psycopg2 \
            mysqlclient \
    ;fi

# Install nmap & extension
ARG PYTHON_INSTALL_NMAP=false
RUN if [ ${PYTHON_INSTALL_NMAP} = true ]; then \
        apt -yqq install \
            libpcap-dev \
        && curl -LO https://nmap.org/dist/nmap-7.80.tgz \
        && tar -zxf nmap-7.80.tgz \
        && cd nmap-7.80 \
        && ./configure \
        && make -j 2 \
        && make install \
        && cd .. \
        && rm -rf nmap-7.80 \
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
        pip install \
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
        pip install \
            django-redis \
            channels \
            channels-redis \
    ;fi

ARG PROJECT_NAME=html
ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

# Import entrypoint script to control startup
COPY entrypoint.sh /usr/local/bin/entrypoint

# Different from php-fpm from here
RUN apt install -yqq \
        mariadb-client \
        dos2unix \
        openssh-server

# Add sshd config
COPY sshd_config /etc/ssh/sshd_config

# Modify user and add ssh public key
RUN groupadd -o -g ${PGID} silverdock \
    && useradd -o -u ${PUID} -g silverdock -s /bin/bash -m -c "SilverDock user" silverdock \
    && install -d -m 700 -o silverdock -g silverdock /home/silverdock/.ssh

# USER silverdock
COPY silverdock.pem.pub /home/silverdock/.ssh/authorized_keys

RUN chmod 600 /home/silverdock/.ssh/authorized_keys \
    && chown silverdock:silverdock /home/silverdock/.ssh/authorized_keys \
    && chmod 755 /usr/local/bin/entrypoint \
    && mkdir -p /usr/share/nginx/${PROJECT_NAME}

WORKDIR /usr/share/nginx/${PROJECT_NAME}
CMD [ "/usr/local/bin/entrypoint" ]
EXPOSE 22
