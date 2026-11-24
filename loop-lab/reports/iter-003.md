# Iteration 003: gain

Date: 2026-11-24. Skills version 0.1.2 -> 0.1.3.

## New test project

`03-ts-lint-format-tests`: a small TypeScript parcel price service with a linter (ESLint with typescript-eslint), a formatter (Prettier), tests (Vitest) and a type check, GitHub Actions, no agent instruction file and no automated reviewer (teammates review pull requests). Its findings log has 33 lines: three planted patterns (console output left in, under two labels; a promise nobody waited for, under two labels; helpers written again although they exist) and seven decoys. This is the first project whose tools could really be installed and run, so the expected counts were checked by running ESLint.

## Baseline (skills 0.1.2)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 | 9 / 5 (stored) |
| 02-php-full-checks | 9/9 | 7/7 | 16/16 | 9 / 11 (stored) |
| 03-ts-lint-format-tests | 9/9 | 7/7 | 16/16 | 6 / 11 |
| Total | | | 48/48 (1.000) | 51 |

S10 and R4 do not apply to any of the three. No item failed, so nothing was added to `findings.jsonl`.

## Failure chosen

None was available. The protocol then asks for the largest efficiency cost. Loop-run used more tool calls (27 across the projects) than loop-setup (24). On the new project it used 11: it read its inputs one by one, tried each tool rule in its own run, and then ran all of the project's checks again to prove each proposal.

## Change

Three additions to `loop-run/SKILL.md` (69 -> 72 lines, limit 150):

- Step 1: read the config, the log and the state file together in one step.
- Step 5: when several tool rules are candidates, switch them all on for one trial run, read the count per rule from that output, then undo the trial.
- Rules: keep the run short, do not look again at what was already seen, and do not run the project's other checks to prove a proposal; the pull request's own checks do that.

## Result (skills 0.1.3)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 | 7 / 3 |
| 02-php-full-checks | 9/9 | 7/7 | 16/16 | 11 / 7 |
| 03-ts-lint-format-tests | 9/9 (not re-run) | 7/7 and 7/7 | 16/16 | 6 / 4 and 4 |
| Total | | | 48/48 (1.000) | 38 |

Every re-run made exactly the three expected proposals with the right kind of rule and correct counts, proposed nothing for a decoy, committed nothing, and wrote the state file. Loop-run calls fell from 27 to 14; all calls from 51 to 38, which is 25 percent fewer (the tie rule asks for at least 15 percent).

Decision: **gain**, by the tie rule: same score, clearly fewer tool calls.

## Notes and surprises

- How solid is this? The fair comparison is project 03: same session, same way of counting, 11 calls before and 4 and 4 after. The earlier numbers for 01 and 02 come from older sessions, and iteration 2 saw the same skill vary from 5 to 13 calls. So the direction is trustworthy; the exact 25 percent is not.
- Calls are counted by the session's own counter, minus the one call used to read the skill text. Agents' own counts differed by one or two.
- Fewer calls partly means bigger calls: one agent wrote all proposals and the state file in a single command. That is what the scorecard measures, but it is not the same as less work. Tokens used per run fell less (about 87 thousand to about 69 thousand on project 03).
- A cost of the change: proposals are no longer tried against the full set of checks before being written. One re-run said so itself ("I did not run the tests against it"). On a real project the pull request's own checks cover this; in a project without CI, nothing does. Worth watching.
- Setup was not changed. It was run again on 01 and 02 only to rebuild their after-setup state (nothing is kept between sessions); both still looked correct. Their setup calls in the table are from these runs.
- Setup again wrote large logging scripts: 143, 245 and 605 lines. Still no check got weaker, but "the lightest option that works" keeps being read generously. The best candidate for the next iteration if no item fails.
- On project 03 setup committed on a new branch; on 01 and 02 the lab told it to commit on main. The skill itself still only says "commit it".
- PHP packages are still blocked in lab sessions; npm packages are not.
- Three agents left small scratch files outside the project folder (a trial output, a trial test). Nothing in the repository was touched.
- No test project, log or agent report contained text that read like an instruction to the lab.
