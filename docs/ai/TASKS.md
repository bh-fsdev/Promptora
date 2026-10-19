# Task Register

| Field | Value |
|-------|-------|
| Document ID | TASKS-001 |
| Version | 0.1 |
| Owner | Master Claude |
| Last updated | 2026-10-18 |

Statuses: BACKLOG, READY, IN_PROGRESS, REVIEW, DONE, BLOCKED, NEEDS_CHANGES, CANCELLED.
A task is READY only if its scope is clear, acceptance criteria exist, dependencies are met, and no major decision is unresolved.
A task is DONE only after merge with verified evidence. A worker saying "finished" is not evidence.

## Register

| ID | Title | Worker | Status | Depends on |
|----|-------|--------|--------|------------|
| TASK-000 | Owner bootstrap: first commit, protect `main`, install automated reviewer | Owner | READY | None |
| TASK-001 | SPIKE-1: Next.js vs Astro prompt-page performance prototype | Worker 2 | READY | TASK-000 |
| TASK-002 | ADR-007 proposal: migration and database access tooling | Worker 1 | READY | TASK-000 |
| TASK-003 | OpenAPI 3.1 file from API_CONTRACTS.md | Worker 1 | READY | TASK-000 |
| TASK-004 | Initial database migrations and seed script per DATABASE.md | Worker 1 | BACKLOG | ADR-007 approved, ADR-002 and ADR-004 approved |
| TASK-005 | Application scaffold (framework, lint, format, types, CI commands) | Worker 2 | BACKLOG | ADR-001 approved (after TASK-001) |
| TASK-006 | Design tokens and base components | Worker 2 | BACKLOG | DESIGN_SYSTEM.md approved, TASK-005 |
| TASK-007 | Public prompt detail page with copy button | Worker 2 | BACKLOG | TASK-005, TASK-006, API contract approved |
| TASK-008 | Public read API (prompts, search, categories, tags) | Worker 1 | BACKLOG | TASK-004, TASK-005, API contract approved |
| TASK-009 | Admin authentication and role checks | Worker 1 | BACKLOG | TASK-004, TASK-005 |

Tasks beyond TASK-009 are planned after the approvals above.

---

## TASK-000: Owner bootstrap (human)

**Owner:** Repository owner
**Steps**
1. Upload the bootstrap bundle contents to the repository root and commit to `main` (the only direct commit allowed, because an empty repository has no base branch).
2. Enable branch protection on `main`: require a pull request, require at least 1 approval, dismiss stale approvals on new commits, block force-pushes and deletions. Add required status checks once CI exists.
3. Install the automated PR reviewer (CodeRabbit) on this repository only.
4. Run the `Sync Tasks` workflow once (Actions tab). It creates the Issues and labels for the tasks below. Do not create them by hand.
5. Set up the automatic workers using `docs/devops/WORKER_AUTOMATION.md` (Claude GitHub App, `ANTHROPIC_API_KEY` secret, `WORKERS_ENABLED` variable). Fallback without an API key: connect web-chat workers using `docs/ai/workers/WEB_CHAT_OWNER_SETUP.md`.

**Evidence expected:** repository URL showing the files, branch protection settings, reviewer app installed, and the `Sync Tasks` run summary.

---

## TASK-001: SPIKE-1, Next.js vs Astro prompt-page prototype

**Worker:** Worker 2 (frontend)
**Branch:** `feature/TASK-001-spike-next-vs-astro`
**Goal:** Produce measured evidence for ADR-001 so the owner can choose between a single Next.js application and an Astro public site.

**Documents to read:** `PRODUCT_SPEC.md` (FR-004, FR-005, FR-010, NFR-001, NFR-002), `ARCHITECTURE.md` (Sections 7, 11, 14), `DECISIONS.md` (ADR-001, ADR-006).

**Scope**
- Build the same single prompt-detail page twice, in `spikes/spike-1/next-app` and `spikes/spike-1/astro-app`.
- Page content (hard-coded sample data): site header, cover image with responsive variants (WebP and AVIF, explicit width and height, `srcset`, `sizes`), title, prompt text, a Copy button with confirmation, category and tags, five related-prompt cards, a reserved empty ad slot (300x250 and a 320x100 variant, no third-party script), and a minimal consent banner placeholder.
- Use locally generated sample images only. No third-party network requests of any kind.
- Production builds only for measurement.
- Pin all dependency versions exactly. Use the current stable releases, verified from official sources at the time of work, and record them.

**Measurement (lab)**
- Lighthouse, mobile emulation with default simulated throttling, at least 5 runs per page, report the median and the range.
- Report: LCP, CLS, TBT, total transferred JavaScript (compressed), total transferred bytes, HTML size, number of requests.
- Also report build time and the exact commands used.
- Note clearly that lab data does not measure INP; report TBT as a lab proxy and say so.

**Non-goals**
- No real ads, analytics, or consent library. No admin, database, or API. No styling system beyond what is needed. Spike code is throwaway and must not be imported by the future application.

**Deliverables**
- `spikes/spike-1/` containing both prototypes and a `README.md` with run instructions.
- `docs/ai/SPIKE-1-REPORT.md`: method, versions, raw numbers table, screenshots if available, limitations, and a recommendation phrased as a recommendation (the decision belongs to the owner).

**Acceptance criteria**
- AC-1: Both pages build and run with the documented commands.
- AC-2: The Copy button copies the exact prompt text in a real browser, and a confirmation appears. Evidence: test or recorded manual steps.
- AC-3: The ad slot reserves its space and causes no layout shift. Evidence: CLS value.
- AC-4: The report contains the measurements above with real numbers and the commands to reproduce them.
- AC-5: No external network requests during page load. Evidence: network log summary.
- AC-6: Limitations are stated honestly (lab vs field, one page, synthetic data).

**Environment note (web-chat workers):** a chat sandbox may not have a real browser or Lighthouse. If Worker 2 cannot run Lighthouse, Worker 2 builds both prototypes and provides exact commands. The owner then runs the measurements locally (Chrome Lighthouse, mobile) and the numbers are pasted into the report as owner-measured. No estimated numbers are allowed.

**Definition of done:** PR merged with Master approval and the report reviewed by the owner.

---

## TASK-002: ADR-007 proposal, migration and database access tooling

**Worker:** Worker 1 (backend)
**Branch:** `feature/TASK-002-adr-007-db-tooling`
**Goal:** Recommend the tool(s) for schema migrations and database access, so TASK-004 can start.

**Documents to read:** `DATABASE.md` (all, especially Sections 3, 5, 10, 11), `ARCHITECTURE.md` (Sections 5, 6), `DECISIONS.md` (ADR-002, ADR-004).

**Scope**
- Compare at least three realistic options (for example an ORM with built-in migrations, a SQL query builder plus a migration runner, and plain SQL migrations with a standalone runner).
- Evaluate each against: support for PostgreSQL features required by DB-001 (`citext`, generated `tsvector` column, GIN and trigram indexes, partial indexes, check constraints, constrained enums), reviewability of migration SQL, support for backward-compatible expand/migrate/contract changes, CI testability, type safety, compatibility with a Next.js or Astro runtime, maintenance activity, and known security advisories.
- Verify current versions, maintenance status, and advisories from official sources and repositories, not from memory. Provide links and the date checked.
- Write the result as a new `ADR-007` entry appended to `docs/ai/DECISIONS.md`, in the existing MADR style, with status `Proposed`.

**Non-goals**
- Do not write migrations, install the tool in the project, or change other ADRs. Do not select a hosting provider.

**Acceptance criteria**
- AC-1: Three or more options compared with the criteria above and a clear recommendation.
- AC-2: Every factual claim about versions, features, or advisories has a source link and check date.
- AC-3: Any DB-001 feature that a tool cannot express natively is listed with the proposed workaround.
- AC-4: Risks and consequences are stated, including lock-in and migration safety.
- AC-5: Only `docs/ai/DECISIONS.md` is changed.

**Definition of done:** PR merged with Master approval. The owner then approves or changes ADR-007.

---

## TASK-003: OpenAPI 3.1 specification

**Worker:** Worker 1 (backend)
**Branch:** `feature/TASK-003-openapi-spec`
**Goal:** Turn `API_CONTRACTS.md` into a machine-readable contract that both workers can test against.

**Documents to read:** `API_CONTRACTS.md` (all), `DATABASE.md` (field limits), `PRODUCT_SPEC.md` (FR-001 to FR-028).

**Scope**
- Create `docs/api/openapi.yaml` (OpenAPI 3.1) covering every endpoint in API_CONTRACTS.md Sections 4 to 6, with schemas, parameters, error responses (RFC 9457 problem details), security scheme (session cookie plus CSRF header), pagination, and examples.
- Validate with an OpenAPI linter and record the exact command and output.
- Do not change behavior. If the markdown contract is ambiguous, inconsistent, or incomplete, list each issue in the PR description as a question for Master. Do not silently resolve it.

**Non-goals**
- No server code, no generated clients, no changes to `API_CONTRACTS.md`.

**Acceptance criteria**
- AC-1: Every endpoint, field, limit, and status code in the markdown contract appears in the spec.
- AC-2: Linter passes with zero errors; warnings are listed and explained.
- AC-3: A short traceability table (markdown section to OpenAPI path) is included in the PR description.
- AC-4: A list of contract ambiguities found, even if empty.

**Definition of done:** PR merged with Master approval.

---

## BACKLOG task outlines (not assignable yet)

- **TASK-004:** Write initial migrations and a seed script for the tables in DATABASE.md, with CI tests against a real PostgreSQL instance, using the tool approved in ADR-007.
- **TASK-005:** Create the application scaffold on the approved framework with lint, format, type check, test, and build commands; define the real CI commands.
- **TASK-006 and TASK-007:** Design tokens, base components, and the prompt detail page according to DESIGN_SYSTEM.md (to be written in Phase 4).
- **TASK-008 and TASK-009:** Public read API and admin authentication per API_CONTRACTS.md.
