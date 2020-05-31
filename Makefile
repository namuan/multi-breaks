export PROJECTNAME=$(shell basename "$(PWD)")

.SILENT: ;               # no need for @

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean: clean-pyc ## Clean package
	rm -rf build dist

black: ## Runs black for code formatting
	black multi-breaks.py

lint: black ## Runs Flake8 for linting
	flake8 multi-breaks.py

setup: ## Re-initiates virtualenv
	rm -rf venv
	python3 -m venv venv
	./venv/bin/python3 -m pip install -r requirements/dev.txt

deps: ## Reinstalls dependencies
	./venv/bin/python3 -m pip install -r requirements/dev.txt

package: clean ## Rebuilds venv and packages app
	./venv/bin/python3 -m pip install -r requirements/build.txt
	./venv/bin/python3 setup.py py2app

run: ## Runs the application
	./venv/bin/python3 multi-breaks.py

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo