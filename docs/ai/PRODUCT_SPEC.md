# Product Requirements Document (PRD)

## AI Prompt Library, with a phased path to SaaS

## 1. Document Control

| Field | Value |
|-------|-------|
| Document ID | PRD-001 |
| Version | 0.3 (Draft) |
| Status | DRAFT, not approved |
| Author | Master Claude (AI) |
| Product Owner / Approver | TBD (project owner) |
| Created | 2026-10-18 |
| Last updated | 2026-10-18 |
| Related documents | DECISIONS.md (ADRs); ARCHITECTURE.md, DATABASE.md, API_CONTRACTS.md (planned) |

### 1.1 Revision History

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-10-18 | Initial draft: prompt library with ads |
| 0.2 | 2026-10-18 | Added phased SaaS vision (accounts, AI tool, creator platform) |
| 0.3 | 2026-10-18 | Restructured to PRD standard: requirement IDs, MoSCoW priorities, NFRs, Given/When/Then criteria, risks, glossary |

### 1.2 Conventions

- **Evidence labels:** `[CONFIRMED]` stated by the owner. `[PROPOSED]` recommended, needs approval. `[ASSUMPTION]` needs validation. `[OPEN]` unanswered.
- **Priority (MoSCoW):** Must, Should, Could, Won't (for this phase).
- **Requirement IDs:** `FR-###` functional, `NFR-###` non-functional. IDs are permanent and never reused.
- Nothing is APPROVED until recorded in the Approval Log (Section 16).

## 2. Executive Summary

A public website where the team publishes curated AI image-generation prompts. Each prompt page has a preview image, the full prompt text, and a one-click copy button. Phase A earns revenue from advertising and builds organic search traffic. Later phases add user accounts and subscriptions, an AI photo tool with credits, and a platform for creators to run their own libraries.

## 3. Background and Problem Statement

- [ASSUMPTION] Users want a specific visual result from AI image tools but struggle to write effective prompts.
- [ASSUMPTION] They search for ready-made prompts and need to find, preview, and copy one quickly, mostly on a phone.
- [CONFIRMED] A reference site (promptseen.com) shows this content pattern. It is a structural reference only. No content, prompts, images, or branding may be copied.

## 4. Goals and Non-Goals

### 4.1 Goals

| ID | Goal | Phase |
|----|------|-------|
| G-1 | Build a fast, SEO-friendly prompt library that earns organic traffic | A |
| G-2 | Monetize traffic through ads in compliance with program policies | A |
| G-3 | Convert visitors into registered users and paying subscribers | B |
| G-4 | Offer a paid AI photo tool with positive unit economics | C |
| G-5 | Let creators operate their own libraries on the platform | D |

### 4.2 Non-Goals for Phase A

User accounts, user uploads, comments, payments, AI generation, native mobile apps, video hosting, multi-language UI (unless approved in OQ-1). These are scheduled in later phases, not cancelled.

## 5. Stakeholders and Users

| Stakeholder | Interest |
|-------------|----------|
| Product Owner | Business outcome, scope, budget |
| Visitors (Persona P1) | Find and copy prompts quickly |
| Editors (Persona P2) | Publish content efficiently and safely |
| Engineering (AI workers + reviewers) | Clear, testable requirements |
| Ad network / payment / AI providers | Policy compliance |

### Personas [ASSUMPTION]

- **P1 Visitor:** mobile-first social media user (often in India), arrives from Google or social links, wants a prompt in under 30 seconds.
- **P2 Editor:** publishes several prompts per week, needs a simple admin panel.
- **P3 Owner/Admin:** manages settings, users (later), and reviews analytics.

## 6. Scope by Phase

| Phase | Name | Capabilities | Revenue | Entry gate |
|-------|------|--------------|---------|-----------|
| A | Library + Ads (MVP) | Public library, admin CMS, copy button, search, consent, ads | Ads | PRD approved |
| B | Accounts + Subscriptions | Sign-up, favorites, collections, premium prompts, ad-free plan, billing | Ads + subscription | Phase A live with measurable traffic; payment provider and legal entity decided |
| C | AI Photo Tool | Photo upload, AI generation, credits, job queue, moderation | Credits + subscription | Billing live; AI provider, unit cost and abuse policy approved |
| D | Creator Platform | Multi-tenant workspaces, custom domains, creator roles and billing | Creator plans | B and C stable; demand validated with real creators |

Phase order is [PROPOSED] (see OQ-9).

## 7. Functional Requirements, Phase A

### 7.1 Public Site

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | Home page shows latest, trending, and category sections | Must |
| FR-002 | Category listing pages with pagination | Must |
| FR-003 | Tag listing pages with pagination | Should |
| FR-004 | Prompt detail page: title, preview image, full prompt text, category, tags, "how to use" note | Must |
| FR-005 | One-tap copy button that copies the exact prompt text and shows confirmation | Must |
| FR-006 | Keyword search across published prompts | Must |
| FR-007 | Related prompts section on detail pages | Should |
| FR-008 | Static pages: About, Contact, Privacy Policy, Terms, Disclaimer, Copyright/DMCA contact | Must |
| FR-009 | Consent banner; non-essential scripts load only after consent where required | Must |
| FR-010 | Reserved ad slots with fixed dimensions (no layout shift) | Must |
| FR-011 | `sitemap.xml`, `robots.txt`, canonical URLs, structured data, Open Graph tags | Must |
| FR-012 | Custom 404 page and search-friendly redirects when URLs change | Should |

### 7.2 Admin Panel

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-020 | Secure admin login with roles: admin, editor | Must |
| FR-021 | Create, edit, preview, publish, and unpublish prompts (states: draft, scheduled, published, archived) | Must |
| FR-022 | Scheduled publishing at a set date and time | Should |
| FR-023 | Image upload with automatic resizing and WebP/AVIF conversion; alt text required | Must |
| FR-024 | Manage categories and tags | Must |
| FR-025 | Per-prompt SEO fields (title, description, slug) | Must |
| FR-026 | Takedown action: unpublish and purge cache | Must |
| FR-027 | Audit log of admin actions (who changed what, when) | Should |
| FR-028 | Basic analytics integration (traffic and top prompts) | Should |

## 8. Non-Functional Requirements

| ID | Category | Requirement | Priority |
|----|----------|-------------|----------|
| NFR-001 | Performance | Mobile Core Web Vitals in the "good" range for LCP, INP, CLS on prompt pages (targets finalized in ARCHITECTURE.md; ad scripts included in the budget) | Must |
| NFR-002 | SEO | Public pages are server-rendered or pre-rendered and crawlable without client-side JavaScript | Must |
| NFR-003 | Accessibility | Conform to WCAG 2.2 Level AA for public pages | Must |
| NFR-004 | Security | No known high-severity issues from OWASP Top 10 categories; admin routes require authentication and authorization; secrets never in source | Must |
| NFR-005 | Privacy | Consent managed per applicable law; privacy policy accurate to actual data practices | Must |
| NFR-006 | Availability | Target uptime proposed at 99.5% monthly for the public site [PROPOSED] | Should |
| NFR-007 | Backup/Recovery | Daily database backups and tested restore; initial RPO 24h, RTO 4h [PROPOSED] | Must |
| NFR-008 | Compatibility | Latest two versions of Chrome, Safari (iOS), Firefox, Edge; Android Chrome | Must |
| NFR-009 | Observability | Error tracking, uptime monitoring, and structured logs without sensitive data | Should |
| NFR-010 | Maintainability | Automated tests and CI gates per DEVOPS standards; dependencies pinned and scanned | Must |
| NFR-011 | Scalability | Handle spiky trend-driven traffic via CDN caching; sizing finalized once traffic estimates exist | Should |

## 9. Acceptance Criteria (Selected, Given/When/Then)

**FR-005 Copy button**
- Given a published prompt page, when the visitor taps Copy, then the clipboard contains the exact prompt text with no extra characters, and a confirmation message appears.
- Given a browser that blocks clipboard access, when the visitor taps Copy, then the prompt text is selected and a manual-copy hint is shown.

**FR-021 / FR-022 Publishing**
- Given a draft prompt, when it is not published, then it is not reachable publicly, not in search results, and not in the sitemap.
- Given a prompt scheduled for time T, when T passes, then it becomes public within 5 minutes and appears in the sitemap.

**FR-009 Consent**
- Given a visitor in a region that requires consent, when no consent is recorded, then no advertising or tracking script is requested.

**FR-020 Admin access**
- Given an unauthenticated request to any admin route or API, then access is denied and no data is returned.

**FR-026 Takedown**
- Given a published prompt, when an admin triggers takedown, then the page returns not-found or gone to visitors within 5 minutes, including CDN caches.

**FR-011 SEO**
- Given any published prompt, then the page has a unique title, meta description, canonical URL, and valid structured data.

## 10. Business Model and Assumptions

- [CONFIRMED] Phase A revenue: advertising (AdSense) plus organic traffic.
- [ASSUMPTION] AdSense approval requires original content, complete legal pages, and policy compliance. Approval is not guaranteed.
- [ASSUMPTION] Trend-driven content produces spiky, seasonal traffic.
- [ASSUMPTION] Revenue per visitor varies by region and device. No revenue forecast is made in this document.
- [OPEN] Secondary revenue (affiliate, sponsored posts) in later phases.

## 11. Legal, Privacy, and Compliance

- **Copyright:** publish only images and prompts we own or have licensed. Maintain a takedown process.
- **AI content:** label AI-generated imagery where required.
- **Privacy:** applicable regimes may include India DPDP Act and EU/UK GDPR/ePrivacy, depending on traffic regions (OQ-4). Legal review is recommended before launch. This document is not legal advice.
- **Advertising:** comply with ad program policies, including invalid-traffic rules.

## 12. Success Metrics (KPIs) [PROPOSED]

| Metric | Source | Target |
|--------|--------|--------|
| Indexed pages, impressions, clicks | Search Console | OPEN |
| Monthly visitors, returning-visitor rate | Analytics | OPEN |
| Copy-button click rate per prompt page | Analytics events | OPEN |
| Mobile Core Web Vitals pass rate | Field data | OPEN |
| Ad approval status, RPM, viewability | Ad dashboard | OPEN |
| Prompts published per week | CMS | OPEN |

## 13. Dependencies, Constraints, and Risks

### 13.1 Dependencies

- Domain, hosting account, and GitHub repository (not yet provisioned).
- Ad network account approval.
- Content supply: original images and prompts.

### 13.2 Constraints

- [OPEN] Budget ceiling, hosting preference, launch date.
- [PROPOSED] Low operational complexity: managed services, one database, no microservices.

### 13.3 Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|------------|
| R-1 | Ad program rejects the site (thin or unoriginal content) | Medium | High | Original content, complete legal pages, quality review before applying |
| R-2 | Copyright claim on published images or prompts | Medium | High | Rights checklist per post, fast takedown (FR-026) |
| R-3 | Ads degrade Core Web Vitals and rankings | Medium | Medium | Performance budget includes ads; reserved slots; lazy loading |
| R-4 | Traffic depends on one source (Google) | Medium | High | Build social and direct channels; avoid content spam patterns |
| R-5 | Phase C AI cost exceeds revenue per user | Medium | High | Validate unit economics before building; hard usage limits |
| R-6 | Phase D built without real demand | Medium | Medium | Validate with creators before investment |
| R-7 | Retrofit cost of multi-tenancy | Medium | High | Tenant-ready data model (ADR-004) |

## 14. Open Questions

| ID | Question | Needed by |
|----|----------|-----------|
| OQ-1 | Content language: English, Hinglish/Hindi, or both? | Architecture |
| OQ-2 | Content source and launch volume (how many prompts at launch)? | Planning |
| OQ-3 | Brand name, domain, logo status? | Design |
| OQ-4 | Target regions (consent and legal pages)? | Architecture |
| OQ-5 | Monthly budget and hosting preference? | ADR-003 |
| OQ-6 | Launch date? | Planning |
| OQ-7 | Video prompts and templates: launch or later? | Scope |
| OQ-8 | Who operates the admin panel? | Admin design |
| OQ-9 | Is phase order A, B, C, D acceptable? | Roadmap |
| OQ-10 | Acceptable AI provider and per-image cost for Phase C? | Phase C gate |
| OQ-11 | Have real creators requested Phase D? | Phase D gate |
| OQ-12 | Payment provider and legal entity? | Phase B gate |

## 15. Glossary

| Term | Meaning |
|------|---------|
| Prompt | Text instruction given to an AI image tool to produce a picture |
| CMS | Content management system, here the admin panel |
| ADR | Architecture Decision Record |
| MoSCoW | Must / Should / Could / Won't prioritization |
| Core Web Vitals | Google's page-experience metrics (LCP, INP, CLS) |
| RPO / RTO | Recovery point / recovery time objective |
| Tenant | An isolated customer workspace in a multi-tenant system |

## 16. Approval Log

| Item | Status | Approved by | Date |
|------|--------|-------------|------|
| Product concept: library site, ads, new project | CONFIRMED | Owner | 2026-10-18 |
| Vision: library + accounts/subscription + AI tool + creator platform | CONFIRMED | Owner | 2026-10-18 |
| Sequencing: ads and traffic first, SaaS later | CONFIRMED | Owner | 2026-10-18 |
| Phase A requirements (Sections 7 and 8) | PENDING | | |
| Non-goals (Section 4.2) | PENDING | | |
| Phase order A, B, C, D | PENDING | | |
