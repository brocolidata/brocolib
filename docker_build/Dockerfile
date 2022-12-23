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

# ENV PYTHONPATH "/brocolib"
ENV PYTHONPATH "${PYTHONPATH}:/brocolib/extract_load"
ENV PYTHONPATH "${PYTHONPATH}:/brocolib/transform"
ENV PYTHONPATH "${PYTHONPATH}:/brocolib/utils:/brocolib/utils/brocolib_utils"
ENV PYTHONPATH "${PYTHONPATH}:/brocolib/factory_utils:/brocolib/factory_utils/brocolib_factory_utils"


# Copy & Install the dependencies file
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "${PATH}:~/.local/bin"
