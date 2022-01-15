FROM ubuntu:latest

RUN apt-get -y update && apt-get -y upgrade \
    && apt-get -y install \
        curl \
        unzip \
        bash \
        python3-dev \
        python3.7 \
        python3-pip \        
        git \
        make \
        libffi-dev \
        jq \
    && pip install --upgrade pip

ENV PYTHONPATH "/src"
ENV PYTHONPATH "${PYTHONPATH}:/src/extract_load"
ENV PYTHONPATH "${PYTHONPATH}:/src/transform"
ENV PYTHONPATH "${PYTHONPATH}:/src/utils:/src/utils/brocolib_utils"
ENV PATH "${PATH}:/src"

COPY requirements.txt .
RUN pip3 install -r requirements.txt
