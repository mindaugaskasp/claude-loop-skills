.PHONY: check check-billing check-reports review

check: check-billing check-reports

check-billing:
	cd packages/billing && ruff check .
	cd packages/billing && ruff format --check .
	cd packages/billing && mypy
	cd packages/billing && pytest -q

check-reports:
	cd packages/reports && flake8
	cd packages/reports && black --check .
	cd packages/reports && pytest -q

review:
	git diff main...HEAD | claude -p "$$(cat tools/review-prompt.md)"
