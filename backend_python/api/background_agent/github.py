"""GitHub REST/OAuth client used by the background agent."""
from __future__ import annotations

import logging
from urllib.parse import urlencode

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class GitHubError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, token: str = ''):
        self.token = token
        self.base_url = getattr(settings, 'BACKGROUND_AGENT_GITHUB_API_URL', 'https://api.github.com').rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'NEBians-Background-Agent/1.0',
        })
        if token:
            self.session.headers['Authorization'] = f'Bearer {token}'

    @staticmethod
    def authorize_url(*, state: str, redirect_uri: str) -> str:
        client_id = getattr(settings, 'BACKGROUND_AGENT_GITHUB_CLIENT_ID', '') or settings.GITHUB_CLIENT_ID
        scopes = getattr(settings, 'BACKGROUND_AGENT_GITHUB_SCOPES', 'repo workflow read:org user:email')
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': scopes,
            'state': state,
            'allow_signup': 'false',
        }
        return 'https://github.com/login/oauth/authorize?' + urlencode(params)

    @staticmethod
    def exchange_code(*, code: str, redirect_uri: str) -> tuple[str, str]:
        client_id = getattr(settings, 'BACKGROUND_AGENT_GITHUB_CLIENT_ID', '') or settings.GITHUB_CLIENT_ID
        client_secret = getattr(settings, 'BACKGROUND_AGENT_GITHUB_CLIENT_SECRET', '') or settings.GITHUB_CLIENT_SECRET
        if not client_id or not client_secret:
            raise GitHubError('Background-agent GitHub OAuth is not configured')
        response = requests.post(
            'https://github.com/login/oauth/access_token',
            json={
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'redirect_uri': redirect_uri,
            },
            headers={'Accept': 'application/json', 'User-Agent': 'NEBians-Background-Agent/1.0'},
            timeout=20,
        )
        try:
            data = response.json()
        except ValueError as exc:
            raise GitHubError('GitHub returned an invalid OAuth response') from exc
        token = data.get('access_token') or ''
        if response.status_code >= 400 or not token:
            raise GitHubError(data.get('error_description') or data.get('error') or 'GitHub OAuth token exchange failed')
        return token, data.get('scope') or ''

    def _request(self, method: str, path: str, **kwargs):
        url = path if path.startswith('http') else f'{self.base_url}{path}'
        kwargs.setdefault('timeout', 30)
        response = self.session.request(method, url, **kwargs)
        if response.status_code >= 400:
            message = ''
            try:
                payload = response.json()
                message = payload.get('message') or str(payload)
            except ValueError:
                message = response.text[:500]
            raise GitHubError(f'GitHub API {response.status_code}: {message}')
        if response.status_code == 204:
            return None, response
        try:
            return response.json(), response
        except ValueError:
            return response.text, response

    def current_user(self) -> dict:
        data, _ = self._request('GET', '/user')
        return data

    def list_repositories(self, *, page: int = 1, per_page: int = 50, query: str = '') -> list[dict]:
        params = {
            'visibility': 'all',
            'affiliation': 'owner,collaborator,organization_member',
            'sort': 'updated',
            'direction': 'desc',
            'per_page': max(1, min(per_page, 100)),
            'page': max(1, page),
        }
        repos, _ = self._request('GET', '/user/repos', params=params)
        query_l = query.strip().lower()
        if query_l:
            repos = [r for r in repos if query_l in (r.get('full_name') or '').lower()]
        return repos

    def get_repository(self, full_name: str) -> dict:
        _validate_full_name(full_name)
        data, _ = self._request('GET', f'/repos/{full_name}')
        return data

    def list_branches(self, full_name: str, *, per_page: int = 100) -> list[dict]:
        _validate_full_name(full_name)
        data, _ = self._request('GET', f'/repos/{full_name}/branches', params={'per_page': min(per_page, 100)})
        return data

    def create_pull_request(self, full_name: str, *, title: str, head: str, base: str, body: str, draft: bool = False) -> dict:
        _validate_full_name(full_name)
        data, _ = self._request('POST', f'/repos/{full_name}/pulls', json={
            'title': title[:256],
            'head': head,
            'base': base,
            'body': body,
            'draft': bool(draft),
        })
        return data

    def find_open_pull_request(self, full_name: str, *, head: str, base: str) -> dict | None:
        _validate_full_name(full_name)
        owner = full_name.split('/', 1)[0]
        data, _ = self._request('GET', f'/repos/{full_name}/pulls', params={
            'state': 'open',
            'head': f'{owner}:{head}',
            'base': base,
            'per_page': 10,
        })
        return data[0] if isinstance(data, list) and data else None


def _validate_full_name(value: str) -> None:
    parts = (value or '').split('/')
    if len(parts) != 2 or not all(parts):
        raise GitHubError('Invalid GitHub repository name')
    allowed = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.')
    if any(any(ch not in allowed for ch in part) for part in parts):
        raise GitHubError('Invalid GitHub repository name')
