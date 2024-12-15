#!/bin/sh
#
#set -e
#
#DOCKER_USERNAME=ainatarun
#docker login -u="${DOCKER_USERNAME}" -p="${DOCKER_PASSWORD}"
#
## create buildkit
#docker buildx create --use
#docker buildx inspect --bootstrap
#
#docker buildx build --push \
#  --build-arg BUILDKIT_INLINE_CACHE=1 \
#  --platform linux/amd64 \
#  -t ainatarun/calendly:latest
