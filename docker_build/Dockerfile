FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y upgrade \
    && apt-get -y install \
        software-properties-common \
        curl \
        unzip \
        bash \
        python3-pip \
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
ENV PYTHONPATH "${PYTHONPATH}:/src/factory_utils:/src/utils/brocolib_factory_utils"

# Copy & Install the dependencies file
COPY requirements.txt .
RUN pip install -r requirements.txt
