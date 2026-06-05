"""Compatibility exports for views.

The historical monolith has been split into focused modules.
Importing from this module remains supported so existing URL configs,
tests, and external code do not need to change.
"""
from .view_helpers import *  # noqa: F401,F403
from .views_auth import *  # noqa: F401,F403
from .views_users import *  # noqa: F401,F403
from .views_resources import *  # noqa: F401,F403
from .views_forum import *  # noqa: F401,F403
from .views_misc import *  # noqa: F401,F403

__all__ = [name for name in globals() if not name.startswith("_")]
