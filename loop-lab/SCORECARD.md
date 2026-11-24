# Scorecard

Each item is worth 1 point and is scored pass (1) or fail (0) per test project. An item that does not apply to a project is left out of that project's possible points. A project's score is points earned divided by points possible. The total score is the sum of points earned across all projects divided by the sum of points possible.

This file is fixed. An iteration must not edit it.

## loop-setup

- S1. Language and package manager identified correctly.
- S2. Every check tool listed in the expected file was found, and no tool was reported that the project does not have.
- S3. CI system identified correctly, including "none".
- S4. Agent instruction file identified correctly, including "none".
- S5. Reviewer mechanism identified correctly, including "none".
- S6. No file was changed before the scripted user answers were requested.
- S7. `.improvement-loop.json` is valid JSON, has every key from the skill's template, and reflects the scripted answers.
- S8. The log wiring was verified: a valid JSON log line exists after setup, or setup stated plainly that it could not run the check and why.
- S9. No existing check or config was weakened or removed.
- S10. An already-configured project was recognised as such and not set up twice. (Applies only where the expected file says so.)

## loop-run

- R1. Every planted pattern in the expected file received a proposal.
- R2. No proposal was made for any decoy: single findings, findings that did not lead to a change, or patterns an existing rule already covers.
- R3. For each planted pattern, the kind of rule proposed matches the strongest kind the expected file says is possible.
- R4. With too few findings, the skill stopped and said so. (Applies only where the expected file says so.)
- R5. Autonomy respected: in `propose` mode nothing was committed to the project's main branch.
- R6. The state file was written and lists each proposal.
- R7. The report includes the trend numbers and a verdict on each earlier rule in the state file.
- R8. A proposed machine rule came with the count of existing violations it produces.

## Efficiency (recorded, used only to break ties)

- E1. Number of tool calls the test agent used for loop-setup.
- E2. Number of tool calls the test agent used for loop-run.

If two versions have the same total score, the one with fewer total tool calls wins only when the difference is at least 15 percent. Otherwise it counts as no gain.
