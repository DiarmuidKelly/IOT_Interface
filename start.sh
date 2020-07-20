#!/bin/bash
app="docker.test"
docker build -t ${app} .
docker run -d -p 3030:3030 \
  --name=${app} \
  -v $PWD:/app ${app}