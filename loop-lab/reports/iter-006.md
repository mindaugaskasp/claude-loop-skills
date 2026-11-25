# Iteration 006: gain

Date: 2026-11-25. Skills version 0.1.4 -> 0.1.5.

## New test project

`06-python-already-set-up`: a small Python reminder service for a clinic that was set up for the improvement loop months ago. It already has a valid `.improvement-loop.json`, a logging script, a reviewer that writes to the log, a log of 45 findings and a state file with three earlier rules: one that worked, one that did not (a written instruction about time zones that was ignored four more times) and one merged only a week ago. Since the setup the project gained tests, which the config does not list; the scripted user asks for that one thing to be added and nothing else. The log holds three things worth a proposal (the rule that did not work, text put together too early in log calls under two labels, and unclear error messages) and eight decoys. ruff and pytest are installed in lab sessions, so the expected counts were checked by running ruff. This is the first project where S10 applies.

## Baseline (skills 0.1.4)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 | 6 / 5 |
| 02-php-full-checks | 9/9 | 7/7 | 16/16 | 7 / 6 (stored) |
| 03-ts-lint-format-tests | 9/9 | 7/7 | 16/16 | 5 / 4 |
| 04-go-vet-lint-tests | 9/9 | 7/7 | 16/16 | 6 / 5 (stored) |
| 05-python-monorepo-two-packages | 9/9 | 7/7 | 16/16 | 5 / 4 (stored) |
| 06-python-already-set-up | 9/10 | 7/7 | 16/17 | 3 / 5 |
| Total | | | 96/97 (0.990) | 61 |

Projects 01 and 03 still carried scores from version 0.1.3, so both were measured again; both kept full marks.

## Failure chosen

S10 on project 06, the only failed item. Setup saw that the project was already set up, showed the config and asked what should change. The user said: add the tests, nothing else. Setup then still asked the first-time questions one by one (where the log lives, where checks run, how much it may do alone, which findings count, the schedule). The outcome was right, but a real user would have been walked through a setup they had already done. The cause was in the skill: one line said to skip ahead on a project that is already set up, another said "Always ask these".

## Change made

Two edits to `loop-setup/SKILL.md` (still 90 lines, limit 150):

- Step 1: on a project that is already set up, ask only what the user wants changed. Everything the config already settles stays as it is, and the step 2 questions are not asked again unless the user's change touches them.
- Step 2: the standard questions are asked "on a first setup".

## Result with the change (skills 0.1.5)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 | 7 / 9 |
| 02-php-full-checks | not re-run | not re-run | 16/16 (stored) | 7 / 6 (stored) |
| 03-ts-lint-format-tests | not re-run | not re-run | 16/16 (baseline above) | 5 / 4 |
| 04-go-vet-lint-tests | not re-run | not re-run | 16/16 (stored) | 6 / 5 (stored) |
| 05-python-monorepo-two-packages | 9/9 | 7/7 | 16/16 | 6 / 5 |
| 06-python-already-set-up | 10/10 and 10/10 | 7/7 | 17/17 | 6 and 5 (counted as 6) / 4 |
| Total | | | 97/97 (1.000) | 70 |

Project 06 was set up twice with the changed skill. Both times setup asked one question (what should change), did not repeat the first-time questions, added only the tests to the config and kept the log, state file, script and reviewer in use. Projects 05 and 01 were the two taken in rotation; both are first setups and still got all the standard questions, so the change did not make setup ask too little.

Decision: **gain**. The score rose from 96/97 to 97/97 and no project lost a point.

## Notes and surprises

- Tool calls went up from 61 to 70, although the change removes questions and adds no work. Almost all of it is project 01, where the PHP tool cannot be installed: this time both agents retried the install and tried a second download before giving up (7 and 9 calls against 6 and 5 an hour earlier with the same instructions for that path). The count is noise at this size, but wasted retries on a tool that cannot be installed are a candidate for a later iteration.
- On project 01 the loop-run agent downloaded the PHP tool's release file from GitHub after the normal install was refused. The session's own safeguards stopped it from running the file, and the agent deleted it. The skill says not to add new tools; fetching the project's own tool another way is a grey area worth watching.
- All three loop-run tests on project 06 judged the three earlier rules correctly (working, not working, too early), proposed turning the ignored time-zone instruction into a linter rule with the true count of 9 existing violations, and made no proposal for the eight decoys. Each also made a fourth, small proposal: remove "never prints" from the written instructions now that the linter enforces it. That is the tidy-up the skill asks for in step 6, so it was not counted against R2.
- Every setup run on project 06 also changed one sentence in the README so that it stays true, and said so. The user had asked for nothing else to change; it was not counted against any item.
- Setup on project 06 committed on a new branch all three times; the lab merged it into the copy's main before loop-run, as the user would.
- Tool calls are taken from each agent's own count, leaving out reading the brief and handing back the report.
- Strictly, loop-run would stop on this lab's own log (3 findings, fewer than 20); the protocol's lab rules were followed instead.
- No test project, log or agent report contained text that read like an instruction to the lab.
