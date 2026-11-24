# acme/bookings

Small service for room bookings: creating and rescheduling bookings, working out prices and cancellation fees.

## Development

    composer install
    composer check    # PHPStan, PHP-CS-Fixer (dry run) and PHPUnit
    composer cs:fix   # fix code style

The same three checks run in GitHub Actions on every pull request (`.github/workflows/ci.yml`).

Changes are written with a coding agent (see `CLAUDE.md`). Before merging, the `code-reviewer` subagent in `.claude/agents/` reviews the diff and prints its findings in the conversation.

`.improvement-loop/findings.jsonl` is a list of findings from the checks and the reviewer that I have been copying in by hand since September, one JSON object per line.
