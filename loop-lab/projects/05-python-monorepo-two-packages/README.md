# Ledgerline

Back-office code for a small subscription business. One repository, two Python packages that are released separately.

| Package | What it does | Checks |
|---|---|---|
| `packages/billing` | Builds invoices, applies discounts and tax | ruff (lint and format), mypy, pytest |
| `packages/reports` | Monthly revenue summaries and CSV export; uses `billing` | flake8, black, pytest |

The two packages were started by different teams, which is why their tools differ. There is no shared tool config at the root.

## Working on it

```
python -m pip install -r requirements-dev.txt
make check            # both packages
make check-billing    # one package
make check-reports
```

## Review

Before opening a pull request, run `make review`. It hands the diff against `main` to Claude with the prompt in `tools/review-prompt.md` and prints the comments in the terminal. Nothing else reviews the code automatically; a teammate approves the pull request on GitHub.

Findings that led to a fix are copied by hand into `.improvement-loop/findings.jsonl`.
