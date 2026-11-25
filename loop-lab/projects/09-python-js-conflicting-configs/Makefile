.PHONY: check lint-py test-py lint-js serve

check: lint-py test-py lint-js

lint-py:
	ruff check backend

test-py:
	python -m pytest

lint-js:
	npx eslint frontend

serve:
	PYTHONPATH=backend python -m repaircafe.api
