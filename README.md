# Promptora

AI prompt library, built in phases toward a SaaS product.

- Product requirements: `docs/ai/PRODUCT_SPEC.md`
- Architecture decisions: `docs/ai/DECISIONS.md`
- Architecture: `docs/ai/ARCHITECTURE.md`
- Data model: `docs/ai/DATABASE.md`
- API contracts: `docs/ai/API_CONTRACTS.md`
- Task register: `docs/ai/TASKS.md`
- Progress dashboard: `docs/ai/PROGRESS.md`
- Worker instructions: `docs/ai/workers/`

## Working agreement

- `main` is protected. No direct commits after the initial bootstrap commit.
- Every change is a Pull Request from `feature/TASK-ID-short-description` that references its Issue.
- Every PR needs passing CI (when configured), an independent automated review, and Master approval.
- No secrets in code, logs, Issues, or PR comments.

Status of all documents: DRAFT until the Approval Log in each document says otherwise.
