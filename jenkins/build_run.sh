#!/bin/bash

# *** BUILD TEST ***

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Docker is not running"
  exit 1
fi

# Start Docker Compose services
docker compose up --build -d

sleep 1

# Check if all containers are running
if [ "$( docker container inspect -f '{{.State.Running}}' redis )" == "true" ]; then
        echo "[OK] Script build - redis is running"

        if [ "$( docker container inspect -f '{{.State.Running}}' monitoring-app )" == "true" ]; then
                echo "[OK] Script build - monitoring-app is running"

                if [ "$( docker container inspect -f '{{.State.Running}}' monitoring-client )" == "true" ]; then
                        echo "[OK] Script build - monitoring-client is running"
                else
                        echo "[ERR] Script build - monitoring-client not running"
                        exit 1
                fi
        else
                echo "[ERR] Script build - monitoring-app not running"
                exit 1
        fi
else
        echo "[ERR] Script build - redis not running"
        exit 1
fi

exit 0