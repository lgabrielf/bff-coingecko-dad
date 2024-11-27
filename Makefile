.PHONY: docker-build docker-run docs format install lint mgtdown mgtinit mgtrevision mgtup requirements run security test update

# Define the default function to run when no target is specified
.DEFAULT_GOAL := help

#Define the host and port for running the project
HOST := localhost
PORT := 8088

# Define the name of the environment file
ENV_FILE := .env

# Read the variables from the environment file and export them
include $(ENV_FILE)
VARIABLES := $(grep -v '^#' $(ENV_FILE) | xargs)
export $(VARIABLES)

# CLOUD_BUILD_VARIABLES := $(shell \
# 	grep -v "^#" $(ENV_FILE) | \
# 	sed --expression="s&^&      - '&;s&$$&'-__-&" )

CLOUD_BUILD_VARIABLES := $(shell \
	grep -v "^#" $(ENV_FILE) | \
	sed --expression="s&$$&-__-&" )

# SED_EXPRESSION := 30s&SUBENV&$(CLOUD_BUILD_VARIABLES)&
SED_EXPRESSION := 29s&SUBENV&$(CLOUD_BUILD_VARIABLES)&
SED_EXPRESSION_GITLAB := 4s&G_A_T_ENV&$(GITLAB_ACCESS_TOKEN)&
# Define a help target to display Makefile usage
help:
	@echo "docker-build:"
	@echo "make docker-build GITLAB_ACCESS_TOKEN=__your_token__# Build Docker images from a Dockerfile."
	@echo "docker-run:"
	@echo "make docker-run ENV_FILE=".env" PORT="8089" # Create and run a new container from an image."
	@echo "docs:"
	@echo "make docs # Get and copy openapi.json for docs folder. Attention: Need the API running."
	@echo "format:"
	@echo "make format # Formatting the code using blue and isort."
	@echo "install:"
	@echo "make install  # Install depedencies from pyproject.toml."
	@echo "lint:"
	@echo "make lint # Linting code using blue and isort."
	@echo "mgtdown:"
	@echo "make mgtdown # Downgrade operations, proceeding from the last database revision using alembic."
	@echo "mgtinit:"
	@echo "make mgtinit # Create an environment using the alembic.ini template."
	@echo "mgtrevision:"
	@echo "make mgtrevision MSG="create well table" #  Create a revision file with autogenerate using alembic."
	@echo "mgtup:"
	@echo "make mgtup #  Upgrade operations, proceeding from the current database revision using alembic."
	@echo "requirements:"
	@echo "make requirements # Exports requirements files." 
	@echo "run:"
	@echo "make run ENV_FILE=".env" HOST="localhost" PORT="8089" # Execute the hypercorn for starting project for local endpoint tests."
	@echo "security:"
	@echo "make security # Execute the pip-audit for report malicious library."
	@echo "test:"
	@echo "make test # Execute tests by pytest."
	@echo "update:"
	@echo "make update # Update depedencies in pyproject.toml."
docker-build:
	@poetry run docker build -t bff-coingecko-dad:test .
docker-run:
	@poetry run docker run --rm --name bff-coingecko-dad --env-file $(ENV_FILE) -p $(PORT):8080  bff-coingecko-dad:test
docs:
	@curl -o docs/openapi.json http://$(HOST):$(PORT)/openapi.json
format:
	@poetry run blue .
	@poetry run isort .
install:
	@poetry install
lint:
# Recommend for pre-commit hook if starting project
# echo 'poetry run blue . --check\npoetry run isort . --check' >  .git/hooks/pre-commit
# chmod +x .git/hooks/pre-commit
	@poetry run blue . --check
	@poetry run isort . --check
mgtdown:
	@poetry run alembic downgrade -1
mgtinit:
	@poetry run alembic init alembic
mgtrevision:
	@poetry run alembic revision --autogenerate -m "$(MSG)"
mgtup:
	@poetry run alembic upgrade head
requirements:
	@poetry export -f requirements.txt --without-hashes  > requirements.txt
	@poetry export --dev -f  requirements.txt --without-hashes  > requirements-dev.txt
run:
	@poetry run hypercorn -b "$(HOST):$(PORT)" wellexds.main:app --reload
security:
	@poetry run pip-audit
test:
	@poetry run pytest -v
update:
	@poetry update
