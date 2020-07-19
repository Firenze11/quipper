FROM python:3.8.3-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
  ffmpeg

# ls /data

ADD requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt
