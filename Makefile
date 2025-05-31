POETRY_VERSION=1.8.3

ci-prebuild:
	python -m pip install poetry setuptools
	cat /dev/null > requirements.txt

clean:
	rm -f .coverage
	rm -f requirements.txt
	rm -f .pytest_cache
	rm -rf dist
	rm -f reports

.PHONY:= build
build: ##
	python -m poetry install

.PHONY:= package
package: ##
	python -m poetry build --format=wheel

.PHONY: format
format: ##
	ruff format .

.PHONY: ci
ci: clean build package

.PHONY: docker-build
docker-build:
	docker build -t review_extractor .

