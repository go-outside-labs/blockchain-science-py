.PHONY: install
install:
	@poetry install

.PHONY: clean
clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf .tox
	@rm -rf .pytest_cache
	@poetry env remove --all

.PHONY: lint
lint:
	@tox -e lint

.PHONY: test
test:
	@pytest -vvv

.PHONY: example
example:
	@poetry run python src/main.py -e

.PHONY: api
api:
	@poetry run python src/main.py -a
