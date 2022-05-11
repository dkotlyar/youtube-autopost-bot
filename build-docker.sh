#!/bin/bash
DIR=$(dirname `readlink -f $0`)
DOCKERFILE=$DIR/Dockerfile
docker build -f $DOCKERFILE -t youtube-bot/youtube-bot $DIR
