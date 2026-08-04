"""
Qwen file upload — upload images, PDFs, audio, video to Alibaba Cloud OSS
via Qwen's STS token endpoint, then return file_obj dicts for message payloads.

Ported from flashy/backend/providers/qwen_utils/file_upload.py but adapted
for synchronous use with the standard `requests` library (no curl_cffi).
"""
import hashlib
import hmac
import logging
import mimetypes
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional
from urllib.parse import quote

import requests

logger = logging.getLogger(__name__)

QWEN_URL = "https://chat.qwen.ai"

_FILE_TYPE_MAP = {
    ".png": ("image", "image", "vision"),
    ".jpg": ("image", "image", "vision"),
    ".jpeg": ("image", "image", "vision"),
    ".gif": ("image", "image", "vision"),
    ".webp": ("image", "image", "vision"),
    ".bmp": ("image", "image", "vision"),
    ".svg": ("image", "image", "vision"),
    ".pdf": ("document", "file", "document"),
    ".txt": ("document", "file", "document"),
    ".doc": ("document", "file", "document"),
    ".docx": ("document", "file", "document"),
    ".mp4": ("video", "video", "video"),
    ".avi": ("video", "video", "video"),
    ".mov": ("video", "video", "video"),
    ".m4v": ("video", "video", "video"),
    ".mkv": ("video", "video", "video"),
    ".webm": ("video", "video", "video"),
    ".mp3": ("audio", "audio", "audio"),
    ".wav": ("audio", "audio", "audio"),
    ".ogg": ("audio", "audio", "audio"),
    ".flac": ("audio", "audio", "audio"),
    ".aac": ("audio", "audio", "audio"),
    ".m4a": ("audio", "audio", "audio"),
}

_file_cache: Dict[str, dict] = {}

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB per file
MAX_FILES_PER_MESSAGE = 5
ALLOWED_EXTENSIONS = set(_FILE_TYPE_MAP.keys())

# Qwen STS tokens (and the signed OSS upload URLs they mint) are short-lived.
# Cached file objects must never outlive them — otherwise the chat endpoint
# silently drops attachments (instant empty stream). 15 min is well under the
# typical STS expiry while still covering rapid retries within a run.
_CACHE_TTL = 15 * 60


def _get_cached_upload(content_hash):
    """Return a cached upload only if it is still fresh (URL not expired)."""
    entry = _file_cache.get(content_hash)
    if not entry:
        return None
    file_obj, uploaded_at = entry
    if time.time() - uploaded_at > _CACHE_TTL:
        _file_cache.pop(content_hash, None)
        return None
    return file_obj


def _put_upload(content_hash, file_obj):
    _file_cache[content_hash] = (file_obj, time.time())


def _drop_upload(content_hash):
    _file_cache.pop(content_hash, None)


def classify_file(file_name: str, mime_type: str):
    ext = os.path.splitext(file_name)[1].lower()
    if ext in _FILE_TYPE_MAP:
        return _FILE_TYPE_MAP[ext]
    return (mime_type, "file", "document")


def build_oss_headers(method: str, date_str: str, sts_data: dict, content_type: str) -> dict:
    bucket_name = sts_data.get("bucketname", "qwen-webui-prod")
    file_path = sts_data.get("file_path", "")
    access_key_id = sts_data.get("access_key_id")
    access_key_secret = sts_data.get("access_key_secret")
    security_token = sts_data.get("security_token")

    headers = {
        "Content-Type": content_type,
        "x-oss-content-sha256": "UNSIGNED-PAYLOAD",
        "x-oss-date": date_str,
        "x-oss-security-token": security_token,
        "x-oss-user-agent": "aliyun-sdk-js/6.23.0 Chrome 132.0.0.0 on Windows 10 64-bit",
    }

    headers_lower = {k.lower(): v for k, v in headers.items()}
    canonical_headers_list = []
    signed_headers_list = []
    required_headers = [
        "content-md5", "content-type", "x-oss-content-sha256",
        "x-oss-date", "x-oss-security-token", "x-oss-user-agent",
    ]

    for header_name in sorted(required_headers):
        if header_name in headers_lower:
            canonical_headers_list.append(f"{header_name}:{headers_lower[header_name]}")
            signed_headers_list.append(header_name)

    canonical_headers = "\n".join(canonical_headers_list) + "\n"
    canonical_uri = f"/{bucket_name}/{quote(file_path, safe='/')}"
    canonical_request = f"{method}\n{canonical_uri}\n\n{canonical_headers}\n\nUNSIGNED-PAYLOAD"

    date_parts = date_str.split("T")
    date_scope = f"{date_parts[0]}/ap-southeast-1/oss/aliyun_v4_request"
    string_to_sign = (
        f"OSS4-HMAC-SHA256\n{date_str}\n{date_scope}\n"
        f"{hashlib.sha256(canonical_request.encode()).hexdigest()}"
    )

    def sign(key, msg):
        return hmac.new(key, msg.encode() if isinstance(msg, str) else msg, hashlib.sha256).digest()

    date_key = sign(f"aliyun_v4{access_key_secret}".encode(), date_parts[0])
    region_key = sign(date_key, "ap-southeast-1")
    service_key = sign(region_key, "oss")
    signing_key = sign(service_key, "aliyun_v4_request")
    signature = hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()

    headers["authorization"] = (
        f"OSS4-HMAC-SHA256 Credential={access_key_id}/{date_scope},Signature={signature}"
    )
    return headers


def upload_file(
    file_path: str,
    session: requests.Session,
    headers: dict,
) -> Optional[dict]:
    if not os.path.isfile(file_path):
        logger.warning("File not found: %s", file_path)
        return None

    file_data = open(file_path, "rb").read()
    file_size = len(file_data)
    file_name = os.path.basename(file_path)

    if file_size > MAX_FILE_SIZE:
        logger.warning("File too large: %s (%d bytes, max %d)", file_name, file_size, MAX_FILE_SIZE)
        return None

    mime_type, _ = mimetypes.guess_type(file_name)
    if not mime_type:
        mime_type = "application/octet-stream"

    content_hash = hashlib.md5(file_data).hexdigest()
    cached = _get_cached_upload(content_hash)
    if cached is not None:
        logger.info("Using cached file: %s", file_name)
        return cached

    file_type, show_type, file_class = classify_file(file_name, mime_type)

    try:
        sts_resp = session.post(
            f"{QWEN_URL}/api/v2/files/getstsToken",
            json={
                "filename": file_name,
                "filesize": file_size,
                "filetype": mime_type,
            },
            headers=headers,
            timeout=30,
        )
        if sts_resp.status_code != 200:
            logger.warning("STS token request failed: %s", sts_resp.status_code)
            return None

        sts_json = sts_resp.json()
        if not sts_json.get("success"):
            logger.warning("STS token error: %s", sts_json)
            return None

        data = sts_json.get("data", {})
        file_url = data.get("file_url", "")
        file_id = data.get("file_id", "")

        date_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        oss_headers = build_oss_headers("PUT", date_str, data, mime_type)

        upload_resp = session.put(
            file_url.split("?")[0],
            data=file_data,
            headers=oss_headers,
            timeout=60,
        )
        if upload_resp.status_code not in (200, 204):
            logger.warning("File upload to OSS failed: %s", upload_resp.status_code)
            return None

        parse_status = None

        now_ms = int(time.time() * 1000)
        
        meta_dict = {
            "name": file_name,
            "size": file_size,
            "content_type": mime_type,
        }
        if parse_status:
            meta_dict["parse_meta"] = {"parse_status": parse_status}

        file_obj = {
            "type": show_type,
            "file": {
                "created_at": now_ms,
                "data": {},
                "filename": file_name,
                "hash": None,
                "id": file_id,
                "meta": meta_dict,
                "update_at": now_ms,
                "type": mime_type,
            },
            "id": file_id,
            "url": file_url,
            "name": file_name,
            "collection_name": "",
            "progress": 0,
            "status": "uploaded",
            "greenNet": "success",
            "size": file_size,
            "error": "",
            "itemId": str(uuid.uuid4()),
            "file_type": mime_type,
            "showType": show_type,
            "file_class": file_class,
            "uploadTaskId": str(uuid.uuid4()),
        }

        _put_upload(content_hash, file_obj)
        logger.info("File uploaded: %s (%d bytes, id=%s)", file_name, file_size, file_id)
        return file_obj

    except Exception as e:
        logger.exception("File upload error: %s", e)
        return None


def upload_file_from_bytes(
    file_name: str,
    file_data: bytes,
    session: requests.Session,
    headers: dict,
) -> Optional[dict]:
    """Upload a file from raw bytes (e.g. from a Django UploadedFile) to Qwen OSS."""
    file_size = len(file_data)
    if file_size > MAX_FILE_SIZE:
        logger.warning("File too large: %s (%d bytes, max %d)", file_name, file_size, MAX_FILE_SIZE)
        return None

    mime_type, _ = mimetypes.guess_type(file_name)
    if not mime_type:
        mime_type = "application/octet-stream"

    content_hash = hashlib.md5(file_data).hexdigest()
    cached = _get_cached_upload(content_hash)
    if cached is not None:
        logger.info("Using cached file: %s", file_name)
        return cached

    file_type, show_type, file_class = classify_file(file_name, mime_type)

    try:
        sts_resp = session.post(
            f"{QWEN_URL}/api/v2/files/getstsToken",
            json={
                "filename": file_name,
                "filesize": file_size,
                "filetype": mime_type,
            },
            headers=headers,
            timeout=30,
        )
        if sts_resp.status_code != 200:
            logger.warning("STS token request failed: %s", sts_resp.status_code)
            return None

        sts_json = sts_resp.json()
        if not sts_json.get("success"):
            logger.warning("STS token error: %s", sts_json)
            return None

        data = sts_json.get("data", {})
        file_url = data.get("file_url", "")
        file_id = data.get("file_id", "")

        date_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        oss_headers = build_oss_headers("PUT", date_str, data, mime_type)

        upload_resp = session.put(
            file_url.split("?")[0],
            data=file_data,
            headers=oss_headers,
            timeout=60,
        )
        if upload_resp.status_code not in (200, 204):
            logger.warning("File upload to OSS failed: %s", upload_resp.status_code)
            return None

        parse_status = None

        now_ms = int(time.time() * 1000)
        
        meta_dict = {
            "name": file_name,
            "size": file_size,
            "content_type": mime_type,
        }
        if parse_status:
            meta_dict["parse_meta"] = {"parse_status": parse_status}

        file_obj = {
            "type": show_type,
            "file": {
                "created_at": now_ms,
                "data": {},
                "filename": file_name,
                "hash": None,
                "id": file_id,
                "meta": meta_dict,
                "update_at": now_ms,
                "type": mime_type,
            },
            "id": file_id,
            "url": file_url,
            "name": file_name,
            "collection_name": "",
            "progress": 0,
            "status": "uploaded",
            "greenNet": "success",
            "size": file_size,
            "error": "",
            "itemId": str(uuid.uuid4()),
            "file_type": mime_type,
            "showType": show_type,
            "file_class": file_class,
            "uploadTaskId": str(uuid.uuid4()),
        }

        _put_upload(content_hash, file_obj)
        logger.info("File uploaded from bytes: %s (%d bytes, id=%s)", file_name, file_size, file_id)
        return file_obj

    except Exception as e:
        logger.exception("File upload from bytes error: %s", e)
        return None


PARSE_POLL_INTERVAL = 2
PARSE_MAX_WAIT = 120


def parse_file(file_id: str, session: requests.Session, headers: dict) -> bool:
    """Trigger Qwen's internal file parsing (OCR for PDFs, etc.).
    
    Returns True if parsing was triggered successfully.
    """
    try:
        resp = session.post(
            f"{QWEN_URL}/api/v2/files/parse",
            json={"file_id": file_id},
            headers=headers,
            timeout=30,
        )
        if resp.status_code != 200:
            logger.warning("Parse trigger failed for %s: %s", file_id, resp.status_code)
            return False
        data = resp.json()
        if not data.get("success"):
            logger.warning("Parse trigger error for %s: %s", file_id, data)
            return False
        logger.info("Parse triggered for file %s", file_id)
        return True
    except Exception as e:
        logger.warning("Parse trigger exception for %s: %s", file_id, e)
        return False


def wait_for_parse(file_id: str, session: requests.Session, headers: dict,
                   interval: float = PARSE_POLL_INTERVAL, max_wait: float = PARSE_MAX_WAIT) -> bool:
    """Poll parse status until success or timeout.
    
    Returns True if parsing completed successfully, False otherwise.
    """
    import time as _time
    elapsed = 0.0
    while elapsed < max_wait:
        try:
            resp = session.post(
                f"{QWEN_URL}/api/v2/files/parse/status",
                json={"file_id_list": [file_id]},
                headers=headers,
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("data", [])
                if items and len(items) > 0:
                    status = items[0].get("status", "")
                    if status == "success":
                        logger.info("Parse completed for file %s", file_id)
                        return True
                    if status in ("failed", "error"):
                        err = items[0].get("error_msg", "")
                        logger.warning("Parse failed for file %s: %s", file_id, err)
                        return False
        except Exception as e:
            logger.warning("Parse status poll exception for %s: %s", file_id, e)
        _time.sleep(interval)
        elapsed += interval
    logger.warning("Parse timed out for file %s after %.0fs", file_id, max_wait)
    return False