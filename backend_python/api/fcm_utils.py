import os
import json
import logging
import requests
import concurrent.futures
from django.conf import settings
from django.core.cache import cache
from django.db import close_old_connections

logger = logging.getLogger(__name__)

FCM_TOKEN_CACHE_KEY = 'fcm_access_token'
FCM_PROJECT_ID_CACHE_KEY = 'fcm_project_id'

def get_fcm_access_token_and_project_id():
    """
    Load FCM access token and project_id. Uses Django cache to avoid repeated requests.
    Returns (access_token, project_id) or (None, None) if not available.
    """
    token = cache.get(FCM_TOKEN_CACHE_KEY)
    project_id = cache.get(FCM_PROJECT_ID_CACHE_KEY)
    if token and project_id:
        return token, project_id

    service_account_path = os.environ.get('FIREBASE_SERVICE_ACCOUNT_PATH')
    if not service_account_path:
        service_account_path = settings.BASE_DIR / 'firebase-service-account.json'

    if not os.path.exists(service_account_path):
        logger.warning("FCM: firebase-service-account.json not found at %s. Push notifications disabled.", service_account_path)
        return None, None

    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request

        with open(service_account_path, 'r') as f:
            data = json.load(f)
            project_id = data.get('project_id')

        if not project_id:
            logger.error("FCM: firebase-service-account.json is missing 'project_id'")
            return None, None

        creds = service_account.Credentials.from_service_account_file(
            str(service_account_path),
            scopes=['https://www.googleapis.com/auth/firebase.messaging']
        )
        creds.refresh(Request())
        token = creds.token

        # Access token lasts 1 hour. Cache it for 55 minutes to be safe.
        cache.set(FCM_TOKEN_CACHE_KEY, token, 3300)
        cache.set(FCM_PROJECT_ID_CACHE_KEY, project_id, 3300)
        return token, project_id

    except Exception as e:
        logger.exception("FCM: Failed to load credentials or refresh token: %s", str(e))
        return None, None

def send_fcm_message(tokens, title, body, data=None):
    """
    Sends FCM message to a list of registration tokens.
    Spawns background threads so that it doesn't block the Django request thread.
    """
    if not tokens:
        return
    if isinstance(tokens, str):
        tokens = [tokens]

    # Spawn thread to run the send loop in the background
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    executor.submit(_send_fcm_batch, tokens, title, body, data)

def _send_fcm_batch(tokens, title, body, data=None):
    close_old_connections()
    try:
        token, project_id = get_fcm_access_token_and_project_id()
        if not token or not project_id:
            return

        url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # Ensure all data values are string types
        fcm_data = {}
        if data:
            for k, v in data.items():
                if v is not None:
                    fcm_data[str(k)] = str(v)

        session = requests.Session()
        for fcm_token in tokens:
            payload = {
                "message": {
                    "token": fcm_token,
                    "notification": {
                        "title": title,
                        "body": body,
                    }
                }
            }
            if fcm_data:
                payload["message"]["data"] = fcm_data

            try:
                resp = session.post(url, json=payload, headers=headers, timeout=5)
                if resp.status_code == 200:
                    logger.debug("FCM: Successfully sent to token %s...", fcm_token[:15])
                elif resp.status_code in (404, 410) or (resp.status_code == 403 and "SENDER_ID_MISMATCH" in resp.text):
                    logger.info("FCM: Token is expired/invalid/mismatched (status %d). Deleting from database.", resp.status_code)
                    from api.models import FCMToken
                    FCMToken.objects.filter(token=fcm_token).delete()
                else:
                    logger.error("FCM: Error response (status %d): %s", resp.status_code, resp.text)
            except Exception as e:
                logger.error("FCM: Request failed for token: %s", str(e))
    finally:
        close_old_connections()


_PRUNE_CODES = {'UNREGISTERED', 'SENDER_ID_MISMATCH'}


def _classify(resp):
    """Short, stable label for one FCM response (used in campaign error breakdowns)."""
    if resp.status_code == 200:
        return True, 'ok'
    code = ''
    try:
        err = (resp.json() or {}).get('error', {})
        for d in err.get('details', []) or []:
            if d.get('errorCode'):
                code = d['errorCode']
                break
        code = code or err.get('status', '')
    except Exception:  # noqa: BLE001
        pass
    if resp.status_code in (404, 410):
        code = code or 'UNREGISTERED'
    if resp.status_code == 403 and 'SENDER_ID_MISMATCH' in resp.text:
        code = 'SENDER_ID_MISMATCH'
    return False, (code or f'HTTP_{resp.status_code}').lower()


def send_fcm_detailed(tokens, title, body, data=None, workers=8):
    """Send now, wait, and report. Returns {token: (accepted: bool, code: str)}.

    Dead tokens (unregistered, wrong sender) are removed here so every caller prunes the same way.
    `code` is 'ok' or a lower-case reason such as 'unregistered', 'quota_exceeded', 'timeout',
    'no_credentials'."""
    tokens = list(dict.fromkeys(t for t in (tokens or []) if t))
    if not tokens:
        return {}
    access, project_id = get_fcm_access_token_and_project_id()
    if not access or not project_id:
        return {t: (False, 'no_credentials') for t in tokens}
    url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
    headers = {"Authorization": f"Bearer {access}", "Content-Type": "application/json"}
    fcm_data = {str(k): str(v) for k, v in (data or {}).items() if v is not None}
    results, dead = {}, []

    def one(tok):
        payload = {"message": {"token": tok, "notification": {"title": title, "body": body}}}
        if fcm_data:
            payload["message"]["data"] = fcm_data
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=8)
            ok, code = _classify(resp)
            if not ok and code.upper() in _PRUNE_CODES:
                dead.append(tok)
            return tok, (ok, code)
        except requests.Timeout:
            return tok, (False, 'timeout')
        except Exception as exc:  # noqa: BLE001
            logger.error("FCM: request failed: %s", exc)
            return tok, (False, 'network')

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, min(workers, len(tokens)))) as pool:
        for tok, res in pool.map(one, tokens):
            results[tok] = res
    if dead:
        from api.models import FCMToken
        FCMToken.objects.filter(token__in=dead).delete()
    return results
