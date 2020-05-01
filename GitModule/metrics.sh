#!/usr/bin/env bash

# get current directory
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#create volume
# docker volume create metrics

# build and run docker, then get container id
docker build . -t code
docker run -v metrics:/metrics code --url="$1"
CONTAINERID=$(docker ps -q -n 1)

#copy volume data to current directory
# docker cp $CONTAINERID:/metrics $DIR

# cleanup
# remove containers, images, and volumes
#echo "stopping docker"
#docker stop $CONTAINERID
# docker system prune -a --volumes
echo "Metrics created"