.PHONY: fmt fmt-check lint test check run

fmt:
	cargo fmt

fmt-check:
	cargo fmt --check

lint:
	cargo clippy --all-targets -- -D warnings

test:
	cargo test

# Everything that must pass before a pull request is opened.
check: fmt-check lint test

run:
	cargo run -- data/readings.csv 310
