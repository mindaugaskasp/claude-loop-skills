.PHONY: review check run

# The only check this project has. Run it before every merge.
review:
	@scripts/review.sh

check: review

run:
	@bundle exec bin/seedbox due
