# Loop lab

A scheduled task improves the `loop-engineering` skills by running the improvement loop on the skills themselves, one iteration per session.

- `PROTOCOL.md` : what one iteration does. Fixed.
- `SCORECARD.md` : how a run of the skills is scored. Fixed.
- `state.json` : progress, scores and history. Set `status` to `paused` to stop the loop; set it back to `running` to resume.
- `findings.jsonl` : every failed scorecard item.
- `projects/` and `expected/` : test projects and the known truth about each.
- `reports/` : one short report per iteration.
