# Define PROJECT_DIR variable to get the directory of the Makefile
this := $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
PROJECT_DIR := $(dir $(this))

# Target to display help message
help:
	@echo "Make targets:"
	@echo "============="
	@awk '/^[a-zA-Z_-]+:.*?## / {split($$0, N, ":.*?## "); printf "%-20s %s\n", N[1], N[2]}' $(MAKEFILE_LIST) | sort


# Define variables
COMPOSE = docker-compose
API_CONTAINER = api

# Targets
build: ## Build containers if using GPU
	$(COMPOSE) build

build-cpu: ## Build containers if using CPU
	$(COMPOSE) -f docker-compose-cpu.yml build

up: ## Run containers if using GPU
	$(COMPOSE) up

up-cpu: ## Run containers if using CPU
	$(COMPOSE) -f docker-compose-cpu.yml up

down-cpu:  ## Stop and remove the docker-compose containers if using CPU
	$(COMPOSE) -f docker-compose-cpu.yml down

down:  ## Stop and remove the docker-compose containers if using GPU
	$(COMPOSE) -f docker-compose.yml down

migrations: ## Run database migration commands
	bash run_migrations.sh

api-container: ## Grab API container and open Bash shell
	$(COMPOSE) exec $(API_CONTAINER) bash

restart: ## Restart containers
	$(COMPOSE) restart

test:  # Run Django tests
	$(COMPOSE) exec $(API_CONTAINER) bash -c "python manage.py test"

django-shell: ## Get a django Ipython shell inside the api container
	$(COMPOSE) exec $(API_CONTAINER) bash -c "python manage.py shell"

db-shell:  ## Get an interactive shell inside the db container
	$(COMPOSE) exec pgsql bash

frontend:  ## Get an interactive shell inside the frontend container
	$(COMPOSE) exec frontend bash
