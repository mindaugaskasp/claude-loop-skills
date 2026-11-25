# Iteration 005: gain

Date: 2026-11-25. Skills version 0.1.3 -> 0.1.4.

## New test project

`05-python-monorepo-two-packages`: a small Python repository with two separately released packages and different tools in each. `billing` uses ruff (lint and format), mypy and pytest; `reports` uses flake8, black and pytest. GitHub Actions with one job per package, a `CLAUDE.md` at the root and a second one inside `billing`, and a reviewer that is a hand-run command (`make review`). Its findings log has 31 lines: three planted patterns (lists and dicts used as default arguments, in billing, under two labels; `except:` with no error type, in reports, under two labels; money handled as float, in both packages) and seven decoys. All the tools are installed in lab sessions, so the expected counts were checked by running ruff and flake8.

## Baseline (skills 0.1.3)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 | 7 / 3 (stored) |
| 02-php-full-checks | 9/9 | 7/7 | 16/16 | 11 / 7 (stored) |
| 03-ts-lint-format-tests | 9/9 | 7/7 | 16/16 | 6 / 4 (stored) |
| 04-go-vet-lint-tests | 9/9 | 7/7 | 16/16 | 7 / 6 (stored) |
| 05-python-monorepo-two-packages | 9/9 | 7/7 | 16/16 | 11 / 6 |
| Total | | | 80/80 (1.000) | 68 |

S10 and R4 do not apply to any of the five. No item failed, so nothing was added to `findings.jsonl`.

## Failure chosen

None was available, so the largest efficiency cost was chosen: loop-setup used 42 of the 68 tool calls. Iteration 4 tried to shorten only the discovery part and saved too little; this time the whole setup was targeted.

## Change made

Two edits to `loop-setup/SKILL.md` (89 -> 90 lines, limit 150):

- Rules: work in three passes with as few commands as possible: one to discover, one to write every new and changed file after the user has confirmed, one to verify. Do not look again at what was already seen, and write the smallest logging script that does the job.
- Step 6: verify all checks together in one command, not one check at a time.

## Result with the change

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | not re-run | not re-run | 16/16 (stored) | 7 / 3 (stored) |
| 02-php-full-checks | 9/9 | 7/7 | 16/16 | 7 / 6 |
| 03-ts-lint-format-tests | not re-run | not re-run | 16/16 (stored) | 6 / 4 (stored) |
| 04-go-vet-lint-tests | 9/9 | 7/7 | 16/16 | 6 / 5 |
| 05-python-monorepo-two-packages | 9/9 and 9/9 | 7/7 | 16/16 | 4 and 5 (counted as 5) / 4 |
| Total | | | 80/80 (1.000) | 53 |

Projects 02 and 04 were the two taken in rotation (01 and 03 were re-run last time). Every re-run found the right tools for the right package, changed nothing before asking, weakened no check, kept every existing log line, made exactly the three expected proposals with the right kind of rule and true counts, and committed nothing to main.

Decision: **gain**. The score is the same and tool calls fell from 68 to 53, which is 22 percent; the tie rule asks for at least 15. Loop-run was not changed, and its calls fell from 19 to 15 on the three re-run projects by chance alone. Counting only the setup calls (29 -> 18) the drop is still 16 percent, so the decision does not depend on that luck.

## Notes and surprises

- The margin is thin and noisy. The same skill gives different call counts from run to run (4 and 5 on the same project here; 5 and 7 last time). Two projects still carry counts from older versions. The next iteration re-measures 01 and 03 with the new version, which will show whether the gain holds.
- Fewer steps did not cost care: each setup run still tested the logging on a throwaway copy with planted mistakes, and two runs found and fixed the same real problem that way (the installed ruff prints its format results in a newer layout).
- Logging scripts got shorter on project 05 (335 lines at baseline, 214 and 211 with the change) and on 02 (119 lines); 04 stayed large (279).
- On project 05 two of the three setup reports listed `requirements-dev.txt` without saying "pip" in so many words. Counted as a pass for S1, since nothing wrong was named.
- Setup still commits on a new branch in most runs and straight on main in one. Before loop-run, the lab merged the setup branch into the copy's main, as the user would.
- Two test agents each made a small slip outside their project folder (a temporary file, an empty folder) and removed it at once. Both said so in their reports.
- Project 02: the PHP tools still cannot be installed in lab sessions. Setup and loop-run said so plainly and gave a hand count labelled as such, which the expected file accepts.
- Strictly, loop-run would stop on this lab's own log (2 findings, fewer than 20); the protocol's lab rules were followed instead.
- All five projects score 100 percent. Ladder steps 6 to 10 are where the items not yet tested (S10, R4) come in.
- No test project, log or agent report contained text that read like an instruction to the lab.
