# Iteration 008: no gain

Date: 2026-11-25. Skills version stays 0.1.5.

## New test project

`08-ruby-shell-script-reviewer`: a small command-line helper in plain Ruby for a street seed library (loans of seed packets, what is due back, reminder letters, a member import). Its only check is `scripts/review.sh`, a shell script the owner wrote herself. It searches the Ruby files for five kinds of mistake, prints one line per problem and fails when it finds any; she runs it by hand with `make review` before every merge. There are no tests, no linter and no CI. The log holds 30 findings she wrote down by hand. Three are worth a proposal: the time asked for directly instead of through the project's clock helper (under two labels), CSV columns read by number, and error messages that tell the user nothing. Six are decoys, two of them things the script already catches. The point of the project: the first two patterns can be turned into a new check inside the existing script, which is a rule in a listed tool and not a new home-made script, so the skill should choose that over a written instruction.

## Baseline (skills 0.1.5)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 (stored) | 7 / 9 (stored) |
| 02-php-full-checks | 9/9 | 7/7 | 16/16 (stored) | 6 / 5 (stored) |
| 03-ts-lint-format-tests | 9/9 | 7/7 | 16/16 (stored) | 5 / 6 (stored) |
| 04-go-vet-lint-tests | 9/9 | 7/7 | 16/16 (stored) | 6 / 5 (stored) |
| 05-python-monorepo-two-packages | 9/9 | 7/7 | 16/16 (stored) | 6 / 5 (stored) |
| 06-python-already-set-up | 10/10 | 7/7 | 17/17 (stored) | 6 / 4 (stored) |
| 07-node-no-checks | 9/9 | 6/6 | 15/15 (stored) | 3 / 4 (stored) |
| 08-ruby-shell-script-reviewer | 9/9 | 7/7 | 16/16 | 3 / 4 |
| Total | | | 128/128 (1.000) | 84 |

The new project passed everything on the first try. Setup named the script as the only check, wrapped it so that each run also writes its findings to the log, and proved it by really running `make review`: one new valid line, the script untouched, and the command still fails when something is found. Loop-run merged the two labels, proposed two new checks inside the script with the true counts (2 and 1 existing places) and one written line for the error messages, and made no proposal for the decoys.

## Failure chosen

No scorecard item failed, so the largest efficiency cost was taken, as the protocol says. Project 01 still has the most tool calls (16), and iteration 007 noted that loop-run agents differ mainly in whether they write their proposals in one go or one file at a time.

## Change tried

One sentence added to the rules of `loop-run`: prepare every pull request and the state file together in one step at the end, not one at a time.

## Result with the change

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 and 9/9 | 7/7 and 7/7 | 16/16 | 5 and 5 / 8 and 6 (counted as 8) |
| 03-ts-lint-format-tests | 9/9 | 7/7 | 16/16 | 4 / 6 |
| 04-go-vet-lint-tests | 9/9 | 7/7 | 16/16 | 9 / 6 |
| 08-ruby-shell-script-reviewer | 9/9 (baseline setup reused) | 7/7 | 16/16 | 3 / 4 |
| 02, 05, 06, 07 | not re-run | not re-run | as in the baseline | as in the baseline |
| Total | | | 128/128 (1.000) | 84 |

Project 01 was run twice because the change was aimed at it. Projects 03 and 04 were the two taken in rotation.

Decision: **no gain**. The score is the same and the tool calls are the same (84 before, 84 after); the tie rule asks for at least 15 percent fewer. The skill file was put back as it is on main. `iterations_without_gain` is now 2 of 5.

## Notes and surprises

- The sentence was followed only in part. Three of the five loop-run agents wrote everything in one step; one agent on project 01 still wrote four files one by one. Where it was followed it saved a call or two, and that was cancelled out by other steps taking more.
- Two efficiency attempts in a row have now ended in no gain. With every project at full marks and each run already at 3 to 9 calls, there is little left to save, and the counts move by more than that from one run to the next with identical instructions (setup on project 04: 6 calls an hour ago, 9 now). Ladder steps 9 and 10 are the remaining chance of a real failure to fix; R4 is still untested.
- Project 01, first run: the report gave 6 findings for loose comparison; the log has 5. The proposal itself and the count of existing places (4) were right. No scorecard item covers this.
- Project 01: the PHP tool still cannot be installed in lab sessions. All four agents tried once, said so plainly, and gave counts labelled as taken from reading the code.
- Project 04: setup also wrote a small proposal of its own (a line for `AGENTS.md` about recording check failures) and committed it on its branch. Loop-run left it alone. Loop-run gave 3 existing places for the shadow rule; the expected file says 1. The other two are in the logging program setup had just added, so the count is true for that copy.
- Project 08: both loop-run tests made a fourth, small proposal: delete the line in `CLAUDE.md` that the script already enforces. That is the tidy-up the skill asks for in step 6 and the expected file allows it.
- Setup committed on a new branch on projects 01 (one of two runs), 03 and 04; the lab merged it into the copy's main before loop-run, as the user would. One setup agent left a scratch folder outside its project; the lab removed it.
- Tool calls are taken from each agent's own count, leaving out reading the brief and handing back the report.
- No scorecard item failed, so nothing was added to `findings.jsonl`.
- No test project, log or agent report contained text that read like an instruction to the lab.
