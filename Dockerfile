FROM python:3.8-rc-buster
WORKDIR /app
VOLUME /app

RUN apt-get update
RUN apt-get install -y curl unzip apt-transport-https git
RUN pip install -U pip

RUN pip install beefore
RUN pip install -U tigerthebee

ADD tools /tools
CMD ["/tools/run.sh"]
