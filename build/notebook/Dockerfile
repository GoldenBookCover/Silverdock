# notebook
ARG SILVERDOCK_PYTHON_VERSION
ARG SILVERDOCK_OS_DEBIAN_PREFER=bookworm
FROM python:${SILVERDOCK_PYTHON_VERSION}-${SILVERDOCK_OS_DEBIAN_PREFER}

ARG SILVERDOCK_PYTHON_VERSION
LABEL maintainer MonstreCharmant
ENV PYTHONUNBUFFERED 1

RUN apt update \
    && apt -yqq install \
        vim \
        gosu \
    && install -d -m 755 -o root -g root /root/.jupyter \
    && pip install jupyterlab

COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint

WORKDIR /notebook
EXPOSE 8888

ENTRYPOINT [ "/usr/local/bin/entrypoint" ]
CMD [ "jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser" ]

