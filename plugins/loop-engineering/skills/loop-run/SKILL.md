---
name: loop-run
description: Read a project's findings log, find repeated review and code-check findings, and propose permanent rules for them as pull requests. Use after loop-setup, on a schedule or on demand.
---

# Improvement loop: run

Goal: turn mistakes that keep recurring into rules that prevent them, and prove with numbers whether earlier rules worked.

## Step 1: Load

- Read `.improvement-loop.json` in the project root. If it is missing, stop and tell the user to run `loop-setup` first.
- Read the findings log at `log_path`. If it has fewer than about 20 findings, say so and stop; there is not enough data to find real patterns.
- Read the state file next to the log (`state.json`), if it exists. It records the date of the last run and the rules proposed so far with their categories.

## Step 2: Clean the data

- If `count_only_findings_that_led_to_change` is true, drop findings where `led_to_change` is false. For `null`, check git history for whether the flagged file changed on the same branch after the finding; if that cannot be determined, keep the finding but mark it uncertain.
- Merge category labels that mean the same thing. Tell the user which labels you merged.

## Step 3: Measure earlier rules

For every rule in the state file, compare how often its category appeared before the rule was merged and since. Report each as one of:

- Working: the category has dropped clearly.
- Not working: no real drop after at least two weeks. Propose rewording it or promoting it to a stronger kind of rule (see step 5).
- Too early: not enough time or data.

Also report the overall trend: findings per week, and average review rounds per change if the log allows it.

## Step 4: Find new patterns

Group the findings since the last run by category. A pattern qualifies when it appears at least `min_repeats_for_rule` times and no existing rule covers it. For each one, collect two or three real examples from the log.

## Step 5: Choose the strongest fix

For each pattern, go down this list and take the first option that is possible in this project:

1. Machine rule: a setting or rule in one of the tools listed in `checks`, or a new test. The mistake can then no longer be merged.
2. Coding-agent instruction: one short, specific line in `instruction_file`, with a concrete example of right and wrong.
3. Reviewer instruction: tell the reviewer to always check for this.

Before proposing a machine rule, run the tool with the new rule over the whole codebase and report how many existing violations it produces. If there are many, propose it with a baseline or scoped to new code, and say so.

## Step 6: Prune

- If a machine rule now covers something that is also written in `instruction_file`, propose deleting the written instruction.
- If `instruction_file` is over `instruction_max_lines`, propose which lines to cut, starting with rules whose category has not appeared in the log for a long time.

## Step 7: Deliver according to autonomy

- `propose` (default): open one pull request per rule change. Never commit rule changes to the main branch directly.
- `apply-low-risk`: code-style rule changes that produce no new violations, or only auto-fixable ones, may be applied directly. Everything else is still a pull request.

Each pull request description contains: the pattern, how many times it appeared, the examples, the proposed rule, why this kind of rule was chosen, and the number of existing violations it produces.

If `benchmark_tasks_path` is set, re-run those tasks with and without the change and include the comparison. If it is not set, say plainly that the change is untested and will be judged by the trend in the next runs.

## Step 8: Record and report

- Update the state file: run date, each proposed rule with its category, kind, and pull request link.
- Give the user a short report: trend numbers, the verdict on earlier rules, new proposals, and prune suggestions.

## Rules

- Never weaken or remove an existing check to make numbers look better.
- Never propose a rule from a single finding or from findings that did not lead to a code change.
- Prefer fewer, stronger rules. If nothing qualifies this run, report that and propose nothing.
- If the reviewer itself looks like the problem (many findings that did not lead to changes), say so and propose tightening the reviewer's instructions instead of adding rules.
