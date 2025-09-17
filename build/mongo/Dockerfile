ARG MONGO_VERSION
FROM mongo:${MONGO_VERSION}

VOLUME /data/db /data/configdbs

ARG MONGO_KEYFILE_TEXT
RUN echo "${MONGO_KEYFILE_TEXT}" > /etc/mongo-cluster.key \
    && chown mongodb:mongodb /etc/mongo-cluster.key \
    && chmod 400 /etc/mongo-cluster.key

COPY healthcheck.py /usr/local/bin/healthcheck.py

RUN apt update -yqq \
    && apt install -yqq \
        python3 \
        python3-pymongo \
    && chmod 555 /usr/local/bin/healthcheck.py

# https://docs.docker.com/engine/reference/builder/#healthcheck
HEALTHCHECK --interval=10s --timeout=6s --start-period=30s --retries=3 CMD [ "/usr/local/bin/healthcheck.py" ]

CMD ["mongod"]

EXPOSE 27017
