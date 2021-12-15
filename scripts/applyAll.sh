#!/bin/bash

kubectl apply -k $(git rev-parse --show-toplevel)/k8s
