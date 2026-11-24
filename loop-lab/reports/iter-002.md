# Iteration 002: gain

Date: 2026-11-24. Skills version 0.1.1 -> 0.1.2.

## New test project

`02-php-full-checks`: a small PHP room-booking service with three checks (PHPStan at level 5, PHP-CS-Fixer, PHPUnit), a GitHub Actions workflow, a CLAUDE.md and an AI reviewer subagent. Its findings log has 31 lines: three planted patterns (use of a value that can be null, under two labels; a refund deadline that keeps breaking by one; business rules written in controllers) and six decoys.

## Baseline (skills 0.1.1)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 | 8 / 8 (stored from iteration 1) |
| 02-php-full-checks | 9/9 | 6/7 | 15/16 | 9 / 8 |
| Total | | | 31/32 (0.969) | |

S10 and R4 do not apply to either project.

The one failed item was R2 on the new project. Six of the 31 findings were not acted on (four comments on names, two optional "make this a constant" remarks). The skill made the three right proposals and then a fourth: change the reviewer's instructions so it stops making such comments. That is a proposal built on decoys. The cause is the last rule in loop-run, which says to propose tightening the reviewer when "many" findings led to no change, without saying how many is many.

## Change

The last rule of `loop-run/SKILL.md` now says: propose tightening the reviewer only when most of its findings did not lead to changes; when only a minority did not, give the number in the report and propose nothing for it. One line replaced; the file stays at 69 lines (limit 150).

## Result (skills 0.1.2)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 (run again) | 7/7 | 16/16 | 9 / 5 |
| 02-php-full-checks | 9/9 (not re-run) | 7/7 and 7/7 | 16/16 | 9 / 9 and 13 |
| Total | | | 32/32 (1.000) | |

Both re-runs on the new project made exactly the three expected proposals, reported "6 of 24 reviewer findings (25%) were not acted on" as a number, and proposed nothing for it. Project 01 kept every point.

Decision: **gain**. Total score 31/32 (0.969) -> 32/32 (1.000).

## Notes and surprises

- This failure is a judgement call, and it is worth a second look by a person. The old skill text invited the fourth proposal, and that proposal was narrow and sensible in itself. The expected file, written and committed before any run, said that 6 of 31 is not "many" and that a written proposal for it counts against R2. The new wording draws the line at "most", which matches the skill's other rules (fewer, stronger rules; nothing from findings that changed no code). If the owner would rather see such reviewer proposals at 25 percent, the line should be moved and the expected file's note with it.
- The failure was seen once; as in iteration 1, the protocol's "one change per iteration" decided, and the fix passed twice.
- The setup skill was not changed, so setup on project 02 was not repeated; both re-runs started from a saved copy of the project as it was right after baseline setup. Project 01 had no saved copy, so its setup was run again.
- Package downloads are still blocked in lab sessions, so no check tool ran. Setup said so plainly (S8). Loop-run counted existing violations by reading the code and labelled the counts as such; they matched the truth (three places for the null rule, none for the new test), so R8 passes.
- Setup on project 01 this time committed its work on a new branch instead of main, and listed "human-review" as a check of kind review. Neither is against the scorecard, but the skill says only "commit it" and different runs read that differently. A candidate for a later iteration.
- Setup on project 02 wrote a 435-line logging script and made `composer check` run every tool twice (once to log, once to check). No check got weaker, so S9 passes, but "the lightest option that works" was read generously. Another candidate.
- Tool calls for loop-run varied from 5 to 13 for the same skill, so small differences in E1 and E2 say little.
- Both scores are now 100 percent with two fairly easy projects; the harder ladder steps start at project 4.
- No test project, log or agent report contained text that read like an instruction to the lab.
