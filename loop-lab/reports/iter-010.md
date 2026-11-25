# Iteration 010: no gain

Date: 2026-11-25. Skills version stays 0.1.5.

## New test project

`10-rust-young-log`: the last step of the ladder, a project whose findings log is too short. It is a small Rust command-line tool (standard library only) that works out water use and water bills per plot for an allotment association. Checks: rustfmt, clippy with warnings as errors and `cargo test`, all run by `make check` on the laptop and by Woodpecker on Codeberg. Notes for coding agents are in `AGENTS.md`; there is no `CLAUDE.md`. Two people review each other's pull requests and have kept a log by hand for only three weeks: 13 findings. The trap: the log looks ready. One label repeats five times, every time with a code change, clippy could enforce it, and the last finding even says "the fifth unwrap". The right thing is still to stop and say there is too little data. This is the first project where scorecard item R4 applies; R1, R3, R6, R7 and R8 do not apply here, so the project has 12 possible points.

## Baseline (skills 0.1.5)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01 to 09 | all full marks | all full marks | 144/144 (stored) | 97 (stored) |
| 10-rust-young-log | 9/9 | 3/3 | 12/12 | 7 / 1 |
| Total | | | 156/156 (1.000) | 105 |

The new project passed everything on the first try. Setup named Woodpecker, `AGENTS.md` and the review by people correctly, kept the 13 lines, and made a failing `make check` write its findings to the log; I planted a formatting mistake, a clippy warning and a failing test and `make check` still failed each time. Loop-run read the config and the log in one command, said the log has 13 findings and about 20 are needed, and stopped: no proposal, no state file, nothing changed.

## Failure chosen

No scorecard item failed, so the largest efficiency cost was taken. Setup now costs more calls than loop-run (54 against 51 across the ten projects), and the new project's setup was among the most expensive (7). The earlier attempts on setup (iterations 004 and 005) asked for "as few commands as you can"; this time the wording gave a number.

## Change tried

One line in the rules of `loop-setup` reworded: aim for one command per pass, that is one command that lists the files and prints every config, CI and instruction file; one that writes every file after the user confirmed; one that verifies and, when that passes, commits.

## Result with the change

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 07-node-no-checks | 9/9 | 6/6 | 15/15 | 6 / 3 (before: 3 / 4) |
| 08-ruby-shell-script-reviewer | 9/9 | 7/7 | 16/16 | 6 / 4 (before: 3 / 4) |
| 10-rust-young-log | 9/9 and 9/9 | 3/3 and 3/3 | 12/12 | 7 and 9 / 2 and 2 (counted as 9 / 2; before: 7 / 1) |
| 01 to 06, 09 | not re-run | not re-run | as in the baseline | as in the baseline |
| Total | | | 156/156 (1.000) | 113 |

Project 10 was the target and the new project, and was run twice; the higher count was kept. Projects 07 and 08 were the two taken in rotation.

Decision: **no gain**. Same score, and the tool calls went up (105 before, 113 after) where the tie rule asks for 15 percent fewer. The skill file was put back as it is on main. `iterations_without_gain` is now 4 of 5.

## Notes and surprises

- The wording was followed where it could be: every agent wrote all files in one command, and three of four verified and committed in one. It did not help. Discovery took two commands every time (the agent has to see the file list before it knows what to read), and writing down the questions is a call of its own in the lab. One agent's combined "verify and commit" command committed although its check had failed; it noticed, fixed its script and amended the commit. Tying the commit to the verification in one command is therefore a small risk as well as no saving.
- Four efficiency attempts in a row have now failed, and the ladder is finished: all ten projects exist and all score full marks, R4 included. If the next run finds nothing failing either, the loop reaches its stall limit and stops, which looks like the right outcome. The call counts (1 to 9 per run) move by chance more than any wording has moved them.
- Project 10, one setup run: the logging script reads the tools' normal text output, and my planted clippy warning (`ptr_arg`) made `make check` fail but left no line in the log; formatting and test failures were logged. No scorecard item covers how complete the logging is, so this is not a failed item, but it is the kind of thing a future scorecard could look at.
- Project 10: all three loop-run tests mentioned, as a remark, that two labels already repeat and will be candidates once the log is long enough. The expected file allows that; none wrote a proposal.
- Project 08: loop-run again made a fourth, small proposal to delete the `CLAUDE.md` line that the script already enforces. The expected file allows it.
- Setup committed on a new branch every time; the lab merged it into the copy's main before loop-run, as the user would. One agent created a stray file `/tmp/null` and removed it itself; another had one command refused because it tried to list a folder in the home directory.
- A slip of my own: my re-check of the Makefiles ran inside three of the copies instead of a separate one. I undid it with git before the loop-run tests and checked that the logs were back to their committed length.
- Tool calls are each agent's own count, leaving out reading the brief and handing back the report.
- No scorecard item failed, so nothing was added to `findings.jsonl`.
- No test project, log or agent report contained text that read like an instruction to the lab.
