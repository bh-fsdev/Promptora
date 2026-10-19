# Worker Automation (GitHub Actions)

| Field | Value |
|-------|-------|
| Document ID | DEVOPS-WA-001 |
| Version | 0.2 (Draft, untested) |
| Last updated | 2026-10-18 |

## Target flow

1. **Tasks become Issues automatically.** `Sync Tasks` reads the Task Register in `docs/ai/TASKS.md` and creates missing Issues with labels. No AI or API key involved.
2. **A worker picks up a READY Issue automatically.** `Worker Dispatch` runs every 15 minutes (or on demand), claims one READY Issue per worker, runs the worker, and creates a `feature/TASK-ID-...` branch and pushes it.
3. **The workflow verifies the push.** It checks that the branch really exists. Only then does it set `status:review` and post a link to open the PR. Otherwise the Issue becomes `status:blocked`. Nothing is marked complete on the worker's word.
4. **The owner opens the PR manually** from the posted compare link, using the PR title and body the worker wrote.
5. **CI runs** because a human opened the PR. **CodeRabbit reviews.** Master reviews the diff.
6. Review findings go back to the worker by setting the Issue label `status:needs-changes`. The next dispatch run continues on the same branch.
7. Merge is manual, after approval and green checks.

Why the PR is manual: pull requests opened with the built-in workflow token do not trigger other workflows, so CI would not run. A PR opened by a human does trigger CI.

## Components

| File | Purpose | Needs API key |
|------|---------|---------------|
| `scripts/sync_tasks.py` | Parse the register, create Issues and labels, promote BACKLOG to READY when dependencies are DONE | No |
| `.github/workflows/sync-tasks.yml` | Runs the script on changes to `TASKS.md` and on demand | No |
| `.github/workflows/worker-dispatch.yml` | Claims READY (or `needs-changes`) Issues and runs workers | Yes |
| `.github/workflows/ci.yml` | Hygiene checks now, Node checks once `package.json` exists | No |
| `CLAUDE.md` | Rules every worker run reads | n/a |

## Labels

| Label | Meaning |
|-------|---------|
| `status:backlog` | Defined, not startable |
| `status:ready` | A worker may pick it up |
| `status:in-progress` | Claimed by a worker (one active Issue per worker) |
| `status:review` | Branch pushed, waiting for manual PR, CI, review |
| `status:needs-changes` | Owner sends it back to the worker |
| `status:blocked` | Pre-flight failed, run failed, or no branch pushed |
| `worker:1`, `worker:2` | Assignment |

## How the register controls work

The Task Register in `TASKS.md` is the source of truth for status. To release a task, change its status in the register through a PR. After merge, `Sync Tasks` promotes it. A task becomes `status:ready` only if the register says READY and every TASK dependency is DONE. TASK-000 counts as done because the workflow runs from `main`.

## One-time setup (repository admin)

1. Commit the bundle to `main` (workflows must be on the default branch).
2. Settings, Actions, General: allow GitHub Actions. Under "Workflow permissions" choose read repository contents by default. Tick "Allow GitHub Actions to create and approve pull requests" only if you later want it. It is not needed for this flow.
3. Run `Sync Tasks` once manually (Actions tab, Run workflow). Confirm Issues #1 onward appear with labels. This step needs no API key.
4. For workers, install the Claude GitHub App on this repository only (https://github.com/apps/claude) and add the secret `ANTHROPIC_API_KEY` (Settings, Secrets and variables, Actions). Never paste the key in chat, Issues, or PRs.
5. Add the repository variable `WORKERS_ENABLED` = `true` only when you are ready for scheduled runs. Remove it or set it to anything else to stop all scheduled worker runs instantly.
6. Branch protection on `main`: require a pull request, require CI status checks `hygiene` and `node` (after the first CI run shows them), block force pushes and deletions, require conversation resolution. Approvals: set 1 and enable Code Owners review if a second person or a bot authors PRs. If you open every PR yourself, GitHub does not let you approve your own, so keep approvals at 0 and rely on required checks plus Master review before you merge.
7. Install CodeRabbit on this repository only.

## First test

1. Run `Sync Tasks`. Expected: Issues for TASK-001 to TASK-009 with correct labels.
2. Make a harmless test: create Issue "[TASK-900] TEST add a line to docs/ai/PROGRESS.md" with labels `worker:1` and `status:ready`, and a matching row in the register (or run `Worker Dispatch` manually with that Issue number).
3. Expected: Issue becomes `status:in-progress`, a run appears, a `feature/TASK-900-...` branch is pushed, the Issue becomes `status:review`, and a compare link is posted. No PR is created by the bot.
4. Open the PR yourself. Expected: `CI` runs, CodeRabbit comments.
5. Send Master the run link, the Issue link, the PR link, and any error text. Master marks each part VERIFIED only after seeing its evidence.

## Safety controls

- Kill switch variable `WORKERS_ENABLED` for scheduled runs.
- One active Issue per worker; global dispatcher concurrency group.
- Duplicate-branch check before starting a new task.
- 45-minute job timeout and `--max-turns 40`.
- Tool allowlist excludes `gh pr create`, `gh pr merge`, workflow and secret editing.
- Branch pushed by the worker is verified by the workflow, not trusted from the AI's report.
- Text from anyone except the owner is treated as data (see `CLAUDE.md`).
- Enforce "workers do not edit `.github/workflows`" with CODEOWNERS plus required review, because a prompt rule alone is not a control.

## Cost

Each worker run uses API credits and Actions minutes. Scheduled polling that finds nothing costs only a few seconds of Actions time. Start with one task, check usage, then raise limits. Set a spend limit on the API key where the console allows it.

## Known limits and risks

- Not yet tested. Action inputs, branch naming, git push permissions, and the tool allowlist must be confirmed by the first run. Fix from the run log.
- Pushes made with the workflow token do not trigger workflows. That is intended here.
- The `feature/` branch prefix relies on the action's `branch_prefix` input. If the branch is named differently, the verification step will not find it, and the Issue will become `status:blocked`. Adjust the prompt or input.
- Review feedback in "fix" mode comes from `gh pr view --comments`. Inline review comments may not be included. Summarize critical ones in an Issue comment.
- GitHub scheduled workflows can be delayed and are disabled after 60 days without repository activity.
- Hosted runners usually have no real browser for Lighthouse. SPIKE-1 measurements may need to run locally by the owner.
- Fully unattended operation beyond this loop (auto-creating new tasks from product goals, auto-merge) is intentionally not enabled.

## Troubleshooting

| Symptom | Likely cause |
|---------|--------------|
| No Issues created | `Sync Tasks` not on `main`, or Actions disabled, or the register table format changed |
| Nothing is picked up | `WORKERS_ENABLED` not `true`, no `status:ready` Issue with a `worker:` label, or the worker already has an `in-progress` Issue |
| Authentication error in worker run | `ANTHROPIC_API_KEY` missing or wrong secret name |
| App or permission error | Claude GitHub App not installed on this repository |
| Issue becomes `status:blocked` | See the run link in the Issue comment; usually a failed pre-flight or no branch matching `feature/TASK-ID-` |
| CI did not run on the PR | PR was opened by a bot, or CI file is not on `main` |
