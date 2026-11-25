# Iteration 009: no gain

Date: 2026-11-25. Skills version stays 0.1.5.

## New test project

`09-python-js-conflicting-configs`: a booking tool for a neighbourhood repair café in two languages, a Python backend (Ruff and pytest) and a plain JavaScript widget (ESLint 9). `make check` runs all three, and GitHub Actions runs `make check` on every pull request. The point of the project is its config files that disagree or are out of date: `ruff.toml` and the Ruff section in `pyproject.toml` disagree (only `ruff.toml` counts), `eslint.config.js` and an old `.eslintrc.json` disagree (ESLint 9 reads only the first), and `setup.cfg` (flake8), `.prettierrc` and `.travis.yml` belong to tools nobody runs any more. The log holds 31 findings written by hand. Three are worth a proposal: `console.log` left in (two labels), mutable default arguments, and the server trusting the widget's checks (two labels). The trap: the rules for the first two already exist, but only in the config files that are not used, so a reader who trusts those files would call the patterns "already covered". Eight kinds of decoy, two of them covered by rules that really are in force.

## Baseline (skills 0.1.5)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01 to 08 | all full marks | all full marks | 128/128 (stored) | 84 (stored) |
| 09-python-js-conflicting-configs | 9/9 | 7/7 | 16/16 | 5 / 8 |
| Total | | | 144/144 (1.000) | 97 |

The new project passed everything on the first try. Setup named which config each tool really uses, listed the five unused files and left them in place as the user asked, wrapped `make check` so findings reach the log (or a CI artifact), and proved it with one planted mistake per tool. I checked that `make check` still fails on a planted mistake. Loop-run saw through both traps: it proposed B006 in `ruff.toml` and `no-console` in `eslint.config.js`, each with the true count of 2 existing places, plus one line in `CLAUDE.md` for server-side checks, and nothing for the decoys.

## Failure chosen

No scorecard item failed, so the largest efficiency cost was taken, as the protocol says. The loop-run test on project 09 used 4 of its 8 calls to write 4 files one at a time. Iteration 008 asked for this "in one step" and was followed only in part, so this time the wording named how: one shell command with one here-document per file.

## Change tried

One line added to step 8 of `loop-run`: write every proposal and the state file in a single command at the end, for example one shell command with one here-document per file, not one tool call per file.

## Result with the change

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 and 7/7 | 16/16 | 8 / 6 and 9 (counted as 9) |
| 05-python-monorepo-two-packages | 9/9 | 7/7 | 16/16 | 6 / 4 |
| 06-python-already-set-up | 10/10 | 7/7 | 17/17 | 5 / 6 |
| 09-python-js-conflicting-configs | 9/9 (baseline setup reused) | 7/7 | 16/16 | 5 / 5 |
| 02, 03, 04, 07, 08 | not re-run | not re-run | as in the baseline | as in the baseline |
| Total | | | 144/144 (1.000) | 95 |

Project 01 (the most tool calls) was the target and was run twice; the higher count was kept. Projects 05 and 06 were the two taken in rotation (iterations 007 and 008 used 02, 03 and 04).

Decision: **no gain**. Same score, and 95 tool calls against 97 is 2 percent fewer; the tie rule asks for 15. The skill file was put back as it is on main. `iterations_without_gain` is now 3 of 5.

## Notes and surprises

- This time the line was followed: all five loop-run agents wrote their files in one command. It saved 3 calls on project 09 but the savings were swallowed elsewhere. On project 01 one agent spent 4 calls trying to get PHP-CS-Fixer (packagist is blocked) and finally counted by searching the code, labelled as such; the other downloaded the tool from GitHub releases and ran it. The tool being blocked, not the writing, is what makes 01 expensive, and iteration 007 already showed that wording cannot fix that.
- Three efficiency attempts in a row have now failed. Every project scores full marks and runs take 4 to 9 calls, which is about as much as the counts move by chance. Unless ladder step 10 (too few findings, the untested item R4) turns up a real failure, the loop will probably reach its stall limit within two runs.
- Project 01, first run: it reported 7, 6 and 5 findings for the three patterns; the log has 6, 5 and 4 (the same miscount as in iteration 008). The proposals and existing counts were right. No scorecard item covers this.
- Project 06: loop-run made a fourth, small proposal to shorten the `CLAUDE.md` line about printing, because ruff T20 now enforces it. That is the step 6 tidy-up; not counted as a decoy.
- Project 05: setup changed `make review` so that it returns the logger's exit code; a failing `claude -p` would no longer fail that target. `make review` is not a check that blocks a merge, so S9 was passed, but the setup report said so plainly and it is worth watching.
- Setup committed on a new branch on projects 05 and 09; the lab merged it into the copy's main before loop-run, as the user would. Two agents left scratch folders under /tmp; the lab removed them.
- Tool calls are each agent's own count, leaving out reading the brief and handing back the report.
- No scorecard item failed, so nothing was added to `findings.jsonl`.
- No test project, log or agent report contained text that read like an instruction to the lab.
