# notebook
ARG SILVERDOCK_PYTHON_VERSION
ARG SILVERDOCK_OS_DEBIAN_PREFER=bookworm
FROM python:${SILVERDOCK_PYTHON_VERSION}-${SILVERDOCK_OS_DEBIAN_PREFER}

ARG SILVERDOCK_PYTHON_VERSION
LABEL maintainer MonstreCharmant
ENV PYTHONUNBUFFERED 1

ARG PUID=1000
ARG PGID=1000

# Import entrypoint script to control startup
COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint

RUN apt update \
    && apt -yqq install \
        vim \
        gosu \
    && groupadd -o -g ${PGID} note \
    && useradd -o -g note -u ${PUID} -m -s /bin/bash note \
    # /home/note/.jupyter 是默认配置目录，jupyter 会从这里读取配置文件 \
    # /home/note/.jupyter is the default config folder, where jupyter loads config files
    && install -d -m 755 -o note -g note /home/note/.jupyter \
    && pip install jupyterlab

# 工作目录，打开 jupyter 时默认位于这里
WORKDIR /home/note

EXPOSE 8888

ENTRYPOINT [ "/usr/local/bin/entrypoint" ]
CMD [ "jupyter", "lab", "--ip=0.0.0.0" ]

