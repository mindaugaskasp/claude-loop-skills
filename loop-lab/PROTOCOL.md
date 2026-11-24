# Loop lab protocol

This is the procedure for one iteration of improving the `loop-engineering` skills by running the improvement loop on the skills themselves. One scheduled session performs exactly one iteration and then ends. All memory between sessions lives in this repository.

This file is fixed. An iteration must not edit it, `SCORECARD.md`, or the expected file of any project that already exists on main.

## What an iteration may change

- `plugins/loop-engineering/skills/**` (the thing being improved)
- `plugins/loop-engineering/.claude-plugin/plugin.json` (version number only)
- `loop-lab/state.json`, `loop-lab/findings.jsonl`, `loop-lab/reports/**`
- New folders under `loop-lab/projects/` and new files under `loop-lab/expected/`

Nothing else.

## Step 0: Decide whether to run

1. Clone the repository and read `loop-lab/state.json` on main.
2. If `status` is not `running`, do nothing. Try to delete the scheduled task that started this session; if that is not possible, say so in the final message. End.
3. If an open pull request exists from a branch named `loop/iter-*` that was created less than 2 hours ago, another iteration is still in progress. End.
4. If such a pull request is older than 2 hours, close it, count it as a failed run (step 9), and continue.

Create branch `loop/iter-NNN` from main, where NNN is `iteration + 1` padded to three digits.

## Step 1: Add one test project (while fewer than `max_projects` exist)

Add the next project on this ladder. Each is a small but realistic skeleton: real config files, a few source files, git initialised when the test agent receives it.

1. PHP, one code-style tool, no CI, no agent instructions.
2. PHP with static analysis, code style and tests, GitHub Actions, a CLAUDE.md, an AI reviewer subagent.
3. TypeScript with a linter, formatter and tests, GitHub Actions.
4. Go with vet, a linter and tests, GitLab CI.
5. Python monorepo with two packages and different tools in each.
6. A project that already contains a valid `.improvement-loop.json` and a log with earlier rules in its state file.
7. A project with no checks at all.
8. A project whose only check is a home-made shell script reviewer.
9. A polyglot project (two languages) with conflicting or outdated config files.
10. A project whose findings log has fewer than 20 findings.

For each new project write, before running anything on it:

- `loop-lab/projects/<name>/` : the skeleton, including a findings log at the path its expected file names. The log contains planted repeated patterns and decoys (single findings, findings with `led_to_change` false, patterns already covered by a rule).
- `loop-lab/expected/<name>.json` : the truth for every scorecard item that applies, the planted patterns with the strongest possible kind of rule for each, the decoys, and `scripted_answers`, the answers a user would give to the questions loop-setup asks.

## Step 2: Measure the baseline

For every project that has no entry in `project_scores` for the current main commit of the skills (always the new project; all projects if the stored scores are from an older skill version), run a test:

1. Copy the project to a temporary folder outside the repository. The expected file must not be copied and must not be mentioned to the test agent.
2. Start a fresh agent that has not seen this protocol's expected files. Give it: the path to the copy, the full text of the skill to run, and the scripted answers as "the user's answers when you ask". Tell it to treat pull requests as written proposals in a `proposals/` folder, because the test project has no remote. Ask it to finish with a plain report of what it found, asked, changed and proposed, and how many tool calls it used.
3. Run `loop-setup` first, then `loop-run` in a second fresh agent on the result.
4. Score the outcome against the expected file using `SCORECARD.md`. Score from the files the agent produced, not only from its report.

Write every failed item to `loop-lab/findings.jsonl` as one JSON line:

`{"ts": "...", "iteration": N, "source": "scorecard", "category": "<item id>-<short-label>", "project": "<name>", "summary": "what went wrong, one sentence", "led_to_change": null}`

## Step 3: Run the improvement loop on the skills

Follow `plugins/loop-engineering/skills/loop-run/SKILL.md` with this repository as the project, using `.improvement-loop.json` at the repository root. In this lab:

- The findings log is `loop-lab/findings.jsonl`.
- "Machine rule" means nothing here; the scorecard is fixed. A fix is a change to the wording or steps of a skill file.
- Choose one change per iteration: the failure pattern that costs the most points, counting repeats across projects and earlier iterations. If two cost the same, take the older one.
- If the skill files have no failing items left, choose the largest efficiency cost instead (E1, E2).
- Keep each skill file within `instruction_max_lines`. A change that adds lines must remove lines elsewhere once the file is over the limit.
- Do not write project-specific special cases into a skill (for example naming a test project or its exact file layout). The fix must be a general instruction.

## Step 4: Measure the change

Re-run the tests with the changed skill on: every project that had a failing item, the new project, and two other projects chosen in rotation. For the item the change targeted, run the affected project twice; the item counts as fixed only if it passes both times.

The change is a gain when the total score is higher than the baseline and no project lost a point it had before, or when the score is equal and the tie rule in `SCORECARD.md` is met.

## Step 5: Record

Write `loop-lab/reports/iter-NNN.md`: the failure chosen, the change made, baseline and new scores per project, the decision, and anything surprising. Keep it under 60 lines.

Update `loop-lab/state.json`:

- `iteration` plus 1.
- Gain: store the new `project_scores` and `total_score`, set `iterations_without_gain` to 0, set `led_to_change` true on the findings the change fixed, and raise the patch number of the plugin version.
- No gain: restore the skill files to their state on main (keep the new project, findings and report), and add 1 to `iterations_without_gain`.
- Append `{iteration, date, change, baseline, result, decision}` to `history`.
- Set `consecutive_failed_runs` to 0.
- Set `status` to `done` if `iteration` reached `max_iterations` or `iterations_without_gain` reached `stall_limit`.

## Step 6: Validate

Run `claude plugin validate .` if the command is available. If it fails, fix the cause; if it cannot be fixed, treat the iteration as no gain.

## Step 7: Pull request and merge

Commit, push the branch and open a pull request titled `Loop iteration NNN: <gain or no gain> - <one line>`, with the report as its description. Merge it. Every iteration's pull request is merged, because it carries the records; the skill change is inside it only when it was a gain.

## Step 8: Finish

End with a three-line summary: the iteration number, the decision with scores, and whether the loop is still running. If `status` became `done`, add a short overall summary of the history and try to delete the scheduled task.

## Step 9: If the run fails

If the iteration cannot be completed (no access, agents cannot be started, merge refused), do not leave half-finished skill changes on main. If it is possible to commit to the repository, add 1 to `consecutive_failed_runs` through a small pull request and set `status` to `halted` when it reaches `failed_run_limit`. Say plainly in the final message what blocked the run.
