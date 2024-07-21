# Manage the temporal docker containers
Push-Location browsers/docker-tempo
$env:COMPOSE_PROJECT_NAME = "temporal"
docker volume rm -f temporal_temporalio_cass temporal_temporalio_es
docker-compose -f docker-compose-cass-es.yml up -d --remove-orphans
Pop-Location

# Manage the browsers docker containers
Push-Location browsers
$env:COMPOSE_PROJECT_NAME = "browsers"
docker-compose -f docker-compose.yml up -d --remove-orphans --build
Pop-Location

# Manage the llm docker containers
Push-Location llm
$env:COMPOSE_PROJECT_NAME = "llm"
docker-compose -f docker-compose.yml up -d --remove-orphans --build
Pop-Location