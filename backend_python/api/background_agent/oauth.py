"""GitHub OAuth for the background agent, reusing the main app's callback URL.

The agent authorizes with broad repository scopes (``repo workflow read:org
user:email``) but redirects back through the site's existing
``/auth/github/callback/`` endpoint (one registered redirect URI in the GitHub
OAuth App). The callback recognises the ``bg::`` state marker and hands the
code here so the token is stored against the signed-in platform admin's
credential. Because the credential is keyed to the platform account, the same
admin never re-authorizes when signing in from another device.
"""
from __future__ import annotations

from urllib.parse import urlencode

from django.conf import settings

from api.background_agent.crypto import encrypt_secret
from api.background_agent.github import GitHubClient, GitHubError
from api.models import BackgroundAgentCredential
from api.utils import now_ms

STATE_PREFIX = 'bg::'
SCOPES = 'repo workflow read:org user:email'


def build_authorize_url(*, state: str, redirect_uri: str) -> str:
    """Authorize URL with broad agent scopes, targeting the shared callback."""
    client_id = getattr(settings, 'BACKGROUND_AGENT_GITHUB_CLIENT_ID', '') or settings.GITHUB_CLIENT_ID
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': SCOPES,
        'state': state,
        'allow_signup': 'false',
    }
    return 'https://github.com/login/oauth/authorize?' + urlencode(params)


def make_state(admin_id) -> str:
    from django.core.signing import TimestampSigner
    signed = TimestampSigner(salt='background-agent-github-oauth').sign(str(admin_id))
    return STATE_PREFIX + signed


def parse_state(state: str):
    """Return the admin id encoded in a ``bg::`` state, or None if invalid."""
    from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
    if not state or not state.startswith(STATE_PREFIX):
        return None
    try:
        return TimestampSigner(salt='background-agent-github-oauth').unsign(
            state[len(STATE_PREFIX):], max_age=600,
        )
    except (BadSignature, SignatureExpired):
        return None


def exchange_and_store(admin_user, *, code: str, redirect_uri: str):
    """Exchange the OAuth code for a token and persist it on the admin's credential.

    Returns ``(github_login, None)`` on success or ``(None, error_message)``.
    """
    if not code:
        return None, 'Missing authorization code.'
    try:
        token, scopes = GitHubClient.exchange_code(code=code, redirect_uri=redirect_uri)
        github_user = GitHubClient(token).current_user()
    except GitHubError as exc:
        return None, str(exc)
    now = now_ms()
    credential, _ = BackgroundAgentCredential.objects.get_or_create(
        admin_user=admin_user,
        defaults={'created_at': now},
    )
    credential.github_user_id = github_user.get('id') or 0
    credential.github_login = github_user.get('login') or ''
    credential.github_avatar_url = github_user.get('avatar_url') or ''
    credential.encrypted_access_token = encrypt_secret(token)
    credential.token_scopes = scopes
    credential.updated_at = now
    credential.last_validated_at = now
    credential.revoked_at = 0
    credential.save(update_fields=[
        'github_user_id', 'github_login', 'github_avatar_url',
        'encrypted_access_token', 'token_scopes', 'updated_at',
        'last_validated_at', 'revoked_at',
    ])
    return github_user.get('login') or 'account', None
