FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y upgrade \
    && apt-get -y install \
        software-properties-common \
        curl \
        unzip \
        bash \
        pip \
        git \
        make \
        libffi-dev \
        jq \
        libpq-dev\
        gcc

# ENV PYTHONPATH "/src"
ENV PYTHONPATH "${PYTHONPATH}:/src/extract_load"
ENV PYTHONPATH "${PYTHONPATH}:/src/transform"
ENV PYTHONPATH "${PYTHONPATH}:/src/utils:/src/utils/brocolib_utils"
ENV PYTHONPATH "${PYTHONPATH}:/src/factory_utils:/src/factory_utils/brocolib_factory_utils"

COPY requirements.txt .
RUN pip install -r requirements.txt
