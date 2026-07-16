"""Compatibility exports for views.

The historical monolith has been split into focused modules.
Importing from this module remains supported so existing URL configs,
tests, and external code do not need to change.
"""
from .view_helpers import *  # noqa: F401,F403
from .views_public import *  # noqa: F401,F403
from .views_forum import *  # noqa: F401,F403
from .views_profile import *  # noqa: F401,F403
from .views_auth import *  # noqa: F401,F403
from .views_ajax import *  # noqa: F401,F403
from .views_notifications import *  # noqa: F401,F403
from .views_admin import *  # noqa: F401,F403
from .views_background_agent import *  # noqa: F401,F403
from .views_arena import *  # noqa: F401,F403
from .views_study_lab import *  # noqa: F401,F403
from .views_interactive import *  # noqa: F401,F403
from .views_news import *  # noqa: F401,F403
from .views_admin_news import *  # noqa: F401,F403
from .views_results import *  # noqa: F401,F403

__all__ = [name for name in globals() if not name.startswith("_")]
