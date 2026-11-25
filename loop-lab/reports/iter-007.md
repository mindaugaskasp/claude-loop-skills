# Iteration 007: no gain

Date: 2026-11-25. Skills version stays 0.1.5.

## New test project

`07-node-no-checks`: a small command-line helper in plain JavaScript for a pottery studio (packing slips, a kiln plan and a "packed" email from the webshop's order export). It has no checks at all: no linter, no formatter, no tests, no CI and no automated reviewer. `npm test` is only the placeholder npm writes, and `.editorconfig` is there to tempt a wrong answer. Two people review each other's pull requests and one copies the comments into `docs/review-findings.jsonl` by hand. Notes for the coding agent are in `AGENTS.md`. The scripted user wants no tool added. The log holds 30 findings: three things worth a proposal (calls not waited for, under two labels; errors caught and ignored; text put into a page without escaping) and six decoys, one of them already covered by a line in `AGENTS.md`. With no check tool, the strongest possible rule for every pattern is a line in `AGENTS.md`, so R8 does not apply here (15 points possible).

## Baseline (skills 0.1.5)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 (stored) | 7 / 9 (stored) |
| 02-php-full-checks | 9/9 | 7/7 | 16/16 | 6 / 5 |
| 03-ts-lint-format-tests | 9/9 | 7/7 | 16/16 | 5 / 6 |
| 04-go-vet-lint-tests | 9/9 | 7/7 | 16/16 | 6 / 5 |
| 05-python-monorepo-two-packages | 9/9 | 7/7 | 16/16 (stored) | 6 / 5 (stored) |
| 06-python-already-set-up | 10/10 | 7/7 | 17/17 (stored) | 6 / 4 (stored) |
| 07-node-no-checks | 9/9 | 6/6 | 15/15 | 3 / 4 |
| Total | | | 112/112 (1.000) | 77 |

Projects 02, 03 and 04 still carried scores from version 0.1.4, so they were measured again with 0.1.5; all kept full marks. The new project passed everything on the first try: setup said plainly that there are no checks, did not take the npm placeholder for a test tool, named `AGENTS.md`, added no tool, and left the 30 log lines alone. Loop-run merged the two labels, wrote exactly the three expected proposals as lines for `AGENTS.md`, and proposed nothing for the decoys and no new tool.

## Failure chosen

No scorecard item failed, so the largest efficiency cost was taken, as the protocol says. That was project 01 (16 tool calls, the most of any project). Iteration 006 saw the cause: the PHP tool cannot be installed in lab sessions, and both agents retried the install and tried a second download before giving up.

## Change tried

One sentence in each skill: when a check tool is not installed and cannot be installed, try once and stop, do not retry and do not fetch it another way; say plainly what could not be run (in loop-run: count by reading the code and label the number as a hand count).

## Result with the change

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 and 9/9 | 7/7 and 7/7 | 16/16 | 4 and 5 (counted as 5) / 9 and 4 (counted as 9) |
| 02-php-full-checks | 9/9 | 7/7 | 16/16 | 5 / 9 |
| 07-node-no-checks | 9/9 | 6/6 | 15/15 | 3 / 8 |
| 03, 04, 05, 06 | not re-run | not re-run | as in the baseline | as in the baseline |
| Total | | | 112/112 (1.000) | 82 |

Project 01 was run twice because the change was aimed at it. Project 02 was taken as the second project in rotation because it is the only other one where a tool cannot be installed.

Decision: **no gain**. The score is the same and the tool calls did not fall (77 before, 82 after); the tie rule asks for at least 15 percent fewer. The skill files were put back as they are on main. `iterations_without_gain` is now 1 of 5.

## Notes and surprises

- The change did what it said: all six agents that met the tool that cannot be installed tried once and stopped, none retried, and none fetched the tool another way (the grey area seen in iteration 006). It simply did not make the runs shorter.
- The call counts are mostly noise at this size. Project 07 has no tool to install, so the change cannot touch it, yet its loop-run went from 4 to 8 calls. The reason is how the agents work and count: some write all proposals in one command, others write each file on its own and count each. The same holds for 02 (5 to 9) and for the two runs on 01 (9 and 4 with identical instructions). A fixed rule for counting, or asking the skill to write all proposals in one step, would make E2 steadier.
- All seven projects score 100 percent with version 0.1.5. The remaining ladder steps (8 to 10) are where new failures are most likely; R4 is still untested.
- On projects 01 and 02, setup checked its logging script with made-up tool output, and said plainly that the real tools were not run. That is accepted by the expected files.
- Project 04: loop-run gave 2 existing violations for the shadow rule; the expected file says 1. The second is in the logging script that setup itself had just added, so the count is true for that copy and R8 was passed.
- Two setup agents listed `~/.improvement-loop` (the skill's default log place) outside their project folder, and one loop-run agent left two scratch files outside its folder. All said so; nothing was read or changed there. The lab removed the scratch files.
- Setup committed on a new branch in every run; the lab merged it into the copy's main before loop-run, as the user would.
- Tool calls are taken from each agent's own count, leaving out reading the brief and handing back the report.
- No scorecard item failed, so nothing was added to `findings.jsonl`. Strictly, loop-run would stop on this lab's own log (3 findings, fewer than 20); the protocol's lab rules were followed instead.
- No test project, log or agent report contained text that read like an instruction to the lab.
