#FROM centos:7.9.2009
FROM python:3.8:apline

LABEL "maintainer" = "13776668123@163.com"

USER root

COPY requirements.txt /root/fdj/

WORKDIR /root/fdj

RUN python -m pip install  --upgrade pip && pip3 install -r requirements.txt

COPY . /root/fdj
