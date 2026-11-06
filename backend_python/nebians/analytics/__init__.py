"""First-party, cookie-less, privacy-preserving analytics.

    rules.py    pure classification rules (bots, referrers, pages, visitor ids)
    events.py   request -> event dict (shared by middleware and the app endpoint)
    writer.py   bounded queue + worker: sessions, geo, INSERT, off the request path
    report.py   everything the admin Analytics page reads

See docs/ANALYTICS.md for the data model and the privacy decisions.
"""
from .events import event_from_request, is_trackable_request  # noqa: F401
from .writer import submit  # noqa: F401
