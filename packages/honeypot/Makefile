check-format:
	poetry run black . --check
lint:
	poetry run flake8 .
static-analysis-pyre:
	poetry run pyre --noninteractive check
static-analysis-mypy:
	poetry run mypy --strict .
test-unit:
	python -m unittest discover -s ./src/
start-server-simple-http:
	ENABLE_SIMPLE_HTTP=true python ./src/main.py