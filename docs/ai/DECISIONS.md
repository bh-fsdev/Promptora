# Architecture Decision Records (ADR Log)

| Field | Value |
|-------|-------|
| Document ID | ADR-LOG-001 |
| Version | 0.2 (Draft) |
| Format | MADR-style (Status, Context, Decision Drivers, Options, Decision Outcome, Consequences) |
| Related | PRODUCT_SPEC.md (PRD-001) |
| Last updated | 2026-10-18 |

**Rule:** every decision below has status `Proposed` until the owner approves it. Accepted ADRs are never edited; they are superseded by a new ADR.

## Index

| ADR | Title | Status |
|-----|-------|--------|
| ADR-001 | Web framework | Proposed (pending SPIKE-1) |
| ADR-002 | Database and backend structure | Proposed |
| ADR-003 | Media storage, CDN, and hosting | Proposed (hosting deferred) |
| ADR-004 | Multi-tenancy readiness | Proposed |
| ADR-005 | Authentication, payments, and AI vendors | Proposed (vendors deferred) |
| ADR-006 | Advertising and consent handling | Proposed |

## Research Notes and Confidence

Sources: web search on 2026-10-18. Mostly secondary sources (blogs, aggregators), not official benchmarks. Treat performance and cost claims as hypotheses to be confirmed by SPIKE-1.

- Next.js 16 is the current major line; exact latest patch must be checked at build time (`npm show next version`).
- nextjs.org reports security releases in July 2026 and a move to a formal security release process.
- Astro 6 shipped in March 2026; a 2026 write-up reports Cloudflare acquired the Astro team in January 2026.
- 2026 comparisons broadly agree: Astro is content-first with minimal default JavaScript; Next.js is application-first with a larger ecosystem. Quoted numbers differ between sources and are not used for decisions.
- Still unknown (see PRD OQ-1 to OQ-6): budget, hosting preference, language, regions, launch date, traffic.

---

## ADR-001: Web Framework

- **Status:** Proposed
- **Date:** 2026-10-18
- **Deciders:** Product Owner (approver), Master Claude (proposer)
- **Related requirements:** NFR-001, NFR-002, FR-011, FR-020, Phases B to D

### Context

Phase A is an SEO-critical content site with an admin panel. Phases B to D need authentication, billing, background jobs, and dashboard-style features.

### Decision Drivers

- Mobile Core Web Vitals and crawlability
- Speed of delivery for a small team
- One consistent codebase through Phases B to D
- Security patch burden and ecosystem maturity

### Considered Options

1. **Next.js, single full-stack application**
2. **Astro for the public site plus a separate application for admin/SaaS**
3. **Astro only (SSR with islands)**

### Pros and Cons

| Option | Pros | Cons |
|--------|------|------|
| 1 | One TypeScript codebase for site, admin, auth, billing, API; large ecosystem and hiring pool; pre-rendering and incremental regeneration support crawlable pages | More JavaScript by default, so more effort to reach top Core Web Vitals; frequent releases and security patches require upgrade discipline |
| 2 | Best content performance and likely lower hosting cost | Two codebases, shared auth and data layer, more DevOps for a small team |
| 3 | Single codebase, very light pages | Weaker fit for the heavy application features in Phases B to D |

### Decision Outcome

Proposed: **Option 1**, conditional on SPIKE-1 (a prototype prompt page measured on mobile, with and without a placeholder ad slot). If targets cannot be met with reasonable effort, move the public site to Option 2 before the Phase A build starts.

### Consequences

- Set a JavaScript budget for public pages; load consent and ad code lazily.
- Pin dependency versions, enable dependency and secret scanning, and plan routine patch upgrades.

---

## ADR-002: Database and Backend Structure

- **Status:** Proposed
- **Date:** 2026-10-18
- **Related requirements:** FR-021, NFR-007, Phases B to D

### Context

The data is relational: prompts, categories, tags, media, and later users, subscriptions, credits, and tenants.

### Considered Options

1. Managed PostgreSQL, backend logic inside the main application
2. Document database (for example MongoDB)
3. Multiple specialized databases and separate services

### Decision Outcome

Proposed: **Option 1.** One managed PostgreSQL database. Backend logic lives in the main application for Phase A. Extract background workers only when Phase C needs long-running AI jobs.

### Consequences

- Single source of truth and simpler operations; strong fit for billing and entitlements later.
- No microservices, Kubernetes, or second database without a justified need.
- ORM and migration tooling to be chosen with the data model in Phase 3.

---

## ADR-003: Media Storage, CDN, and Hosting

- **Status:** Proposed (hosting decision deferred)
- **Date:** 2026-10-18
- **Related requirements:** FR-023, NFR-001, NFR-011

### Context

The product is image-heavy and traffic is spiky. Image bandwidth is expected to be the main cost driver.

### Considered Options (hosting)

1. Managed platform for Next.js (simplest operations; cost can grow with traffic and image optimization)
2. Cloudflare-centric stack (CDN, storage, and edge in one place; verify Next.js compatibility and limits)
3. Container hosting or VPS (cheapest at steady load; more operations work)

### Decision Outcome

Proposed: store originals in object storage and serve optimized WebP/AVIF variants through a CDN, generated at upload. Final hosting choice is deferred until budget and traffic estimates exist (OQ-5).

### Consequences

- Choose storage and CDN first, because they drive cost.
- Image variants and cache purge on takedown must be part of the design (FR-026).

---

## ADR-004: Multi-Tenancy Readiness

- **Status:** Proposed (needs explicit owner approval)
- **Date:** 2026-10-18
- **Related requirements:** G-5, Risk R-7

### Context

Phase D needs tenant isolation. Retrofitting multi-tenancy later is expensive, but Phase D demand is unvalidated.

### Considered Options

1. Single-tenant now; retrofit later
2. **Tenant-ready lite:** every content row belongs to a `workspace`; only one default workspace exists; no tenant features built
3. Full multi-tenancy from day one

### Decision Outcome

Proposed: **Option 2.**

### Consequences

- Small added complexity in queries and tests.
- Substantially cheaper migration if Phase D proceeds.
- Avoids over-engineering if Phase D is never built.

---

## ADR-005: Authentication, Payments, and AI Vendors

- **Status:** Proposed (vendor selection deferred)
- **Date:** 2026-10-18
- **Related requirements:** G-3, G-4, OQ-10, OQ-12

### Decision Outcome

No vendor is selected now. Requirements recorded:

- **Auth:** email login plus social login, secure sessions, roles (admin, editor, user, later creator).
- **Payments:** provider depends on legal entity and region (OQ-12).
- **AI tool:** provider and per-image cost validated before Phase C; moderation, rate limiting, and abuse controls required.

### Consequences

Phase A must keep user identity and entitlement checks easy to add later.

---

## ADR-006: Advertising and Consent Handling

- **Status:** Proposed
- **Date:** 2026-10-18
- **Related requirements:** FR-009, FR-010, NFR-001, NFR-005, Risks R-1, R-3

### Decision Outcome

Proposed:

- Load ad and tracking scripts only after consent where required.
- Reserve fixed ad slot dimensions to prevent layout shift.
- Isolate ad code behind one module so it can be disabled for paid users in Phase B.

### Consequences

- Ad scripts count toward the performance budget.
- Ad program approval is not guaranteed and depends on original content and policy compliance.

---

## Planned Tasks (not yet created as GitHub Issues)

| ID | Task | Purpose |
|----|------|---------|
| SPIKE-1 | Prototype a prompt page; measure mobile Core Web Vitals with and without an ad placeholder | Decides ADR-001 |
| DOC-1 | Data model draft in DATABASE.md (including workspace) | Phase 3 |
| DOC-2 | Route and API contracts in API_CONTRACTS.md | Phase 3 |
| LEGAL-1 | Owner reviews ad program policies and consent rules for target regions | Compliance |

## Approval Log

| Decision | Status | Approved by | Date |
|----------|--------|-------------|------|
| ADR-001 | PENDING | | |
| ADR-002 | PENDING | | |
| ADR-003 | PENDING | | |
| ADR-004 | PENDING | | |
| ADR-005 | PENDING | | |
| ADR-006 | PENDING | | |
