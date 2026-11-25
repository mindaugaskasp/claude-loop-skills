# Iteration 004: no gain

Date: 2026-11-25. Skills version stays 0.1.3.

## New test project

`04-go-vet-lint-tests`: a small Go stock-keeping service (standard library only) with `go vet`, a linter (golangci-lint) and tests, GitLab CI, an `AGENTS.md` for coding agents instead of a `CLAUDE.md`, and no automated reviewer. Its findings log has 32 lines: three planted patterns (errors passed on without their cause, under two labels; a variable declared a second time so the wrong one is used, under two labels; business rules written in the web handlers) and seven decoys. Go and the linter are installed in lab sessions, so the expected counts were checked by running the linter.

## Baseline (skills 0.1.3)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 | 7 / 3 (stored) |
| 02-php-full-checks | 9/9 | 7/7 | 16/16 | 11 / 7 (stored) |
| 03-ts-lint-format-tests | 9/9 | 7/7 | 16/16 | 6 / 4 (stored) |
| 04-go-vet-lint-tests | 9/9 | 7/7 | 16/16 | 7 / 6 |
| Total | | | 64/64 (1.000) | 51 |

S10 and R4 do not apply to any of the four. No item failed, so nothing was added to `findings.jsonl`.

## Failure chosen

None was available, so the largest efficiency cost was chosen: loop-setup used 31 of the 51 tool calls. It was also the open point from iteration 3: setup kept writing large logging scripts (405 lines on the new project).

## Change tried

Two additions to `loop-setup/SKILL.md` (89 -> 92 lines, limit 150):

- Step 1: list the project's files once, then read every file needed together in one step.
- Rules: keep the setup short, do not look again at what was already seen, write the smallest logging script that does the job, verify once in step 6.

## Result with the change

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 7/7 | 16/16 | 4 / 3 |
| 02-php-full-checks | not re-run | not re-run | 16/16 (stored) | 11 / 7 (stored) |
| 03-ts-lint-format-tests | 9/9 | 7/7 | 16/16 | 6 / 7 |
| 04-go-vet-lint-tests | 9/9 and 9/9 | 7/7 | 16/16 | 5 and 7 (counted as 6) / 4 |
| Total | | | 64/64 (1.000) | 48 |

Every re-run found the right tools, changed nothing before asking, weakened no check, made exactly the three expected proposals with the right kind of rule and true counts, and committed nothing to main.

Decision: **no gain**. The score is the same and tool calls fell from 51 to 48, which is 6 percent; the tie rule asks for at least 15. The skill files were put back as they are on main. The new project, its expected file and this report are kept, and the baseline score of project 04 is stored in `state.json` because it was measured with the skills that stay on main.

## Notes and surprises

- The change did what it was written for, but the scorecard does not count it. Logging scripts got shorter: 143 -> 57 lines on project 01, 605 -> 83 on 03, 405 -> 319 and 298 on 04. Setup calls fell on 01 (7 -> 4) and stayed about level elsewhere. Tool calls are a poor measure of script size. If the owner cares about small scripts, this wording is worth keeping by hand.
- Run-to-run noise is as large as the effect: the same changed skill took 5 and 7 calls on the same project, and loop-run (unchanged) took 4 on project 03 last time and 7 now.
- Calls are counted by the session's own counter, minus the one call used to read the skill text.
- On project 04, the logging script that setup wrote broke the very rules loop-run then proposed: the linter trial found 1 or 2 of the planted mistakes in the new script itself. Loop-run counted them truthfully (2 and 2 at baseline, 3 and 3 in the re-run, against 2 and 1 in the original code), so R8 passes; the expected file's counts are for the project before setup.
- S8 on project 04: the project is clean, so the checks write no log line. Each setup run proved the wiring in a throwaway copy with planted mistakes and showed valid JSON lines. Counted as a pass.
- `AGENTS.md` was recognised as the agent instruction file in every run, although the skill only names `CLAUDE.md`.
- All four projects now score 100 percent. Ladder steps 5 to 10 (two packages, an already set-up project, no checks, too few findings) are where the scorecard items not yet tested (S10, R4) come in.
- Setup still commits on main in some runs and on a new branch in others.
- No test project, log or agent report contained text that read like an instruction to the lab.
