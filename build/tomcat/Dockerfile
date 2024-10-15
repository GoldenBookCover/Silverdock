ARG SILVERDOCK_OPENJDK_VERSION=8u442-alpine3.19
FROM amazoncorretto:${SILVERDOCK_OPENJDK_VERSION}

ARG PUID=1000
ARG PGID=1000

RUN apk add --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
      gosu \
      vim \
      shadow \
      bash \
      fontconfig \
      ttf-dejavu \
    && groupadd -o -g $PGID tomcat \
    && useradd -o -u $PUID -g tomcat -m tomcat \
    && install -m 775 -o tomcat -g tomcat -d /usr/local/tomcat

COPY --chmod=555 entrypoint.sh /usr/local/bin/entrypoint

ENTRYPOINT ["/usr/local/bin/entrypoint"]
WORKDIR /usr/local/tomcat
