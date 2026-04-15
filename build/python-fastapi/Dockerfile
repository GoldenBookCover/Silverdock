
ARG SILVERDOCK_PYTHON_VERSION=3.13
ARG SILVERDOCK_OS_DEBIAN_PREFER=trixie
FROM python:${SILVERDOCK_PYTHON_VERSION}-${SILVERDOCK_OS_DEBIAN_PREFER}

ARG SILVERDOCK_PYTHON_VERSION
LABEL maintainer GoldenBookCover
ENV PYTHONUNBUFFERED=1

# Update all packages
RUN apt update \
    && apt -yqq install \
        vim \
    && pip install \
        fastapi \
        uvicorn \
        python-dotenv \
        sqlalchemy \
        pytest \
    ;
    
# Install production utils
ARG PYTHON_IS_PRODUCTION=false
ENV PYTHON_IS_PRODUCTION=${PYTHON_IS_PRODUCTION}
RUN if [ ${PYTHON_IS_PRODUCTION} = true ]; then \
        pip install \
            pymysql \
            psycopg2 \
    ;fi
    
# Install Google API client
ARG PYTHON_INSTALL_GOOGLEAPI=false
RUN if [ ${PYTHON_INSTALL_GOOGLEAPI} = true ]; then \
    pip install \
        google-api-python-client \
        google-auth-httplib2 \
        google-auth-oauthlib \
        gspread \
        oauth2client \
    ;fi

# Install Redis
# apt install redis-tools \
ARG PYTHON_INSTALL_REDIS=false
RUN if [ ${PYTHON_INSTALL_REDIS} = true ]; then \
        pip install \
            redis \
    ;fi

# Install Pandas
ARG PYTHON_INSTALL_PANDAS=false
RUN if [ ${PYTHON_INSTALL_PANDAS} = true ]; then \
        pip install \
            pandas \
    ;fi

# Install Celery
ARG PYTHON_INSTALL_CELERY=false
RUN if [ ${PYTHON_INSTALL_CELERY} = true ]; then \
        pip install \
            celery \
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
            fastapi-elasticsearch \
    ;fi

# Install Channels
ARG PYTHON_INSTALL_CHANNELS=false
RUN if [ ${PYTHON_INSTALL_CHANNELS} = true ]; then \
        pip install \
            redis \
            channels \
            channels-redis \
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

ARG PROJECT_NAME=html
ARG PUID=1000
ENV PUID=${PUID}
ARG PGID=1000
ENV PGID=${PGID}
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
    && echo "#Silverdock cron job\n#* * * * * www-data python /var/www/schedule.py &> /tmp/test.log" | tee -a /etc/crontab \
    && mkdir -p /var/www

WORKDIR /var/www
CMD [ "/usr/local/bin/entrypoint" ]

EXPOSE 8000
