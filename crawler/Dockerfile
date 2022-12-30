FROM python:3.8.10

RUN apt-get update
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

RUN mkdir -p /build
WORKDIR /build
COPY . /build
CMD ["scrapyd"]