#!/bin/bash
set -e
INPUT_DIR=${INPUT_DIR:-/dockers/xInfraDist/docker-us}
OUTPUT_DIR=${OUTPUT_DIR:-/dockers/xInfraDist/docker-us}
BACKUP_DIR=${BACKUP_DIR:-/dockers/xInfraDist/docker-us/compose-update-backup}
with_timestamp() {
    date +"dc_backup_%Y-%m-%d_%H-%M-%S.yml"
}
WITH_TIMESTAMP="$(with_timestamp)"
if [[ "$(docker images -q compose-update:latest 2> /dev/null)" == "" ]]; then
    (>&2 echo 'Missing docker image: compose-update:latest. Please, checkout the code from https://gitlab.com/x/compose-update.git, open the README.md file and follow the instructions.')
    exit 1
elif [ $# -lt 2 ]; then
    (>&2 echo "Usage: $0 registry_socket_address docker_image")
    (>&2 echo "Example: $0 192.168.10.1:5001 x-us-field:34")
    exit 2
else
    SERVICE_NAME="$(echo $2 | cut -d ':' -f1 | tr -d -)"
    mkdir -p $BACKUP_DIR
    docker run --rm\
        --name compose-update \
        -v "$INPUT_DIR":/usr/src/app/input:ro \
        -v "$OUTPUT_DIR":/usr/src/app/output \
        -v "$BACKUP_DIR":/usr/src/app/backup \
        compose-update:latest  \
            input/docker-compose.yml $2 output/docker-compose.yml \
            --backup backup/$WITH_TIMESTAMP
    docker pull $1/$2
    docker tag $1/$2 $2
    cd $OUTPUT_DIR
    docker-compose up -d --no-deps --no-build $SERVICE_NAME
fi

