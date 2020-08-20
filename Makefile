MODULE := app

# This version-strategy uses git tags to set the version string
TAG := $(shell git describe --tags --always --dirty)

init:
	python3 setup.py install

run:
	@python -m $(MODULE)

test:
	@pytest


lint:
	@echo "\n${BLUE}Running Pylint against source and test files...${NC}\n"
	@pylint --rcfile=setup.cfg **/*.py
	@echo "\n${BLUE}Running Flake8 against source and test files...${NC}\n"
	@flake8
	@echo "\n${BLUE}Running Bandit against source files...${NC}\n"
	@bandit -r --ini setup.cfg

venv-unix:
	python3 -m venv venv

venv-windows:
	py -3.7 -m venv venv

version:
	@echo $(TAG)

.PHONY: clean image-clean build-prod push test

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml
