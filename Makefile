# Portions of this Makefile are derived from cookiecutter-uv-example
# Copyright 2025 Florian Maas
# Licensed under the Apache License, Version 2.0
# https://github.com/fpgmaas/cookiecutter-uv-example/blob/main/Dockerfile

.PHONY: venv 
venv: ## Create venv
	@echo "Create venv"
	@uv sync


.PHONY: quality
quality: ## Run code quality tools.
	@echo "Check deps consitency"
	@uv lock --locked
	@echo "mypy type checking"
	@uv run mypy --txt-report mypy-report src/
	@echo "Check deps"
	@uv run deptry . --per-rule-ignores "DEP003=aisdecoder"  --extend-exclude  scripts

.PHONY: test
test: ## Run tests
	@echo "Unit tests"
	@uv run python -m unittest discover tests/unit/

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help