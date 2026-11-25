# seedbox

A small command-line helper for the Zalgiris street seed library. Neighbours borrow packets of seeds in spring and bring back seeds from their own plants in autumn. This tool keeps the list of loans, shows what is due back and writes the reminder letters.

It is plain Ruby with one gem (`csv`). Data lives in CSV files under `data/`.

## Use

```
bundle install
bundle exec bin/seedbox lend  <member-id> <packet-id>
bundle exec bin/seedbox back  <loan-id>
bundle exec bin/seedbox due
bundle exec bin/seedbox remind
bundle exec bin/seedbox import <file.csv>
```

`import` reads the member list that the library's sign-up form exports.

## Checking a change

There is one check: `make review`. It runs `scripts/review.sh`, a shell script I wrote that looks through the Ruby files for the mistakes I kept making (and that the coding agent kept making). It prints one line per problem and fails when it finds any. I do not merge a branch until it prints nothing.

There are no tests and no linter, and nothing runs on the server when a branch is pushed. The code is on our own Gitea, which has no runners.

Besides the script, I read every change myself before merging. When the script or I find something, I note it in `notes/review-log.jsonl`, one line per finding, with whether it led to a fix. I have done that by hand since late September.

## Layout

- `bin/seedbox` : the commands. Keep them thin.
- `lib/seedbox/` : the work.
- `lib/seedbox/clock.rb` : the one place that asks what time it is.
- `scripts/review.sh` : the review script.
- `notes/review-log.jsonl` : the findings log.
