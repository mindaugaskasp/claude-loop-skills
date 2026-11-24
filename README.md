# claude-loop-skills

A Claude Code plugin, `loop-engineering`, with two skills that add a self-improving loop to any project that already has a reviewer and code checks.

| Skill | When to run | What it does |
|---|---|---|
| `loop-setup` | Once per project | Detects the project's checks, CI and agent instructions, asks a few questions, then installs a findings log and a config file. |
| `loop-run` | On a schedule or on demand | Reads the findings log, finds mistakes that keep recurring, and proposes permanent rules for them as pull requests. |

## How it works

1. Every finding from the reviewer and the code checks is appended to a log, one JSON line each.
2. `loop-run` groups the findings and picks out the ones that repeat.
3. For each repeated mistake it proposes the strongest fix available: a tool rule or test first, then an instruction for the coding agent, then an instruction for the reviewer.
4. On later runs it measures whether each rule reduced its category of finding, and suggests rewording or removing rules that did not.

## Install

```sh
claude plugin marketplace add mindaugaskasp/claude-loop-skills
claude plugin install loop-engineering@mindaugaskasp-plugins
```

On Claude Code 2.1.275 or later, one step inside a session also works:

```
/plugin install loop-engineering --marketplace mindaugaskasp/claude-loop-skills
```

Then run the skills as `/loop-engineering:loop-setup` and `/loop-engineering:loop-run`.

## Per-project settings

Setup writes `.improvement-loop.json` in the project root. Edit it at any time.

| Setting | Default | Meaning |
|---|---|---|
| `log_path` | `~/.improvement-loop/<project-name>/findings.jsonl` | Where findings are stored. Outside the repository by default. |
| `autonomy` | `propose` | `propose`: every rule change is a pull request. `apply-low-risk`: harmless code-style changes go in directly. |
| `count_only_findings_that_led_to_change` | `true` | Ignores reviewer comments that nobody acted on. |
| `min_repeats_for_rule` | `3` | How often a mistake must repeat before a rule is proposed. |
| `instruction_max_lines` | `150` | Length of the agent instruction file above which pruning is suggested. |
| `benchmark_tasks_path` | `null` | Optional set of past tasks to re-run when testing a rule change. |

## Known limits

- A log outside the repository lives on your machine. If the checks run in CI, the log needs a location CI can reach; setup asks about this.
- A skill cannot run on a timer by itself. Setup offers a scheduled CI job or a scheduled local task.
- These skills have not yet been tested against a real project. Treat the first run as a trial.
