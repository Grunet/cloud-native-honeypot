check-format:
	poetry run black . --check
lint:
	poetry run flake8 .
static-analysis-pyre:
	poetry run pyre --noninteractive check
static-analysis-mypy:
	poetry run mypy --strict .