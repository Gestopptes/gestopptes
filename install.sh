set -ex

(
cd browsers
pipenv install
)


(
cd browsers/docker-tempo
COMPOSE_PROJECT_NAME=temporal docker-compose -f docker-compose-cass-es.yml up -d --remove-orphans
)

docker network create hekthon || true
(
cd browsers
COMPOSE_PROJECT_NAME=browsers docker-compose -f docker-compose.yml up -d --remove-orphans --build
)
