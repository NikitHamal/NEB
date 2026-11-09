# TODO

Planned work and known rough edges, in no strict order. Check items off as they land;
add new ones as they come up. Keep entries short — link to an issue/PR instead of writing
essays here once something is actively being worked on.

## Backend

- [ ] Replace the flat IP-keyed rate limiter with a hybrid one: higher limits keyed by
      `userId` for authenticated requests, stricter limits keyed by IP for guests. Needed
      because campus/hostel wifi NATs put many students behind one IP.
- [ ] Add a `@socket.io/redis-adapter` if the API is ever horizontally scaled - the
      marketplace-messaging gateway's in-memory adapter only broadcasts within one
      server process today.

## Frontend

- [ ] Replace free-text error matching with structured error codes: have the server
      return a stable code (e.g. `RESOURCE_DUPLICATE_VOTE`) alongside the message, and
      map codes to user-facing copy in `apps/web/src/lib/errors.ts` instead of
      classifying by message text/HTTP status.
- [ ] Build out the placeholder destinations: Community, Alumni —
      both currently one-line stub pages linked from the nav.

## Housekeeping

- [ ] Extend API test coverage beyond the current two pure-function suites
      (`common/utils/pagination`, `config/env.validation`) - service/controller/repository
      tests need either `@nestjs/testing` + mocked Drizzle, or a real test database.
      `apps/web` still has no test suite at all.