#!/usr/bin/env bash

# Cargar variables de entorno desde el archivo .env
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

sonar-scanner \
    -Dsonar.projectKey=flask-socketio \
    -Dsonar.sources=. \
    -Dsonar.host.url=http://localhost:9000 \
    -Dsonar.token="${SONAR_KEY}"
