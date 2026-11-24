# Bookings service: notes for coding agents

## Commands

- `composer check` runs everything: PHPStan, PHP-CS-Fixer (dry run) and PHPUnit.
- `composer cs:fix` fixes code style.

## Rules

- Money is always an integer number of cents. Never use floats for money.
- Dates are `DateTimeImmutable`. Never use `DateTime` or `date()`.
- Every new class in `src/` gets a test class in `tests/` with the same name plus `Test`.
- Classes are `final` unless there is a reason written in a comment.
- Do not add Composer packages without asking.

## Before you say a change is done

1. Run `composer check` and fix what it reports.
2. Ask the `code-reviewer` subagent to review the diff and deal with what it finds.
