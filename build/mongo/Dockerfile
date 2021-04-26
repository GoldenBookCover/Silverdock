ARG SIRVERDOCK_MONGO_VERSION

FROM mongo:${SIRVERDOCK_MONGO_VERSION}-bionic

VOLUME /data/db /data/configdbs

CMD ["mongod", "--auth"]

EXPOSE 27017
