# Web-Chat Worker Mode (claude.ai Projects)

Applies when you are running as a claude.ai chat inside a Project that has the repository added as project knowledge. This section overrides any rule above that assumes you can push code or open pull requests.

## What you can and cannot do

- You CAN read the repository through project knowledge. It is a snapshot. State the date or commit you believe it reflects. If documents look missing or old, ask the owner to click "Sync now" and wait.
- You CANNOT push, create branches, open PRs, or see CI results and automated reviews. The owner performs those steps. Never ask for tokens, passwords, or keys.
- You CAN create files in your own sandbox if your environment supports it. Only claim what you actually executed there.

## Rules that stay exactly the same

Branch naming, one task per chat, scope limits, no fabricated results, no secrets, pinned dependencies, security rules, PR template, report format. You still name the branch and write the PR title and body. The owner applies them.

## Delivery Package (what you hand to the owner for every task)

1. **Files:** every created or changed file at its exact repo-relative path (for example `docs/ai/DECISIONS.md`, `spikes/spike-1/next-app/package.json`). Provide them as downloadable files or one zip that preserves paths. For a changed existing file, deliver the full updated file and list which parts changed.
2. **Branch name:** `feature/TASK-ID-short-description`.
3. **PR title and body:** filled in using `.github/PULL_REQUEST_TEMPLATE.md`.
4. **Report:** in the required report format.
5. **Owner verification commands:** the exact commands the owner can run to reproduce your evidence, plus a list marked `NOT RUN` for anything your environment could not execute.

## Environment honesty (before you start)

Tell the owner which tools your environment really has: Node and package installation, a real browser, Lighthouse, Docker, PostgreSQL. If a tool is missing, say so first and list what the owner must run locally. Never estimate or invent measurements to fill the gap.

## Review loop

After the owner opens the PR, they will paste the automated reviewer's findings and Master's feedback into your chat. Return only the files that changed, an updated report, and a short reply to each finding (fixed, or disagree with technical reasoning). The PR and branch stay the same.

## Task isolation

Start a new chat in the same Project for each task. At the start of every chat, re-read `docs/ai/TASKS.md` and the documents named in the task. Do not rely on memory from other chats.
