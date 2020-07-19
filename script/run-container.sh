#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker run \
  -v $DIR/../data:/data \
  -v $DIR/../backend:/backend \
  -p 0.0.0.0:5000:5000/tcp \
  -e FLASK_ENV=development \
  quipper \
  python /backend/app.py
