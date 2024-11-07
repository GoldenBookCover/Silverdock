# python application
ARG SILVERDOCK_PYTHON_VERSION
ARG SILVERDOCK_OS_DEBIAN_PREFER=bookworm
FROM python:${SILVERDOCK_PYTHON_VERSION}-${SILVERDOCK_OS_DEBIAN_PREFER}

ARG SILVERDOCK_PYTHON_VERSION
LABEL maintainer MonstreCharmant
ENV PYTHONUNBUFFERED 1

ARG PYTHON_REQUIREMENTS
ARG PUID=1000
ARG PGID=1000
ARG PYTHON_TORCH_VERSION=lastest
ARG PYTHON_TORCH_INDEX

RUN apt update \
    && apt -yqq install \
        vim \
        gosu \
    && groupmod -o -g ${PGID} www-data \
    && usermod -o -u ${PUID} -g www-data www-data \
    && install -o www-data -g www-data -m 775 -d /var/www

RUN if [ ! "x${PYTHON_TORCH_VERSION}" = "x" ]; then \
        if [ "x${PYTHON_TORCH_INDEX}" = "x" ]; then \
            index_url=""; \
        else \
            index_url="--index-url https://download.pytorch.org/whl/${PYTHON_TORCH_INDEX}"; \
        fi; \
        if [ "x${PYTHON_TORCH_VERSION}" = "xlatest" ]; then \
            torch_version=""; \
        else \
            torch_version="==${PYTHON_TORCH_VERSION}"; \
        fi; \
        pip install torch${torch_version} torchvision torchaudio ${index_url}; \
    fi

RUN echo "${PYTHON_REQUIREMENTS}" > /tmp/requirements.txt \
    && pip install -r /tmp/requirements.txt

COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint

WORKDIR /var/www
ENTRYPOINT [ "/usr/local/bin/entrypoint" ]
CMD [ "gosu", "www-data", "python", "main.py" ]

