import base64
import json
import uuid

from django.core.cache import cache

SRC_TTL = 6 * 3600
ART_TTL = 24 * 3600


def _pack(obj):
    raw = json.dumps(obj).encode("utf-8")
    return base64.b64encode(raw)


def _unpack(blob):
    try:
        val = json.loads(base64.b64decode(blob))
        return val if isinstance(val, dict) else None
    except Exception:
        return None


def put_source(owner_id, name, kind, data):
    src_id = uuid.uuid4().hex[:16]
    payload = {
        "owner": str(owner_id),
        "name": str(name)[:120],
        "kind": kind,
        "b64": base64.b64encode(data or b"").decode("ascii"),
    }
    try:
        cache.set(f"lazy_src:{src_id}", _pack(payload), SRC_TTL)
    except Exception:
        return ""
    return src_id


def get_source(src_id, owner_id):
    if not src_id:
        return None
    try:
        blob = cache.get(f"lazy_src:{src_id}")
    except Exception:
        return None
    val = _unpack(blob) if blob else None
    if not val:
        return None
    if str(val.get("owner") or "") != str(owner_id):
        return None
    data = val.get("b64") or ""
    try:
        raw = base64.b64decode(data)
    except Exception:
        return None
    return {"name": val.get("name", "file"), "kind": val.get("kind"), "data": raw}


def peek_source(src_id, owner_id):
    if not src_id:
        return None
    try:
        blob = cache.get(f"lazy_src:{src_id}")
    except Exception:
        return None
    val = _unpack(blob) if blob else None
    if not val or str(val.get("owner") or "") != str(owner_id):
        return None
    return {"name": val.get("name", "file"), "kind": val.get("kind"), "size": len(val.get("b64") or "")}


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


def get_artifact(token):
    if not token:
        return None
    try:
        blob = cache.get(f"lazy_art:{token}")
    except Exception:
        return None
    val = _unpack(blob) if blob else None
    if not val:
        return None
    try:
        raw = base64.b64decode(val.get("b64") or "")
    except Exception:
        return None
    return {"owner": str(val.get("owner") or ""), "name": val.get("name", "file"), "mime": val.get("mime"), "data": raw}