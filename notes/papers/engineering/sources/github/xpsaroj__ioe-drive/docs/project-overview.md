# IOE Drive - Project Overview

This document is a snapshot of the project as of 2026-08-14. It exists so that anyone
(including future contributors and AI assistants) can get oriented quickly without having
to re-read the entire codebase. Update it as the project evolves; treat it as living
documentation rather than a historical record.

See `whats-done.md` for a short list of what already works, and `todo.md` for planned
work and known rough edges.

## 1. What this project is

IOE Drive is a collaborative resource-sharing platform for students of the Institute of
Engineering (IOE), Tribhuvan University, Nepal. It lets students browse and download
academic resources (notes, past question papers, assessment papers, books, lab sheets,
etc.) organized by program, semester and subject, and lets signed-in students contribute
resources of their own.

The project is a personal/friends project (not an official IOE product) built and
maintained by me and a small group of collaborators.

### Background: what "IOE" and the "new syllabus" mean

- IOE (Institute of Engineering) is the engineering faculty of Tribhuvan University (TU),
  Nepal's oldest and largest engineering institution, with constituent and affiliated
  colleges (Pulchowk Campus, Thapathali Campus, Purwanchal Campus, and many affiliated
  private colleges) offering Bachelor's level (BE / B.Arch) engineering programs.
- IOE runs Bachelor's programs across disciplines such as Computer (BCT), Civil (BCE),
  Electrical (BEL), Electronics, Communication & Information (BEI), Mechanical (BME),
  Architecture (BAR), Geomatics (BGE), Industrial (BIE), Agriculture (BAG), Automobile
  (BAM), Aerospace (BAS) and Chemical (BCH) Engineering. Most programs run 4 years / 8
  semesters; Architecture (BAR) runs 5 years / 10 semesters.
- First-year and some early-semester "service" subjects (math, physics, chemistry,
  communication, etc.) are owned by the Department of Science and Humanities (SH), which
  is not a student-facing program but exists in this project's data model purely to keep
  subject ownership consistent (`totalYears: 0` is used as a flag for this).
- "New syllabus" refers to IOE's revised curriculum (subject codes such as `ENCE 201`,
  `ENSH 201`, replacing the older short codes from the pre-revision curriculum). This
  project's seed data targets the new syllabus exclusively — subject codes, credit/marks
  breakdowns (theory assessment/final, practical assessment/final) and syllabus links all
  point at the current curriculum published on `ioe.tu.edu.np`. There is no support for
  the old syllabus, and none is currently planned.

## 2. Repository layout

This is an npm-workspaces-free monorepo (two independently managed apps, tied together
with a root `docker-compose.yml` and a handful of root convenience scripts):

```
ioe-drive/
├── apps/
│   ├── server/     NestJS + Drizzle ORM API (apps/server/src)
│   └── web/         Next.js 16 App Router frontend (apps/web/src)
├── docs/            Project documentation (this file, whats-done.md, todo.md)
├── .github/workflows/  CI (lint/typecheck/build) + deploy
├── docker-compose.yml  Local dev stack: postgres, server, web
├── SETUP.md         Manual (non-Docker) and Docker setup instructions
└── CONTRIBUTING.md   Fork/branch/PR workflow
```

There is no shared package between `apps/server` and `apps/web` — types are duplicated by
hand on each side (see section 12).

## 3. Architecture and tech stack

- **Style**: client-server, REST API consumed by a Next.js frontend.
- **Frontend**: Next.js 16 (App Router), React 19, Tailwind CSS v4, TanStack Query v5 for
  server state, React Hook Form + Zod for forms, Clerk for auth, Lucide icons, `sonner`
  for toasts, `next-themes` + `@clerk/themes` for light/dark theming (see section 7),
  `@vercel/analytics` (cookieless page-view analytics via an `<Analytics />` component in
  the root layout, disclosed in `/privacy`).
- **Backend**: Node 22, NestJS 11 (on Express 5 under the hood via
  `@nestjs/platform-express`), organized as feature modules under `src/modules/*`, each
  layered consistently as Controller -> Service -> Repository. Validation is
  `class-validator`/`class-transformer` DTOs plus a global `ValidationPipe`; a global
  `HttpExceptionFilter` + `ResponseInterceptor` shape every response into
  `{ success, data?, message?, error?, meta? }`; auth is enforced by a `ClerkAuthGuard`
  (see section 8); rate limiting is `@nestjs/throttler`. Real-time messaging (section 11)
  adds `@nestjs/websockets` + `@nestjs/platform-socket.io` on the server and
  `socket.io-client` on the web app, the only WebSocket usage in the project.
- **Database**: PostgreSQL 16, Drizzle ORM + drizzle-kit for schema/migrations.
- **Auth**: Clerk (`@clerk/backend` on the API, `@clerk/nextjs` on the web app), with a
  Clerk webhook keeping a local `users`/`profiles` mirror in sync.
- **File storage**: Azure Blob Storage (uploads go through Multer in-memory storage, then
  are streamed to a blob container). A `backblaze-b2` dependency is present in
  `apps/server/package.json` but nothing currently uses it — Azure is the only storage
  backend actually wired up.
- **Deployment** (per README/CI): web to Vercel, API to render (a self-managed VM via SSH + pm2 is also specified but not actually used
  (see `.github/workflows/deploy-server.yml`)).

## 4. Data model (apps/server/src/db/schema.ts)

Enums:
- `semester_enum`: "1".."10"
- `year_enum`: "1".."5"
- `subject_hardness_level_enum`: EASY, MEDIUM, HARD, VERY_HARD
- `resource_type_enum`: NOTE, PAST_QUESTION, ASSESSMENT, LAB_SHEET, BOOK, OTHER

Tables:
- `programs` — id, code (e.g. BCT, BCE, SH), name, totalYears, syllabusUrl.
- `subjects` — id, code, name, programId (FK), hardnessLevel, description, syllabusUrl.
  Subjects belong to exactly one owning program/department (e.g. SH owns first-year
  service subjects) but are *offered* to other programs via `subject_offerings`.
- `subject_marks` — one-to-one with subjects; theoryAssessment/theoryFinal/
  practicalAssessment/practicalFinal integer marks breakdown.
- `subject_offerings` — the join between a subject, the program it's taught in, the year,
  and the semester, plus `isElective`. Unique on (subjectId, semester, programId, year).
  This is the entity most of the app actually filters/browses by (not `subjects` or
  `programs` directly), since the same subject can be offered to multiple programs.
- `users` — id, clerkUserId (unique), fullName, email, `role` (user_role_enum: `USER`
  default, `MODERATOR`, `ADMIN` — see section 9); mirrors Clerk, created/updated via
  webhook (see section 8).
- `profiles` — one-to-one with users; bio, programId, semester, college,
  profilePictureUrl. When both `programId` and `semester` are set, the `/resources`
  browse page uses them to default its filter for that signed-in user (see section 6).
- `resources` — the generic resource entity (notes, past questions, assessment papers,
  lab sheets, books, etc.): title, description, `type` (resource_type_enum, required),
  offeringId (FK to `subject_offerings`), uploadedBy (FK to users, nullable via
  `set null` on delete), `status` (resource_status_enum: `PENDING`/`APPROVED`/`REJECTED`/
  `REMOVED`, required), plus `moderatedBy`/`moderationReason`/`moderationNote`/
  `moderatedAt` — a denormalized snapshot of the latest moderation decision, kept in sync
  with (but not a replacement for) the `moderation_actions` history table below — see
  section 9.
- `resource_files` — one-to-many with resources; fileUrl, fileSize, originalFileName,
  blobName, mimeType, plus unused-so-far `compressedSize`/`compressionMethod` columns
  (no compression is implemented yet).
- `user_recent_resources` — per-user "recently accessed" tracking, unique on (userId,
  resourceId), used for the dashboard and `/library` "Recently Accessed" lists (paginated,
  see section 12; nothing is ever deleted from the table itself - fine at this project's
  scale since the row count per user is bounded by distinct resources ever viewed, not by
  view count).
- `user_bookmarked_resources` — per-user bookmarks, unique on (userId, resourceId). The
  `/library/bookmarks` list itself is paginated (see section 12), but checking whether a
  given resource is bookmarked (for the bookmark icon shown on every resource card) goes
  through a separate, uncapped IDs-only endpoint instead.
- `reports` — a report filed against an already-`APPROVED` resource: resourceId,
  reportedBy, reason (moderation_reason_enum), note, status (`OPEN`/`RESOLVED`),
  resolvedAt, resolvedBy. Unique on (resourceId, reportedBy) — one open report per user
  per resource. See section 9.
- `moderation_actions` — append-only history of every approve/reject/remove: resourceId,
  actorId, action (`APPROVE`/`REJECT`/`REMOVE`), reason, note, createdAt. See section 9.
- `role_changes` — append-only history of USER/MODERATOR role changes made through the
  admin endpoint: userId, changedBy, previousRole, newRole, createdAt. Granting/revoking
  `ADMIN` never goes through that endpoint, so it never appears here either — see
  section 9.
- `webhook_events` — svixId primary key + eventType, used purely for Clerk webhook
  idempotency (see section 8).
- `resource_votes` — one row per (userId, resourceId) upvote/downvote, unique-constrained
  so a user can only ever have one active vote per resource; `resources` itself carries
  denormalized `upvoteCount`/`downvoteCount`/`downloadCount` columns kept in sync inside
  the same transaction as any vote change (row-level `SELECT ... FOR UPDATE` locking to
  close a real TOCTOU race caught during a security review — two concurrent votes could
  otherwise both read the same starting count and double-apply their delta).
  `downloadCount` increments only on a real download (`Content-Disposition: attachment`),
  not an inline preview.
- Marketplace + messaging tables (`marketplace_listings`, `marketplace_listing_photos`,
  `marketplace_reports`, `marketplace_conversations`, `marketplace_messages`) — see
  section 10 for the full data model and section 11 for messaging.

Seventeen migrations exist (`0000`..`0016`). Notable history visible in the earliest
migrations:
subjects.code widened to varchar(15) (`0008`); `notes.subject_id` renamed to
`notes.offering_id` with the FK repointed from `subjects` to `subject_offerings` (`0009`)
— i.e. notes were originally tied directly to a subject and were later moved to be tied
to a specific subject *offering* (subject + program + year + semester), which is the
correct granularity for a program/semester-scoped resource library; and `notes`/
`note_files`/`user_recent_notes`/`user_archived_notes` were renamed in place to
`resources`/`resource_files`/`user_recent_resources`/`user_bookmarked_resources`, with a
required `type` column backfilled to `NOTE` for pre-existing rows (`0010`).

## 5. Resource types and the notes -> resources generalization

The product concept was originally "notes" only and has since been generalized to
"resources" (notes, past questions, assessment papers, lab sheets, books, or other), each
tagged with a required `type` field (`resource_type_enum` in the DB, `ResourceType` enum
on both the server and web side). This rename now touches the database, backend, and
frontend consistently:
- DB tables, backend module (`apps/server/src/modules/resources/*`), and frontend entity
  types (`apps/web/src/types/entities/resources.ts`) all use `Resource`/`ResourceFile`/
  `UploadedResource`/`RecentResource`/`BookmarkedResource` naming.
- Components (`ResourceCard`, `ResourceList`, `ResourceFileList`, `UploadedResourceCard`,
  `RecentResourceCard`, `BookmarkedResourceCard`, etc.) consume the `Resource`-shaped
  types/API responses end to end. See section 6 for the current route layout
  (`/resources` vs `/library`).
- The resource-upload form's "Resource Type" selector is wired to the real
  `ResourceType` enum and is actually submitted with the upload (it previously existed
  in the UI but was silently dropped before reaching the API).

A related rename, done in the same pass: "archived" became "bookmarked" throughout —
the DB table is `user_bookmarked_resources` (`bookmarked_at`, not `archived_at`), the API
paths are `/api/me/bookmarked-resources` and `/api/me/resources/:resourceId/bookmark`,
and the frontend type is `BookmarkedResource`.

## 6. Routing: `/resources` (browse/share) vs `/library` (personal space)

Resource browsing and personal resource views used to be mixed together under one
`/resources` hub page (which linked out to `/resources/current`,
`/resources/me/{recent,bookmarks,uploads}`, and `/resources/share`). This has been split
along a clearer line: `/resources` is the shared/generic side (browse the catalog,
contribute to it), `/library` is the signed-in user's personal space (read-only views of
things tied to them).

- `/resources` is now a single unified browse page — there is no more hub page. It always
  shows Program and Semester selects; once both are chosen, a Subject select joins them in
  the same filter row (which wraps responsively on narrow screens), and the page shows the
  subject's details toggle plus its available resources. For signed-in users with
  `program`/`semester` set on their profile, the filter is defaulted automatically via a
  redirect that puts the choice into the URL as query params (e.g.
  `/resources?programId=6&semester=3`), so a specific view is shareable/bookmarkable.
  Guests (and signed-in users with an incomplete profile) get the same picker with no
  default, and browsing works for them too — see the bugfix note below.
- `/resources/share` (upload) and `/resources/r/[resourceId]` (detail) are unchanged in
  behavior, both nested under `/resources` since they're resource-domain actions/views,
  not personal ones.
- `/library` is a new personal-space hub (auth-required): quick links plus preview panels
  for recently-accessed and bookmarked resources, and a link to My Uploads.
  `/library/recent`, `/library/bookmarks`, `/library/uploads` are the corresponding full
  list pages (moved from the old `/resources/me/*`).
- `proxy.ts` explicitly protects `/library(.*)` and `/resources/share(.*)`, while leaving
  `/resources` itself (browsing) and `/resources/r/[resourceId]` public — see section 8.
- **Bugfix along the way**: `useSubjectOfferings` (the hook backing subject/resource
  browsing) was gated with `enabled: isSignedIn`, silently blocking guests from browsing
  at all even though the backing `/api/subjects` endpoint never required auth. That gate
  is removed, so the public-browsing intent actually holds now (this also retires the
  discrepancy that used to be tracked here about `/resources` blocking guests).

## 7. Theming: light/dark mode

The web app supports light, dark, and system (OS-preference-following) themes.

- **Token-based color system**: `apps/web/src/app/globals.css` defines every color as a
  `--color-*` CSS variable inside a Tailwind v4 `@theme` block, and components are built
  on semantic Tailwind classes (`bg-background`, `text-foreground-secondary`,
  `border-border`, etc.) rather than literal colors (`bg-white`, `text-gray-500`). A
  `.dark { ... }` block overrides every one of those tokens with dark-mode equivalents.
- **Tailwind v4's `dark:` variant** defaults to the `prefers-color-scheme` media query;
  this project overrides that with `@custom-variant dark (&:where(.dark, .dark *));` so
  `dark:` instead responds to a `.dark` class, which is what actually gets toggled (see
  next point). A few genuinely-literal color usages that aren't meant to react to the
  theme automatically (severity-tinted badges like `SubjectHardnessBadge`/
  `MimeTypeBadge`, and the black backdrop dimmers behind `Modal`/`MobileNav`) use
  explicit `dark:` classes or are left as literal black on purpose.
- **`next-themes`** (`apps/web/src/providers/theme-provider.tsx`) manages the `.dark`
  class on `<html>` based on system preference or an explicit user choice, persisted to
  localStorage. Root layout (`app/layout.tsx`) sets `suppressHydrationWarning` on
  `<html>`, since next-themes updates that element before React hydrates.
  `apps/web/src/components/ui/ThemeToggle.tsx` is the light/dark toggle button, present
  in the desktop `Navbar`, `MobileNav`, and the signed-out marketing `Header`.
- **`@clerk/themes`** (`apps/web/src/providers/clerk-theme-provider.tsx`) wraps
  `ClerkProvider` and passes Clerk's own `dark` base theme when the site is in dark
  mode, so Clerk's hosted UI (sign-in, sign-up, user profile, user button) matches
  rather than always rendering light.
- **`apps/web/src/hooks/use-mounted.ts`**: a shared hook (via `useSyncExternalStore`,
  not a `useEffect` + `setState` pair - this project's lint config flags that pattern)
  used anywhere theme-dependent output needs to avoid a hydration mismatch (the actual
  resolved theme isn't known until the client has mounted). `Logo`, `ThemeToggle`, and
  `ClerkThemeProvider` all use it to render a neutral/default appearance for the very
  first render, then the real theme-aware output right after.
- `Logo`'s `theme` prop is now optional and auto-picks the correct light/dark logo
  variant to match the site's current theme; pass it explicitly only when a specific
  variant is needed regardless of theme.

## 8. Auth model

Clerk is the identity provider on both sides.

- **Web** (`apps/web/src/proxy.ts`, a Next.js middleware despite the filename): uses
  `clerkMiddleware`/`createRouteMatcher` to protect `/dashboard`, `/library`,
  `/resources/share`, `/community`, `/market/create`, `/market/(.*)/edit`, `/messages`,
  `/alumni`, `/profile`, `/onboarding`, and redirects already-signed-in users away from
  `/sign-in` and `/sign-up`. `/resources` itself (browsing), `/resources/r/[resourceId]`,
  and `/market` (browsing/detail) are intentionally left public — see sections 6 and 10.
  The matcher used to say `/marketplace(.*)` (a name that never matched any real route,
  since the page lives at `/market`) which silently left the create/edit pages
  unprotected; fixed to the routes above rather than a blanket `/market(.*)`, since
  browsing is deliberately public, same as resources.
- **API** (`apps/server/src/common/guards/clerk-auth.guard.ts`): `ClerkAuthGuard`
  authenticates the request via `@clerk/backend`'s `authenticateRequest` (given a Fetch
  API `Request` bridged from the underlying Express request by
  `common/utils/fetch-request.ts`), then looks up the corresponding row in the local
  `users` table by `clerkUserId`. If no local row exists yet, the request is rejected as
  unauthorized even though Clerk considers the user signed in — the local `users` table
  must be kept in sync with Clerk for auth to work end-to-end (see next point). Applied
  per-controller/route via `@UseGuards(ClerkAuthGuard)`; a `@CurrentUser()` param
  decorator reads the resulting local user off the request in a controller method.
- **User sync**: a Clerk webhook (`/api/webhooks/clerk`, verified via `@clerk/backend`'s
  `verifyWebhook` against the untouched raw body Nest exposes via its `rawBody: true`
  bootstrap option) handles `user.created`/`user.updated`/`user.deleted` and upserts
  into `users`/`profiles`. `webhook_events` provides idempotency (svixId as PK, dedupe
  via `WebhookEventsRepository`). There's also a standalone seeder script
  (`db:sync-clerk-users`) that bulk-syncs all users from a Clerk *development* instance
  (it hard-refuses to run against anything but an `sk_test_` key) into the local DB,
  useful for backfilling or resetting a local dev database without replaying webhooks.
- Route-level authorization on the API is coarse: whole controllers are gated with
  `@UseGuards(ClerkAuthGuard)` (`me`, `users`) or per-route (`resources` create/update).
  Reading resources/subjects/programs is public; only creating/updating resources and
  anything under `/me` or `/users` requires auth. A role concept now exists on top of
  this (`USER`/`MODERATOR`/`ADMIN`) — see section 9.

## 9. Roles and resource moderation

Three roles live on `users.role` (`user_role_enum`): `USER` (default), `MODERATOR`,
`ADMIN`. `ADMIN` includes every `MODERATOR` permission — checked via explicit
`@Roles("MODERATOR", "ADMIN")` lists on each route (`common/decorators/roles.decorator.ts`
+ `common/guards/roles.guard.ts`, a standard Nest `Reflector`-based RBAC guard), not a
hierarchy resolver — plus the ability to promote/demote other users between `USER` and
`MODERATOR` (`PATCH /api/admin/users/role`, by email). Granting or revoking `ADMIN` itself
is never done through the app, by design, only ever a direct database change:
`UPDATE users SET role = 'ADMIN' WHERE email = '...';` (there's no seeded/scripted first-
admin step — a `promote-moderator` seeder existed briefly during development and was
deliberately removed in favor of this).

Every resource carries a `status` (`resource_status_enum`: `PENDING`, `APPROVED`,
`REJECTED`, `REMOVED`). New uploads start `PENDING` and are invisible everywhere except to
their own uploader and moderators/admins — every public read path (`findMany`, `findById`,
`searchSuggestions`, `findSimilar`, the recent/bookmarked joins) either filters to
`APPROVED` or, for `findById`/the file-download-url route, checks the viewer's identity/
role, so a resource pending review can't be browsed, searched, downloaded, or even
confirmed to exist by anyone else (this parity between "visible on the detail page" and
"downloadable" was a real gap fixed during a security pass — the download-url route was
originally missed when the status model was added). A moderator can approve a pending
resource, reject it with a reason (resubmittable — the owner editing a rejected resource
resets it back to `PENDING`), or remove it (terminal — its files are purged from Azure,
the row and moderation reason are kept so the uploader can see why). Every approve/reject/
remove is recorded in an append-only `moderation_actions` table, kept separate from the
"latest action" snapshot still cached directly on `resources` (`moderatedBy`/
`moderationReason`/`moderationNote`/`moderatedAt` — what existing reads already use, so
nothing else had to change to gain history for free). Role changes get the same
treatment via a `role_changes` table.

Any signed-in user other than the uploader can report an already-`APPROVED` resource with
a structured reason (`reports` table, one per resource per reporter, unique-constrained).
Reporting never hides the resource — it stays live until a moderator reviews the open-
reports queue and either dismisses the report or acts on the resource (which auto-resolves
any open reports against it). The reporter's identity (`reports.reportedBy`) and whoever
dismissed a report (`reports.resolvedBy`) are only ever visible to moderators, never
surfaced to the uploader.

Frontend: `moderation` (pending queue, reports queue) and `admin` (role
management — an email + USER/MODERATOR toggle) are role-gated both client-side (their nav
entries don't render at all for unauthorized users) and, more importantly, server-side via
the same `@Roles(...)` guards — the client-side gate is convenience/UX only. Both are
kept out of search engines via `noindex` response metadata.

## 10. Marketplace listings

`/market` is a campus classifieds board: any signed-in student can post something for
sale or something they're looking for, browsable by anyone (including guests) without
needing an account.

- **Data model** (`marketplace_listings`, `marketplace_listing_photos`,
  `marketplace_reports`, `marketplace_moderation_actions`): one `marketplace_listings`
  table with a `type` (`marketplace_listing_type_enum`: `SELLING`/`WANTED`) column,
  mirroring how `resources` uses a single `type` enum rather than separate tables per
  kind. A `category` enum (`TEXTBOOKS_AND_NOTES`, `DRAFTING_AND_STATIONERY`,
  `CALCULATORS_AND_ELECTRONICS`, `LAB_AND_WORKSHOP_EQUIPMENT`,
  `FURNITURE_AND_HOSTEL_ITEMS`, `OTHER`), an optional integer `price` (null means
  "contact for price" - common for `WANTED` posts), and an optional `offeringId` FK to
  `subject_offerings` for textbook/notes-type listings. 1-6 photos are required per
  listing (`marketplace_listing_photos`, enforced both client- and server-side),
  uploaded to Azure Blob Storage via the same pattern as resource files.
- **Moderation model now mirrors resources**: a new listing starts `PENDING` and is
  invisible to everyone but its poster and moderators/admins until a moderator approves
  it (`ACTIVE`) or rejects it with a reason (`REJECTED`, resubmittable - the poster
  editing it resets it back to `PENDING`, same implicit-resubmission behavior resources
  have). This replaced an earlier "live immediately, report-to-remove only" model once
  reports turned out to be too reactive in practice. Reporting still exists as
  defense-in-depth after approval (any signed-in non-owner can report an
  `ACTIVE`/`FULFILLED` listing with a structured reason, `marketplace_reports`, one open
  report per user per listing, mirroring `reports`); a moderator dismisses the report or
  removes the listing (terminal, purges its photos from Azure). Every
  approve/reject/remove is recorded in an append-only `marketplace_moderation_actions`
  table, mirroring `moderation_actions` - REJECT's resubmission cycle is exactly why a
  single denormalized "latest action" snapshot alone is no longer sufficient the way it
  was under the old REMOVE-only model.
- **Status lifecycle**: `PENDING` → `ACTIVE` (moderator-approved) → `FULFILLED` (owner
  marks their own listing as sold/found; reversible via `reactivate`; hidden from the
  default public browse but still reachable via a direct link or the owner's own "My
  Listings" page, `/library/marketplace`) → back to `ACTIVE`; `PENDING`/`ACTIVE` →
  `REJECTED` (moderator-only, resubmittable); `ACTIVE`/`FULFILLED` → `REMOVED`
  (moderator-only, terminal). Browsing (`GET /api/marketplace/listings`) is fully public
  and unfiltered by default (no `offeringId`/`userId`/`q` required, unlike resources'
  `findMany`), since "just look at everything" is the core use case for a classifieds
  board, unlike resources which is always course- or search-scoped; it only ever
  returns `ACTIVE` listings unless `includeAllStatuses` is set.
- **Listing photos are served via signed, short-lived Azure Blob SAS URLs** (60-minute
  expiry, generated on every read path in `MarketplaceListingsService`/
  `MessagingService`), not permanent public URLs — the container is private the same
  way gated resource files are (section 15). This wasn't caught until the frontend photo
  UI was actually being built: the stored `photoUrl` is the raw, unsigned blob URL and
  403s directly in a browser.
- Frontend: `/market` (browse - filters for type/category/price/keyword),
  `/market/create`, `/market/[listingId]` (detail) + `/market/[listingId]/edit`,
  `/library/marketplace` ("My Listings" - not originally called out as its own route but
  needed once fulfilled listings became hidden from the default browse), and
  "Marketplace Pending" + "Marketplace Reports" tabs alongside the existing resource
  moderation queues.

## 11. Real-time messaging

Once a listing exists, any signed-in non-owner can message its poster about it
(`/messages`). Chat is real-time via WebSockets — a deliberate choice made up front over
a simpler polling inbox, even though this introduced the project's only WebSocket usage.

- **Data model** (`marketplace_conversations`, `marketplace_messages`): one
  conversation per (listingId, initiatorId) pair — re-contacting the same poster about
  the same listing reuses the existing thread rather than duplicating it.
  `marketplace_conversations.updatedAt` is bumped explicitly inside the same transaction
  as each new message insert (not via a `$onUpdate` hook, which only fires on an update
  to that row itself), so the inbox can sort by "most recently active" purely off that
  column. Self-messaging your own listing, and messaging a listing that isn't currently
  `ACTIVE`/`FULFILLED` (`PENDING`/`REJECTED`/`REMOVED`), are both blocked server-side -
  including into an already-open conversation, if the listing's status changes out from
  under it after the fact.
- **REST layer** (`MessagingController`, all routes `ClerkAuthGuard`-gated): conversation
  list (with last-message preview and per-conversation unread count), paginated message
  history (newest-first, with "load older" pagination in the thread UI), starting a
  conversation (which sends the first message), marking a conversation read, and a
  total-unread-count endpoint that seeds the nav badge before the socket takes over.
  Sending a message into an *already-open* conversation is socket-only — there's no REST
  fallback for that specific case.
- **WebSocket gateway** (`MessagingGateway`, namespace `/marketplace-messaging`, built on
  `@nestjs/websockets` + `socket.io`): every connected socket auto-joins a personal
  `user:{id}` room (this is what drives live inbox/unread-badge updates without polling,
  even when no specific thread is open), and joins a `conversation:{id}` room lazily,
  only while that thread is actually open. Emitting `new_message`/`conversation_updated`
  lives on the gateway (`emitNewMessage`/`emitConversationUpdated`) but is triggered from
  `MessagingService` for every message-creation path (REST `startConversation` included,
  not just the socket's `send_message`) - `MessagingService` looks the gateway up
  lazily via `ModuleRef` rather than injecting it directly, since `MessagingGateway`
  already depends on `MessagingService` and a constructor-level dependency the other way
  would be circular.
- **Shared auth path**: `ClerkIdentityResolver` (`apps/server/src/clerk/`) was extracted
  out of the duplicated logic that used to live separately in `ClerkAuthGuard` and
  `OptionalClerkAuthGuard`, specifically so the WebSocket gateway's handshake
  authentication (`toSocketFetchRequest`, building a synthetic `Request` from the
  socket's `handshake.auth.token`) goes through the exact same code path as every HTTP
  guard, rather than a second hand-rolled implementation.
  `common/adapters/socket-io.adapter.ts` configures CORS for the gateway imperatively in
  `main.ts` (`app.useWebSocketAdapter(...)`), since a `@WebSocketGateway()` decorator's
  own options are static and evaluated before `ConfigService` is available.
- **Known v1 limitations, not bugs**: the in-memory socket.io adapter doesn't broadcast
  across multiple server processes (fine at this project's single-instance scale; a
  `@socket.io/redis-adapter` would be needed to horizontally scale it). Typing
  indicators, read-receipt UI, and message attachments are out of scope for v1.
- Frontend: `MessagingSocketProvider` (in the root layout) owns the single socket
  connection's lifecycle and the always-on `conversation_updated` → unread-count/inbox
  cache updates; `/messages` (inbox) and `/messages/[conversationId]` (an open thread,
  joining/leaving its room on mount/unmount and appending incoming messages to local
  state directly) are the two pages. `StartConversationButton` on a listing's detail
  page is hidden for the listing's own owner.

## 12. API surface (apps/server)

Registered via Nest controllers, one feature module per domain under
`apps/server/src/modules/*`:

- `GET /health` — liveness check, mounted outside `/api` and outside the rate limiter.
- `POST /api/webhooks/clerk` — Clerk webhook receiver; reads the untouched raw request
  body (via Nest's `rawBody: true` bootstrap option) since signature verification needs
  it.
- `/api/me/*` (auth required) — get/update own profile, list own uploaded resources
  (paginated), list recently-accessed resources (paginated), list bookmarked resources
  (paginated), list every bookmarked resource ID (uncapped, IDs only -
  `GET /bookmarked-resource-ids`, backs the bookmark icon shown on every resource card),
  mark/unmark a resource as recently-accessed or bookmarked. The mark-as-recently-accessed
  call is now actually triggered from the frontend (a resource's detail page and its file
  preview page both fire it) - the endpoint existed for a while but nothing called it.
- `/api/users/:userId` (auth required) — fetch another user's public-ish profile.
- `/api/resources` — `GET /` (filter by `offeringId` or `userId`, at least one required,
  paginated, sorted newest-first by `createdAt`; same for `/api/me/resources`),
  `GET /:resourceId`, `POST /` (auth + multipart upload, field name `resourceFile`, up to
  5 files, body includes the required `type`), `PATCH /:resourceId` (auth, must be the
  uploader), `DELETE /:resourceId` (auth, must be the uploader; also deletes the
  resource's files from Azure Blob Storage), `POST /:resourceId/files` (auth, must be
  the uploader; attach more files, same multipart shape as creation),
  `DELETE /:resourceId/files/:fileId` (auth, must be the uploader),
  `GET /:resourceId/files/:fileId/download-url?download=true|false` (auth; any signed-in
  user for an `APPROVED` resource, only its uploader or a moderator/admin otherwise —
  same visibility rule as `GET /:resourceId`, see section 9) returns a short-lived Azure
  SAS URL for that file. See section 14 for ownership enforcement details and section 15
  for the preview page built on this endpoint. `GET /approved-ids` returns a flat,
  IDs-only list of every `APPROVED` resource (no pagination, no joins) - backs the
  sitemap.
- `POST /:resourceId/approve` / `POST /:resourceId/reject` / `POST /:resourceId/remove`
  (moderator/admin only) and `POST /:resourceId/report` (any signed-in user but the
  uploader) — see section 9.
- `/api/moderation/pending` / `/api/moderation/reports` / `/api/moderation/reports/
  :reportId/dismiss` (moderator/admin only) and `/api/admin/users/role` (admin only) —
  see section 9.
- `/api/programs` — `GET /`, list all programs (small, fixed set - not paginated).
- `/api/subjects` — `GET /?programId=&semester=`, `GET /:subjectId`,
  `GET /upload?programId=&semester=` (subject list scoped for the upload form; always a
  small per-program/semester subset - not paginated), `GET /offering-ids?programId=`
  (flat, IDs-only list of a program's subject-offering ids - backs the sitemap).
- `PUT`/`DELETE /api/me/resources/:resourceId/vote` (auth; self-voting on your own
  upload is blocked server-side), `GET /api/me/resources/vote-values` (this user's own
  vote on a batch of resources) — see section 4.
- `/api/marketplace/listings` — `POST /` (auth, multipart, field `listingPhoto`, 1-6
  photos required, always created `PENDING`), `PATCH`/`DELETE /:listingId` (auth, must
  be the poster), `POST /:listingId/{mark-fulfilled,reactivate}` (auth, must be the
  poster), `POST`/`DELETE /:listingId/photos[/:photoId]` (auth, must be the poster; must
  always leave at least one photo), `POST /:listingId/report` (any signed-in
  non-poster, `ACTIVE`/`FULFILLED` only), `POST /:listingId/{approve,reject}`
  (moderator/admin only) and `POST /:listingId/remove` (moderator/admin only,
  `ACTIVE`/`FULFILLED` only), `GET /:listingId` (public for `ACTIVE`/`FULFILLED`,
  moderator/poster-only otherwise), `GET /` (fully public, unfiltered browse allowed -
  filters: `type`, `category`, `offeringId`, `userId`, `minPrice`, `maxPrice`, `q`) —
  see section 10.
- `/api/moderation/marketplace/pending` (moderator/admin only, the listing review
  queue) / `/api/moderation/marketplace/reports` / `/api/moderation/marketplace/reports/
  :reportId/dismiss` (moderator/admin only) and `/api/me/marketplace/listings` (auth;
  "My Listings", includes non-`ACTIVE` statuses) — see section 10.
- `/api/messaging/conversations` — `GET /` (this user's inbox, paginated),
  `GET /:conversationId` (thread header detail), `GET /:conversationId/messages`
  (paginated, newest-first), `POST /` (start or reuse a thread + send the first
  message), `PATCH /:conversationId/read`, and `GET /api/messaging/unread-count` (all
  auth-required) — see section 11. The WebSocket gateway (`/marketplace-messaging`
  namespace, same origin/port as the REST API) isn't a REST route; see section 11 for
  its `join_conversation`/`leave_conversation`/`send_message` events.

All routes under `/api` share one rate limiter (`@nestjs/throttler`): 500 req / 15 min,
keyed by IP (not by user — see section 16); `/health` and the Clerk webhook opt out via
`@SkipThrottle()`. Responses follow a consistent envelope
(`{ success, data?, message?, error?, meta? }`) via a global `ResponseInterceptor`
(wraps every controller return value) and a global `HttpExceptionFilter` (shapes every
thrown error, including `class-validator`'s validation failures and Multer's
`MulterError`, into the same envelope).

Validation is `class-validator`/`class-transformer` DTOs (one per request shape, under
each module's `dto/`) plus a global `ValidationPipe`.

**Pagination**: `GET /api/resources`, `GET /api/me/resources`,
`GET /api/me/recent-resources`, and `GET /api/me/bookmarked-resources` accept `page`/
`limit` query params (default `page=1`, `limit=10`, `limit` capped at 100) via a shared
`PaginationQueryDto` (`common/dto/pagination-query.dto.ts`) and return
`meta: { page, limit, total, totalPages, hasNextPage, hasPrevPage }` alongside `data`,
built by `common/utils/pagination.ts`. Recently-accessed and bookmarked resources are
not hard-capped at 10 overall. `MeService`'s `getUploadedResources` delegates straight
to `resourcesService.findResources({ userId })` rather than duplicating the same query,
since `GET /api/me/resources` and `GET /api/resources?userId=` are an exact duplicate.
On the frontend, `usePageParam` (`apps/web/src/hooks/use-page-param.ts`) keeps the current
page in the URL (`?page=`, consistent with how `/resources` already keeps its program/
semester filter there) and a shared `<Pagination>` component
(`apps/web/src/components/common/Pagination.tsx`) renders the numbered-pages control,
reused across `/resources`, `/library/uploads`, `/library/bookmarks`, `/library/recent`,
and another user's public profile uploads list.

## 13. File uploads

`storage/file-upload.config.ts` configures Nest's `FilesInterceptor` with in-memory
Multer storage, max 5 files per request, and a `ParseFilePipe` (`FileTypeValidator` +
`MaxFileSizeValidator`) restricting uploads to PDF, `.docx`, JPEG, PNG (`.doc` — the
legacy binary format — was accepted early on and later dropped entirely: it's a much
larger malware/macro attack surface than `.docx`, and had no inline-preview story
anyway). A resource's files can total at most 50 MB combined, however they're split up
(`MAX_RESOURCE_TOTAL_SIZE_BYTES`, also each single file's ceiling since one file can't
exceed the whole budget) — Multer/`ParseFilePipe` only see one file or one request at a
time, so the running total is enforced in `ResourcesService` instead, summed against
whatever's already on the resource before a `POST /:resourceId/files` call is allowed
through, and checked before anything is uploaded to Azure. Uploaded buffers are pushed
straight to Azure Blob Storage
(`storage/azure-blob.service.ts`) under a randomly generated blob name
(`crypto.randomUUID()` + original extension); the resulting blob URL, size, original
filename and MIME type are persisted per-file in `resource_files`. A new resource is
always created `PENDING` (see section 9) regardless of file type. No image/PDF preview
generation, virus scanning, or compression exists yet (the `compressedSize`/
`compressionMethod` columns are placeholders for future work); a client-side `.docx`
inline previewer was attempted and reverted — see `todo.md`.

## 14. Resource editing, deletion, and file management

Beyond create/read, resources can now be edited, deleted, and have their files managed
after the fact:

- `DELETE /api/resources/:resourceId` deletes the resource, removes its files from Azure
  Blob Storage, and (via the FK's cascade) their `resource_files` rows.
- `POST /api/resources/:resourceId/files` attaches one or more newly uploaded files to an
  existing resource (same Multer/Azure path as creation, up to 5 files per request —
  there's no cap on how many times this can be called, so a resource's total file *count*
  isn't hard-limited the way creation's 5-file cap might suggest; its total *size* is,
  though, see section 13).
- `DELETE /api/resources/:resourceId/files/:fileId` removes a single file (Azure blob +
  row), scoped to the given `resourceId` so a file id can't be used to reach into a
  different resource than the one the caller is authorized for.
- All of the above, plus `PATCH`, share a `ResourcesService#assertOwnership` check: if the
  resource doesn't exist or isn't owned by the requesting user, a 404 is returned either
  way (not 403), so a non-owner can't distinguish "doesn't exist" from "isn't yours."

Frontend:
- Editing moved from an in-page modal to a dedicated page,
  `/resources/r/[resourceId]/edit` (auth-required via `proxy.ts`, and further gated
  in-page to the resource's actual uploader — a signed-in non-owner sees a plain "you
  can't edit this" message instead of the form). The edit form
  (`components/forms/ResourceEditForm.tsx`) reuses the same Program -> Semester ->
  Subject cascading selects as the upload form, prefilled via `useSubjectDetails` (a
  resource's own summary only carries its offering id, not the offering's
  program/semester needed to seed those selects).
- Below the form, `ResourceFilesManager` lists current files with a per-file delete
  button plus an "Add Files" control — both act immediately as their own mutations,
  independent of the "Save Changes" button.
- `EditResourceButton`/`DeleteResourceButton` appear next to a resource's title on its
  detail page, and on each card in `/library/uploads`, only when the viewer is the
  resource's uploader (`UploadedResourceCard`'s `showOwnerActions` prop, only ever
  passed `true` from the uploads list — the same card is reused on other users' public
  profiles, where it must stay hidden).

Bugs found and fixed while building this:
- `useUpdateResource`'s success handler used to write the `PATCH` response directly into
  the resource-detail query cache via `setQueryData`. That response is just the bare
  updated row (no joined `files`/`subjectOffering`/`uploader`, unlike `GET`), so anything
  reading those fields off the cache — including the still-mounted edit page immediately
  after a save — would crash. Fixed by invalidating that cache key instead of
  overwriting it, so a complete shape is refetched via `GET` rather than a partial one
  ever being exposed.
- `Modal`'s `animate-in`/`fade-in`/`zoom-in-95` classes were dead (no such Tailwind
  plugin/utility exists in this project) — it never actually animated despite looking
  styled for it. Real `--animate-fade-in`/`--animate-scale-in` keyframes were registered
  via Tailwind v4's native `@theme` animation syntax; `Modal` also now closes on Escape
  (respecting `preventCloseOnOutsideClick`).
- `Button`'s `href` mode (renders as a `Link`) silently dropped every prop except
  `className`/`target` (e.g. `aria-label`, `onClick`) — fixed by forwarding the rest of
  the props through, after confirming no existing usage relied on that gap.
- `sonner`'s `<Toaster>` defaults its `theme` prop to `"light"` when not set, which is
  why toasts stayed white in dark mode; `LayoutWrapper` now passes
  `theme={resolvedTheme ?? "system"}` from `next-themes`.

## 15. File preview

`/resources/r/[resourceId]/files/[fileId]` previews a single file inline instead of
linking straight to a download (the link from `ResourceFileItem` used to point at a
route that never existed).

- The container is private, so the backend never hands out a permanent public URL.
  `resourcesService.getFileDownloadUrl` generates a 15-minute Azure SAS URL per request,
  with `Content-Disposition` set to `inline` (in-page preview) or `attachment` (forced
  download via the page's Download button), and the filename sanitized into the header.
  Any signed-in user can preview/download any resource's files — this endpoint
  deliberately isn't owner-gated, unlike edit/delete.
- The frontend (`useFileDownloadUrl`) always refetches on mount with `staleTime: 0`,
  since the URL genuinely expires and stale-while-revalidate caching would risk handing
  back a dead link.
- PDFs render in a plain `<iframe>`, JPEG/PNG in a plain `<img>` (next/image's optimizer
  is a poor fit for a URL that's only valid for minutes); other MIME types show a
  "download to view" message instead of attempting inline preview.
- A side panel (resource details + a switcher between the resource's other files) sits
  next to the preview and can be collapsed entirely — when hidden, it's removed from the
  layout so the preview pane takes the full width, and a small floating button
  (absolutely positioned, not part of the flex layout) brings it back.

## 16. Known discrepancies / rough edges worth knowing about

- **Rate limiting is IP-only.** A hybrid limiter (higher, per-`userId` limits for
  authenticated users; stricter per-IP limits for guests) is planned, to avoid punishing
  campus NAT/shared-IP situations (a real concern for IOE hostel/lab wifi). The current
  implementation (`@nestjs/throttler`, configured in `app.module.ts`) is a single flat
  500 req/15min limiter keyed by IP for everyone. Tracked in `todo.md`.
- **Placeholder nav destinations.** `Community` and `Alumni` still exist as nav items
  and protected routes but their pages (`apps/web/src/app/{community,alumni}/page.tsx`)
  are literally one-line placeholders with no functionality. `Market` is no longer one
  of these — it's a fully built marketplace + messaging feature now (sections 10-11);
  the `proxy.ts` matcher used to say `/marketplace(.*)` (a name that never matched the
  real `/market` route, silently leaving it unprotected) — fixed.
- **Test coverage is minimal.** `apps/server` has a starter Jest suite (`jest.config.js`,
  wired into `server.yml`'s CI job) covering a couple of pure-function modules
  (`common/utils/pagination`, `config/env.validation`) - no service/controller/repository
  tests yet. `apps/web` has no test suite at all.

## 17. Local development

Two paths, both documented in `SETUP.md`:

- **Without Docker**: `npm install` + `.env` in each of `apps/server` and `apps/web`
  separately, then `npm run db:migrate`, `npm run db:seed-programs`,
  `npm run db:seed-subjects`, `npm run start:dev` in `apps/server` and `npm run dev` in
  `apps/web`.
- **With Docker** (root `docker-compose.yml`, services `pg`, `server`, `web`): a single
  root `.env` drives everything (see `.env.example`); root `package.json` exposes
  `npm run docker:up|start|stop|down|logs` and proxied `db:*` scripts that run inside the
  `server` container via `docker compose exec`. Both app Dockerfiles run as the image's
  built-in non-root `node` user (uid/gid 1000) rather than root, since `apps/server` and
  `apps/web` are bind-mounted into their containers for live editing — running as root
  used to leave files like `.next` root-owned on the host, breaking host-side commands.

Seed data lives in `apps/server/data/{programs,subjects,subject-offerings}.json` — 13
programs (12 engineering programs + SH) and 428 subjects sourced from IOE's published
new-syllabus curriculum pages, keyed by program code so the seeders can be re-run
idempotently (`onConflictDoNothing` throughout). `db:sync-clerk-users` backfills local
`users`/`profiles` rows from a Clerk *development* instance. `db:seed-resources` seeds a
handful of sample resources for local development/testing: for every program except SH,
one subject per semester gets 5 resources, each with 5 fake files - no real uploads, no
Azure calls, just placeholder blob names/URLs/sizes. Unlike the other seeders it is not
idempotent (it doesn't check for previously seeded resources), so it assumes a clean
`resources` table.

CI (`.github/workflows/`): separate PR-check workflows for `apps/server` (lint,
typecheck, build) and `apps/web` (lint, build) that only trigger on changes under their
respective path, a `merge-gatekeeper` workflow that requires those checks to pass before
merge, and a deploy workflow for the server on push to `main`.

## 18. Where things stand, in one paragraph

The core "browse, upload, edit, and delete resources, scoped by program/semester/subject"
loop is fully built end-to-end, consistently under the "resources" name from the
database up through the UI: seeded curriculum data, a required `type` field
distinguishing notes/past questions/assessments/lab sheets/books/other,
Clerk-authenticated upload with Azure-backed file storage, and a unified `/resources`
browse page that works for guests and defaults from a signed-in user's profile when set.
Resource owners can edit a resource's details/subject, delete it entirely, or add/remove
individual files after the fact, all gated by ownership checks enforced server-side.
Personal views (recent, bookmarked, uploaded) now live under their own auth-required
`/library` space, separate from the shared `/resources` browsing/sharing surface. Any
signed-in user can preview or download a resource's files inline via short-lived signed
URLs, rather than only ever seeing a raw download link. Every list that can grow
unbounded (`/resources`, `/library/uploads`, `/library/bookmarks`, `/library/recent`, and
another user's public uploads) is now paginated, sharing one backend helper and one
frontend `<Pagination>` component. The whole site supports light/dark/system theming,
including Clerk's own hosted UI. Resources also carry a real upvote/downvote/download-
count aggregate now (section 4), replacing an old placeholder number on public profiles.
Beyond resources, a full marketplace-listings-plus-real-time-messaging feature is built
end to end (sections 10-11): post something for sale or wanted, browse/report/moderate
listings, and message a listing's poster over a WebSocket-backed chat with a live unread
badge — the project's first real-time feature and its only WebSocket usage. Community
and Alumni are still placeholder destinations with no logic yet; see `todo.md` for
what's next. The API itself was rebuilt from Express onto NestJS (same routes, same DB,
same response shapes), gaining a consistent Controller -> Service -> Repository layering
across every module, `class-validator` DTOs, and Clerk auth via a `ClerkAuthGuard`
backed by `@clerk/backend`.
