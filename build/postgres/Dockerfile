ARG POSTGRES_VERSION=17
ARG OS_PREFER=alpine
FROM postgres:${POSTGRES_VERSION}-${OS_PREFER}

# RUN apk add --update \
#     python3 \
#     python3-dev \
#     py-pip

ARG POSTGRES_USER=postgres
HEALTHCHECK --interval=10s --timeout=6s --start-period=30s --retries=3 \
    CMD pg_isready -U "$POSTGRES_USER" || exit 1
