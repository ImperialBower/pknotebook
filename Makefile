.PHONY: build build-no-cache up up-d down restart logs shell validate ayce default help

COMPOSE = docker compose
IMAGE   = folkengine/pknotebook:latest

# Default target
default: help

# Display help information
help:
	@echo "Available targets:"
	@echo "  make (default)       - Run ayce"
	@echo "  make build           - Build the Docker image"
	@echo "  make build-no-cache  - Build the Docker image without cache"
	@echo "  make up              - Start JupyterLab in the foreground"
	@echo "  make up-d            - Start JupyterLab in the background"
	@echo "  make down            - Stop and remove containers"
	@echo "  make restart         - Restart running containers"
	@echo "  make logs            - Tail container logs"
	@echo "  make shell           - Open a shell in the running container"
	@echo "  make validate        - Build image and verify pkpy imports correctly"
	@echo "  make ayce            - Run build and validate"
	@echo "  make help            - Display this help message"
	@echo ""

# Build the Docker image
build:
	$(COMPOSE) build

# Build without layer cache (useful after Dockerfile or pkpy version changes)
build-no-cache:
	$(COMPOSE) build --no-cache

# Start JupyterLab in the foreground
up:
	$(COMPOSE) up

# Start JupyterLab in the background
up-d:
	$(COMPOSE) up -d

# Stop and remove containers
down:
	$(COMPOSE) down

# Restart running containers
restart:
	$(COMPOSE) restart

# Tail container logs
logs:
	$(COMPOSE) logs -f

# Open a bash shell in the running JupyterLab container
shell:
	$(COMPOSE) exec jupyterlab /bin/bash

# Verify pkpy is installed and importable inside the image
validate:
	@echo "Validating pkpy installation..."
	@docker run --rm $(IMAGE) python -c "import pkpy; print('pkpy OK')" \
		&& echo "Validation passed." \
		|| (echo "Validation FAILED." && exit 1)

# All You Can Eat - build and validate
ayce: build validate
