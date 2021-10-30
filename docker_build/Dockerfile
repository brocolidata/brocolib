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

RUN mkdir -p /src
# RUN rm /var/cache/apk/*

WORKDIR /src
# RUN mkdir devops
# ADD devops ./devops
# ADD modules ./modules
# # CMD echo "Hello Amir this is a container used for Terraform and Nomad"
