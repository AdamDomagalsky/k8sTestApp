#!/bin/bash

CONTAINER_REGISTRY="${CONTAINER_REGISTRY:-domagalsky}"

set -euo pipefail

IMG_NAME=demo-api

docker image build \
    -f Dockerfile \
    --target $IMG_NAME \
    -t $CONTAINER_REGISTRY/$IMG_NAME:$(git rev-parse HEAD) \
    -t $CONTAINER_REGISTRY/$IMG_NAME:latest \
    .

docker push $CONTAINER_REGISTRY/$IMG_NAME --all-tags
