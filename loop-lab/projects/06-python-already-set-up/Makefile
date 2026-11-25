.PHONY: lint format-check test check log-findings

lint:
	ruff check .

format-check:
	ruff format --check .

test:
	python -m pytest -q

check: lint format-check test

# Append the linter's current findings to the improvement-loop log.
log-findings:
	ruff check --output-format json --exit-zero . | python tools/improvement-loop/log-findings --source ruff
