# API Contracts

## 1. Document Control

| Field | Value |
|-------|-------|
| Document ID | API-001 |
| Version | 0.1 (Draft) |
| Status | DRAFT, contingent on ADR-001 and DATABASE (DB-001) approval |
| Author | Master Claude (AI) |
| Approver | Product Owner |
| Last updated | 2026-10-18 |
| Related | PRODUCT_SPEC.md, ARCHITECTURE.md, DATABASE.md |

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-10-18 | Initial Phase A contracts |

**Contract rule:** frontend and backend workers implement exactly this contract. Any change requires an impact assessment, an update here, and notice to affected workers before work continues.

## 2. Conventions

| Topic | Rule |
|-------|------|
| Base path | `/api/v1` |
| Format | JSON, UTF-8, `Content-Type: application/json` |
| Field names | `camelCase` in JSON |
| IDs | UUID strings |
| Timestamps | ISO 8601 UTC, for example `2026-10-18T10:30:00Z` |
| Errors | RFC 9457 Problem Details (`application/problem+json`) |
| Pagination | Cursor-based: `limit` (default 20, max 50), `cursor` |
| Versioning | URL major version; additive changes allowed within v1 |
| Unknown fields | Rejected on write requests with `422` |
| Idempotency | `PUT`/`DELETE` idempotent; publish and takedown are safe to repeat |
| Caching | Public GET responses carry `Cache-Control`; admin responses `no-store` |

### 2.1 Public page routes (server-rendered, not JSON)

| Route | Purpose | Requirement |
|-------|---------|-------------|
| `/` | Home | FR-001 |
| `/category/{slug}` | Category listing | FR-002 |
| `/tag/{slug}` | Tag listing | FR-003 |
| `/prompt/{slug}` | Prompt detail | FR-004 |
| `/search?q=` | Search results | FR-006 |
| `/about`, `/contact`, `/privacy-policy`, `/terms`, `/disclaimer`, `/copyright` | Static pages | FR-008 |
| `/sitemap.xml`, `/robots.txt` | Crawler files | FR-011 |

`[OPEN]` final URL patterns depend on OQ-1 (language) and SEO review.

### 2.2 Standard error body

```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Validation failed",
  "status": 422,
  "detail": "One or more fields are invalid.",
  "instance": "/api/v1/admin/prompts",
  "requestId": "req_01H...",
  "errors": [
    { "field": "slug", "code": "already_exists", "message": "Slug is already in use." }
  ]
}
```

| Status | Meaning |
|--------|---------|
| 400 | Malformed request |
| 401 | Not authenticated |
| 403 | Authenticated but not permitted |
| 404 | Not found (or not public) |
| 409 | State conflict (for example publishing an incomplete prompt) |
| 410 | Gone (taken down) |
| 413 | Payload too large |
| 415 | Unsupported media type |
| 422 | Validation failed |
| 429 | Rate limited (`Retry-After` header) |
| 500 | Unexpected server error (no internal details) |

## 3. Authentication and Authorization

- Admin API uses a server-side session in an `HttpOnly`, `Secure`, `SameSite=Lax` cookie.
- State-changing admin requests require a CSRF token header `X-CSRF-Token`.
- Roles: `admin`, `editor`. Deny by default.
- Public GET endpoints require no authentication.

### Permission matrix

| Capability | Public | Editor | Admin |
|------------|--------|--------|-------|
| Read published content | Yes | Yes | Yes |
| Create and edit prompts, upload media | No | Yes | Yes |
| Publish, schedule, unpublish | No | Yes | Yes |
| Takedown, restore taken-down content | No | No | Yes |
| Manage categories and tags | No | Yes | Yes |
| View audit log | No | No | Yes |
| Manage users | No | No | Yes |

## 4. Public API

### 4.1 `GET /api/v1/prompts`

List published prompts.

| Query | Type | Notes |
|-------|------|-------|
| `category` | string | Category slug |
| `tag` | string | Tag slug |
| `sort` | enum | `latest` (default), `trending` |
| `limit`, `cursor` | | Pagination |

Response `200`:

```json
{
  "items": [
    {
      "id": "uuid",
      "slug": "string",
      "title": "string",
      "excerpt": "string",
      "category": { "slug": "string", "name": "string" },
      "tags": [ { "slug": "string", "name": "string" } ],
      "coverImage": {
        "alt": "string",
        "width": 1280,
        "height": 720,
        "variants": [ { "width": 640, "format": "webp", "url": "https://cdn..." } ]
      },
      "publishedAt": "2026-10-18T10:30:00Z"
    }
  ],
  "nextCursor": "string or null"
}
```

### 4.2 `GET /api/v1/prompts/{slug}`

Response `200`: all list fields plus `promptText`, `howToUse`, `seoTitle`, `seoDescription`, `relatedPrompts[]` (up to 6 list items), `updatedAt`.
Errors: `404` if not published, `410` if taken down.

### 4.3 `GET /api/v1/search`

| Query | Type | Rules |
|-------|------|-------|
| `q` | string | 2 to 100 characters, required |
| `limit`, `cursor` | | Pagination |

Response `200`: same shape as 4.1, ordered by relevance. Only published prompts are returned. Rate limited.

### 4.4 `GET /api/v1/categories` and `GET /api/v1/tags`

Response `200`: `{ "items": [ { "slug", "name", "description", "promptCount" } ] }`.

### 4.5 `POST /api/v1/events/copy` (optional, consent-dependent)

Anonymous engagement event.

Request: `{ "promptId": "uuid" }`. Response `204`. Must not store personal data. Client sends it only when analytics consent exists where required. Rate limited per IP.

### 4.6 Health

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `GET /api/health` | Liveness | `200 { "status": "ok" }` |
| `GET /api/ready` | Readiness (database reachable) | `200` or `503` |

## 5. Admin API

All admin endpoints require authentication, return `no-store`, and write to the audit log for state changes.

### 5.1 Session

| Method and path | Purpose | Notes |
|-----------------|---------|-------|
| `POST /api/v1/admin/session` | Log in | Body: `email`, `password`. Throttled. Generic error message on failure |
| `DELETE /api/v1/admin/session` | Log out | `204` |
| `GET /api/v1/admin/me` | Current user | `id`, `email`, `role` |

### 5.2 Prompts

| Method and path | Purpose | Role |
|-----------------|---------|------|
| `GET /api/v1/admin/prompts` | List all statuses; filter by `status`, `category`, `q` | editor, admin |
| `POST /api/v1/admin/prompts` | Create draft | editor, admin |
| `GET /api/v1/admin/prompts/{id}` | Read one | editor, admin |
| `PATCH /api/v1/admin/prompts/{id}` | Update fields | editor, admin |
| `POST /api/v1/admin/prompts/{id}/publish` | Publish now | editor, admin |
| `POST /api/v1/admin/prompts/{id}/schedule` | Body: `{ "scheduledAt": "..." }` | editor, admin |
| `POST /api/v1/admin/prompts/{id}/unpublish` | Back to draft | editor, admin |
| `POST /api/v1/admin/prompts/{id}/archive` | Archive | editor, admin |
| `POST /api/v1/admin/prompts/{id}/takedown` | Body: `{ "reason": "string" }` | admin |
| `POST /api/v1/admin/prompts/{id}/restore` | From `taken_down` to draft | admin |

Create/update body fields:

| Field | Type | Rules |
|-------|------|-------|
| `title` | string | 3 to 120 chars, required |
| `slug` | string | lowercase letters, digits, hyphens; 3 to 100 chars; unique per workspace and locale |
| `promptText` | string | 10 to 5000 chars; plain text |
| `howToUse` | string | up to 1000 chars |
| `categoryId` | uuid | required |
| `tagIds` | uuid[] | up to 10 |
| `coverMediaId` | uuid | required to publish; media must be `ready` |
| `seoTitle` | string | up to 70 chars |
| `seoDescription` | string | up to 160 chars |
| `rightsNote` | string | required; records source or license |

Publish preconditions (`409` if unmet): title, slug, promptText, category, cover image with alt text, and rights note present.
Changing the slug of a published prompt creates a `301` redirect from the old path.

Response shape for a prompt: all fields above plus `id`, `status`, `scheduledAt`, `publishedAt`, `createdAt`, `updatedAt`, `createdBy`, `updatedBy`.

### 5.3 Media

| Method and path | Purpose |
|-----------------|---------|
| `POST /api/v1/admin/media/uploads` | Create upload intent. Body: `{ "fileName", "mimeType", "bytes" }`. Response: `{ "mediaId", "uploadUrl", "expiresAt" }`. Rejects other types than JPEG, PNG, WebP and files over the size limit (`[PROPOSED]` 10 MB) |
| `POST /api/v1/admin/media/{id}/complete` | Verify and process the upload; starts variant generation. Response: media with `status` |
| `GET /api/v1/admin/media/{id}` | Read metadata and variants |
| `PATCH /api/v1/admin/media/{id}` | Update `altText` |

### 5.4 Categories and tags

| Method and path | Purpose |
|-----------------|---------|
| `GET/POST /api/v1/admin/categories` | List, create |
| `PATCH/DELETE /api/v1/admin/categories/{id}` | Update; delete only if unused (`409` otherwise) |
| `GET/POST /api/v1/admin/tags` | List, create |
| `PATCH/DELETE /api/v1/admin/tags/{id}` | Update; delete detaches from prompts after confirmation flag |

### 5.5 Audit log

`GET /api/v1/admin/audit-log` (admin only): filter by `actorId`, `action`, `from`, `to`; cursor pagination. Read-only.

### 5.6 Users (admin only)

`GET/POST /api/v1/admin/users`, `PATCH /api/v1/admin/users/{id}` (change role, deactivate). No hard delete in Phase A.

## 6. Internal Endpoint

| Endpoint | Purpose | Protection |
|----------|---------|------------|
| `POST /internal/jobs/publish-scheduled` | Publish due prompts, refresh caches and sitemap | Shared secret or signed request from the scheduler; not routable publicly without it; idempotent |

## 7. Rate Limits [PROPOSED, finalized at implementation]

| Endpoint group | Limit (per IP unless noted) |
|----------------|-----------------------------|
| Search | 30 requests per minute |
| Public GET | Generous limit; CDN absorbs most traffic |
| Copy event | 60 per minute |
| Admin login | 5 attempts per 15 minutes per account and per IP |
| Admin API | 120 per minute per user |

Responses over the limit return `429` with `Retry-After`.

## 8. Compatibility and Change Policy

- Additive changes (new optional fields, new endpoints) allowed within v1.
- Breaking changes require `/api/v2` or a documented migration period.
- Frontend must ignore unknown response fields; backend rejects unknown request fields.
- Contract tests in CI verify responses against these schemas.

## 9. Open Items

| ID | Item |
|----|------|
| C-1 | Final URL patterns and locale handling (OQ-1) |
| C-2 | Machine-readable OpenAPI 3.1 file to be generated from this document and kept in sync |
| C-3 | Final rate-limit values and size limits |
| C-4 | Trending algorithm definition for `sort=trending` (for example views or copies over 7 days) |
| C-5 | Whether the copy-event endpoint ships in Phase A (analytics provider decision) |

## 10. Approval Log

| Item | Status | Approved by | Date |
|------|--------|-------------|------|
| Phase A API contracts | PENDING | | |
