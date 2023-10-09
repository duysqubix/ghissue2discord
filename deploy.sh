#!/bin/bash 

# stop container if its running 
docker stop ghbot
# remove container if it exists
docker rm ghbot 
# remove image if it exists
docker rmi ghbot

# build image
docker build -t ghbot . && \

# run container
docker run -d --name ghbot -v ./.env:/app/app/.env -p 80:80 ghbot
