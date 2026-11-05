import base64
import json
import uuid

from django.core.cache import cache

ART_TTL = 24 * 3600


def _pack(obj):
    raw = json.dumps(obj).encode("utf-8")
    return base64.b64encode(raw)


def put_artifact(owner_id, name, mime, data):
    token = uuid.uuid4().hex[:20]
    payload = {
        "owner": str(owner_id),
        "name": str(name)[:150],
        "mime": mime or "application/octet-stream",
        "b64": base64.b64encode(data or b"").decode("ascii"),
    }
    cache.set(f"lazy_art:{token}", _pack(payload), ART_TTL)
    return token


