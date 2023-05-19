#!/bin/bash

# *** STEP PUSH ***

# Stop all containers 
docker compose -f jenkins/docker-compose.yaml down

# Tag Monitoring images
docker tag monitoring:latest tizianoadv/monitoring:latest
docker tag client:latest tizianoadv/client:latest

# Push all images to Docker Hub
docker push tizianoadv/monitoring:latest
docker push tizianoadv/client:latest

# Remove all images
docker rmi tizianoadv/monitoring:latest
docker rmi tizianoadv/client:latest
docker rmi $(docker images -qa)