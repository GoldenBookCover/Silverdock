ARG MONGO_VERSION
FROM mongo:${MONGO_VERSION}

VOLUME /data/db /data/configdb

RUN apt update -yqq \
    && apt install -yqq \
        python3 \
        python3-pymongo

COPY --chmod=755 healthcheck.py /usr/local/bin/healthcheck.py
COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint
COPY --chmod=755 init_cluster.sh /usr/local/bin/init_cluster
COPY --chmod=755 grant_user.sh /usr/local/bin/grant_user

# https://docs.docker.com/engine/reference/builder/#healthcheck
HEALTHCHECK --interval=10s --timeout=6s --start-period=30s --retries=3 CMD [ "/usr/local/bin/healthcheck.py" ]

ENTRYPOINT ["/usr/local/bin/entrypoint"]

CMD ["mongod"]

EXPOSE 27017
