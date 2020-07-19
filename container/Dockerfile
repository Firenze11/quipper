FROM debian:buster-slim

# for python:
#FROM python:3.8.3-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
  ffmpeg

# ls /data

ADD run.sh /run.sh

CMD /run.sh
