# Iteration 001: gain

Date: 2026-11-24. Skills version 0.1.0 -> 0.1.1.

## New test project

`01-php-style-only`: a small PHP invoicing library with one code-style tool (PHP-CS-Fixer), no CI, no agent instructions and no automated reviewer. Its findings log has 28 lines: three planted patterns (missing strict types under two different labels, loose comparison, floats used for money) and five decoys.

## Baseline (skills 0.1.0)

| Project | Setup | Run | Total | Tool calls (setup / run) |
|---|---|---|---|---|
| 01-php-style-only | 9/9 | 6/7 | 15/16 | 8 / 8 |

S10 and R4 do not apply to this project.

The one failed item was R3. For the "floats used for money" pattern, no rule in the style tool can express the fix and the project has no test tool, so the strongest fitting fix is one line of instruction for the coding agent. The skill instead proposed a home-made script that bans every float and every division in the source folder, and called it a machine rule. The cause is the wording "or a new test" in step 5 of loop-run, which invites adding a new check tool to a project that has none.

## Change

One sentence in step 5 of `loop-run/SKILL.md`: a new test counts as a machine rule only when a test tool is already listed in `checks`; do not add a new tool or a home-made check script to get a machine rule; otherwise go to the next option. The file stays at 69 lines (limit 150).

## Result (skills 0.1.1)

| Project | Setup | Run, first | Run, second | Total | Tool calls (run) |
|---|---|---|---|---|---|
| 01-php-style-only | 9/9 (not re-run) | 7/7 | 7/7 | 16/16 | 7 and 9 |

Both re-runs proposed the two style-tool rules and an instruction line for the money pattern, and made no proposal for any decoy. No point was lost.

Decision: **gain**. Total score 15/16 (0.938) -> 16/16 (1.000).

## Notes and surprises

- The setup skill was not changed, so its run was not repeated. Both re-runs of loop-run started from a saved copy of the project as it was right after the baseline setup. This keeps the comparison to the one thing that changed.
- The chosen failure was seen only once. The lab config asks for two repeats before a rule, but the protocol asks for one change per iteration aimed at the most costly failure, and the protocol decides. The fix was confirmed twice.
- The lab sessions cannot reach Packagist, so PHP-CS-Fixer could not be installed. Setup said so plainly and checked its logging script against a sample report (S8 passes on that basis). Loop-run counted existing violations by hand, labelled the counts as hand counts, and they matched the truth (3 files, 4 comparisons), so R8 passes. The expected file notes this limit. A direct download of the tool was tried once while building the project, was refused by the session's safety check, and was not retried.
- Whether a home-made check script is "stronger" than an instruction is a judgement call. The expected file was written before any run and said instruction, so the score follows it.
- With one project the score is now 100 percent. That says little; later projects on the ladder are harder.
- No test project, log or agent report contained text that read like an instruction to the lab.
- One re-run agent listed a folder outside the project once (Composer's settings folder) and read nothing there. Its first attempt to build patches by editing and reverting files was refused; it then built them without touching the project sources.
