---
name: loop-setup
description: Set up a self-improving review loop in the current project. Detect its checks, CI and agent instructions, then install a findings log and config. Run once per project.
---

# Improvement loop: setup

Goal: make every finding from the project's reviewer and code checks get recorded, so the companion skill `loop-run` can later turn repeated findings into permanent rules.

This skill must adapt to whatever project it runs in. Never assume a language, check tool or CI system. Discover first, confirm with the user, then change things.

## Step 1: Discover (read only)

Inspect the project and write down what you find for each item. Mark anything you could not find as "not found" rather than guessing.

- Language and package manager (for example composer.json, package.json, go.mod, pyproject.toml).
- Check tools and their config files: static analysis, code style, tests (for PHP look for phpstan.neon, psalm.xml, .php-cs-fixer.php, phpcs.xml, phpunit.xml; use the equivalents for other languages).
- CI system and its files (.github/workflows, .gitlab-ci.yml, or other).
- Agent instruction files (CLAUDE.md at any level, the .claude directory: agents, skills, hooks, settings).
- How the reviewer is started (subagent, hook, CI job, manual command) and where its findings end up (terminal output, PR comments, CI logs).
- Whether an inner loop already exists, meaning findings are fed back to a coding agent automatically.
- An existing `.improvement-loop.json`. If present, this project is already set up: show the config, ask what the user wants changed, and skip to the relevant step.

## Step 2: Report and ask

Show the user a short summary of what was found and what is missing. Then ask, and wait for answers, on every point that discovery did not settle. Always ask these:

1. Where should the findings log live? Default: outside the repository at `~/.improvement-loop/<project-name>/findings.jsonl`. Alternative: a path inside the repository.
2. Do the checks run on the user's machine, in CI, or both? If any run in CI, a log path on the user's machine is unreachable from CI. Explain this plainly and agree on one of: a CI artifact that is downloaded later, a separate branch or repository for the log, or shared storage the user already has.
3. Autonomy. Default `propose`: every rule change is a pull request for the user to approve. Alternative `apply-low-risk`: code-style rule changes may be applied directly, everything else is still a pull request.
4. Which findings count. Default: only findings that led to a code change, to keep reviewer noise out of the log.

Do not change any file before the user has confirmed the plan.

## Step 3: Write the config

Create `.improvement-loop.json` in the project root and commit it. Per-project settings live here so the user can change them at any time.

```json
{
  "log_path": "~/.improvement-loop/<project-name>/findings.jsonl",
  "autonomy": "propose",
  "count_only_findings_that_led_to_change": true,
  "instruction_file": "CLAUDE.md",
  "instruction_max_lines": 150,
  "min_repeats_for_rule": 3,
  "checks": [
    {"name": "<tool>", "kind": "static-analysis|style|tests|review", "config": "<path>", "command": "<how to run it>"}
  ],
  "benchmark_tasks_path": null
}
```

Fill `checks` from discovery. Leave `benchmark_tasks_path` null unless the user has a set of past tasks to re-run.

## Step 4: Wire up the log

Every finding becomes one line of JSON appended to the log:

```json
{"ts": "2026-01-31T14:05:00Z", "source": "reviewer|<tool name>", "category": "short-kebab-case-label", "rule": "tool rule id or null", "file": "path/to/file", "summary": "one sentence", "led_to_change": true, "ref": "branch or PR"}
```

How to capture findings depends on what discovery found. Pick the lightest option that works and tell the user which you picked and why:

- Tool checks (static analysis, style, tests): use the tool's machine-readable output (JSON or similar) and a small script that converts it to log lines. Put the script in the project, for example `tools/improvement-loop/log-findings`.
- AI reviewer: add to the reviewer's instructions that it must end its review with findings in the JSON line format above, and append them to the log. Reuse existing category labels where one fits; read the last 200 log lines to see which labels exist.
- Claude Code hooks: if the checks run through hooks, the hook can call the logging script. Check the current Claude Code documentation for the hook configuration format before writing it; do not write it from memory.
- `led_to_change`: set it when the fix is made. If that cannot be known at logging time, log `null` and let `loop-run` resolve it from git history.

## Step 5: Schedule the improvement run

A skill cannot run on a timer by itself. Offer the user the options that fit the project and set up the one they choose:

- Manual: the user runs `loop-run` when they want.
- A scheduled CI job (only if the log is reachable from CI).
- A scheduled task on the user's machine.

## Step 6: Verify and hand over

- Run each check once and confirm that a log line is written and is valid JSON.
- Confirm the log path is not accidentally inside the repository when the user asked for outside (and add it to .gitignore if it is inside and should not be committed).
- Tell the user: what was installed, where the log is, how to change settings, and that `loop-run` is the next step once a few weeks of findings exist.

## Rules

- Never invent a tool or config that discovery did not find.
- Never weaken or remove an existing check.
- Keep changes small and show the user a diff before committing.
