Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Navigate to the 'browsers' directory and install dependencies
Push-Location -Path "browsers"
pipenv install
Pop-Location

# Create a Docker network if it doesn't already exist
docker network create hekthon -ErrorAction SilentlyContinue

# Navigate to 'docker-logging' and start Docker Compose services
Push-Location -Path "docker-logging"
$env:COMPOSE_PROJECT_NAME = "docker-logging"
docker-compose up -d --remove-orphans
Pop-Location

# Navigate to 'docker-services' and start Docker Compose services
Push-Location -Path "docker-services"
$env:COMPOSE_PROJECT_NAME = "docker-services"
docker-compose up -d --remove-orphans
Pop-Location

# Navigate to 'docker-services/docker-tempo' and start Docker Compose services with a specific configuration
Push-Location -Path "docker-services/docker-tempo"
$env:COMPOSE_PROJECT_NAME = "temporal"
docker-compose -f docker-compose-cass-es.yml up -d --remove-orphans
Pop-Location

# Navigate to 'browsers', stop any existing services, and start Docker Compose services with a specific configuration
Push-Location -Path "browsers"
$env:COMPOSE_PROJECT_NAME = "browsers"
docker-compose down -t 1 -ErrorAction SilentlyContinue
docker-compose -f docker-compose.yml up -d --remove-orphans --build
Pop-Location
