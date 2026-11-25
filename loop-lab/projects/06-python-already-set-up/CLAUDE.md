# Nudge: notes for coding agents

- Run `make check` before you say a change is done.
- Standard library only at run time. Do not add dependencies without asking.
- Always use timezone-aware datetimes and take the clinic's zone from `Settings.time_zone`. Never call `datetime.now()` or `datetime.utcnow()` without a zone.
- The command line writes with `sys.stdout.write`. Library code reports through `logging` and never prints.
- Message texts live in `nudge/templates.py` and nowhere else.
- Phone numbers are kept in international form (`+370...`) and are checked when the CSV is read.
- Before opening a pull request, ask the `reviewer` subagent to review the diff.
