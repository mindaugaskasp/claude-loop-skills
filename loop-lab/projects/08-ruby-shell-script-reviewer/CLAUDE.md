# Notes for the coding agent

- Ruby 3.3, standard library plus the `csv` gem. Do not add gems.
- Every Ruby file starts with `# frozen_string_literal: true`.
- Commands in `bin/seedbox` only read arguments and print. The work belongs in `lib/seedbox/`.
- Data files are CSV with a header row. Paths come from `Seedbox::Config`, never from a string in the code.
- A loan lasts 180 days. That number lives in `Seedbox::Policy` and nowhere else.
- Run `make review` before you say a task is done.
