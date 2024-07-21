set -ex

(
cd browsers
pipenv install
)


docker network create hekthon || true

(
    cd loki-the-god-of-logging
    docker-compose up -d --remove-orphans
)

(
    cd browsers/docker-tempo
    COMPOSE_PROJECT_NAME=temporal docker-compose down -t 1 --remove-orphans -v || true
    COMPOSE_PROJECT_NAME=temporal docker-compose rm -f -v
    docker volume rm -f   temporal_temporalio_cass    temporal_temporalio_es
    COMPOSE_PROJECT_NAME=temporal docker-compose -f docker-compose-cass-es.yml up -d --remove-orphans
)

(
    cd browsers

    COMPOSE_PROJECT_NAME=browsers docker-compose down -t 1 || true
    COMPOSE_PROJECT_NAME=browsers docker-compose -f docker-compose.yml up -d --remove-orphans --build
)
