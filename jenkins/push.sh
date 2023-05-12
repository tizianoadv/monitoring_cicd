#!/bin/bash

# *** STEP PUSH ***

# Stop all containers 
docker compose down

# Tag Monitoring images
docker tag monitoring:latest tizianoadv/monitoring:latest
docker tag client:latest tizianoadv/client:latest

# Push all images to Docker Hub
docker push tizianoadv/monitoring:latest
docker push tizianoadv/client:latest