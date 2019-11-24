FROM ubuntu:18.04

RUN apt-get update \
&& apt-get install -y python3.7 \
&& apt-get install -y python3.7-dev \
&& apt-get install -y python3-pip \
&& apt-get install -y nano \
&& apt-get install -y locales \
&& apt-get install -y wget \
&& apt-get install -y build-essential \
&& apt-get install -y libffi-dev \
&& apt-get install -y libssl-dev \
&& apt-get install -y mysql-client \
&& apt-get install -y default-libmysqlclient-dev \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    PYTHONIOENCODING=utf-8

COPY ./requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

COPY . /usr/src/cocode-api
WORKDIR /usr/src/cocode-api

CMD ["python3", "main.py", "run"]