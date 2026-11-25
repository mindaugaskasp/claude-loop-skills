# Nudge

Sends text-message reminders to patients of a small clinic before their appointments. It reads the day's appointments from a CSV export of the booking system and works out which reminders are due.

## Working on it

```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
make check
```

`make check` runs the linter (ruff), the formatter check (ruff format) and the tests (pytest). The tests were added in October; before that the project had only ruff. The same three checks run in GitHub Actions on every pull request.

## Review

Before a pull request is opened, the `reviewer` subagent (`.claude/agents/reviewer.md`) reads the diff in Claude Code. A teammate then approves the pull request on GitHub.

## Improvement loop

The project keeps a log of review and linter findings in `.improvement-loop/findings.jsonl` and turns repeated ones into rules. Settings are in `.improvement-loop.json`; the rules proposed so far are in `.improvement-loop/state.json`. `make log-findings` writes the linter's current findings to the log. The loop was set up at the end of August, and the improvement run is started by hand.
