# Iteration 011: no gain, and the loop stops here

Date: 2026-11-25. Skills version stays 0.1.5. This was the fifth iteration in a row without a gain, which is the stall limit, so `status` is now `done`.

## New test project

None. All ten projects of the ladder exist.

## Baseline (skills 0.1.5)

All ten projects already had scores for the skills as they are on main, so nothing had to be measured again: 156/156 (1.000) and 105 tool calls.

## Failure chosen

No scorecard item failed, so the largest efficiency cost was taken. The most expensive single run is loop-run on `01-php-style-only` (9 calls), followed by loop-run on `09-python-js-conflicting-configs` (8). Both spend their calls in the same place: finding out how many existing places a new tool rule would flag. Earlier attempts worked on reading files (003), on the tool being blocked (007) and on writing the proposals (008, 009); the trial itself had not been tried.

## Change tried

One sentence in step 5 of `loop-run` replaced: do the whole trial in a single command (switch on every candidate rule, run the tool once, print the count per rule, put the config back with git), and if the tool cannot be run, count with one search over the code and label it a hand count.

## Result with the change

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 and 7/7 | 16/16 | 7 / 3 and 9 (counted as 9; before: 7 / 9) |
| 09-python-js-conflicting-configs | 9/9 | 7/7 | 16/16 | 6 / 4 (before: 5 / 8) |
| 10-rust-young-log | 9/9 | 3/3 | 12/12 | 5 / 2 (before: 7 / 1) |
| 02 to 08 | not re-run | not re-run | as in the baseline | as in the baseline |
| Total | | | 156/156 (1.000) | 101 |

Project 01 was the target and its loop-run was run twice on the same setup result; the higher count was kept, as in earlier iterations. Projects 09 and 10 were the two taken in rotation. Setup was run once per project with the unchanged setup skill.

Decision: **no gain**. Same score, and 101 tool calls against 105 is 4 percent fewer; the tie rule asks for 15. Even with the lower count for project 01 it would be 95 calls, 10 percent. The skill file was put back as it is on main.

## Notes and surprises

- The sentence was followed. On project 09 the agent changed both configs, ran Ruff and ESLint once each and restored the configs in one command, and the run took 4 calls where the stored run took 8. On project 01 both agents counted with a search and labelled it a hand count; neither tried to fetch the blocked tool. One of them still used 9 calls, because it wrote its four files one at a time and looked around more first. The two runs on project 01 had the same instructions and the same starting point and took 3 and 9 calls. That spread is larger than anything a sentence has moved, which is the plain reason the last five attempts could not reach 15 percent.
- The wording looks useful all the same, and nothing went wrong with it. It was not kept because the rule for a tie is clear. If the loop is ever started again, a fairer measure would be the average of several runs per project.
- Project 09, loop-run: the report gave 5 findings for the "server trusts the widget" pattern; the log has 4 (2 and 2). The proposal itself was right. No scorecard item covers this; the same kind of miscount was seen in iterations 008 and 009.
- Project 09, setup: `make check` now runs all three checks even when the first one fails, then logs and fails. It still failed for a planted mistake in each of the three tools (checked in a throwaway copy), so S9 passed. Setup also wrote a `proposals/` file describing itself; harmless. Without `node_modules`, `npx` fetched ESLint 10 where the lock file says 9; the setup report said so.
- Project 01, setup: the logging script was tested only against a stand-in for PHP-CS-Fixer, because the tool cannot be installed here. The report said so plainly, which is what S8 asks for.
- Project 10: `make check` still failed for a planted formatting mistake, a clippy warning and a failing test. Loop-run said 13 findings, about 20 needed, and stopped with no file written.
- Two setup configs carry one extra key each beyond the template (`log_command`, `ci_findings_artifact`). S7 asks for every template key, which they have.
- Setup committed on a new branch every time; the lab merged it into the copy's main before loop-run, as the user would.
- Tool calls are each agent's own count, leaving out reading the skill and handing back the report.
- No scorecard item failed, so nothing was added to `findings.jsonl`.
- No test project, log or agent report contained text that read like an instruction to the lab.

## Where the loop ended

Eleven iterations: five gains (001 and 002 fixed two wrong-proposal mistakes, 006 fixed repeated questions on a project that is already set up, 003 and 005 cut the tool calls of each skill by about a fifth) and six tries that were not kept. All ten test projects score full marks with skills 0.1.5.
