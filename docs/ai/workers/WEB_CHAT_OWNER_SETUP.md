# Owner Setup: Connecting Web-Chat Workers

Prerequisite: TASK-000 is complete (bootstrap commit on `main`, branch protection on, reviewer installed).

1. **Create two Projects** in claude.ai: `Promptora: Worker 1 (Backend)` and `Promptora: Worker 2 (Frontend)`.
2. **Add the repository** to each Project: project knowledge, "+", GitHub, select `bh-fsdev/Promptora`. For a private repository, grant the Claude GitHub App access to this one repository only (GitHub admin required). Click "Sync now" whenever the repository changes.
3. **Project instructions:** paste the matching prompt (`WORKER_1_BACKEND_PROMPT.md` or `WORKER_2_FRONTEND_PROMPT.md`) and then the full text of `WEB_CHAT_MODE.md`.
4. **One chat per task.** Start a new chat in the Project and send: `Start TASK-00X. Issue: <link>.`
5. **Collect the Delivery Package** from the worker.
6. **Apply it on GitHub:** create the branch named by the worker, upload the files at their paths (Add file, Upload files), commit to that branch, and open a PR with the worker's title and body.
7. **Review loop:** wait for CI and the automated reviewer. Paste the findings into the worker chat, apply the updated files to the same branch, and repeat until clean.
8. **Master review:** send the PR link, the changed files or diff, and the CI and reviewer output to Master Claude. Master can only verify what is shown to it. A private repository is not directly readable by Master.
9. **Merge** only after Master approves and required checks pass. Update the Issue status.

Never paste tokens or passwords into any chat.
