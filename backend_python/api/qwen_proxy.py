"""
Qwen AI Proxy â€” calls chat.qwen.ai directly by spoofing a browser session.

Ported from flashy/backend/providers/qwen_utils/ (fingerprint, cookies, bx-ua)
but simplified for synchronous use with the standard `requests` library.

No API key needed â€” this mimics a real Chrome browser session.
"""
import base64
import hashlib
import json
import logging
import random
import re
import threading
import time
import uuid

# Prefer curl_cffi for TLS fingerprint spoofing (bypasses Aliyun WAF on chat.qwen.ai).
# Fall back to plain requests if curl_cffi is not installed on the server.
try:
    from curl_cffi.requests import Session as _CurlSession
    _USE_CURL_CFFI = True
except ImportError:
    import requests as _requests
    _USE_CURL_CFFI = False

import requests  # kept for midtoken helper which uses a plain requests.Session

logger = logging.getLogger(__name__)

QWEN_URL = "https://chat.qwen.ai"

# Optional HTTP proxy to bypass Aliyun WAF IP blocks.
# Set QWEN_PROXY_URL in the server .env, e.g.:
#   QWEN_PROXY_URL=http://user:pass@proxyhost:port
import os as _os
QWEN_PROXY_URL = _os.environ.get("QWEN_PROXY_URL") or None


def _check_waf_response(resp):
    """Return an error string if the response looks like a WAF/captcha block."""
    if resp.status_code == 403:
        return "Access forbidden (WAF)"
    if resp.status_code in (503, 520, 521, 522, 523, 524):
        return f"WAF/CDN error (HTTP {resp.status_code})"
    if resp.status_code == 200:
        ct = resp.headers.get("content-type", "")
        if "text/html" in ct:
            try:
                text = (resp.text if hasattr(resp, "text")
                        else resp.content.decode("utf-8", "replace"))
                if any(k in text for k in ("aliyun_waf_aa", "captcha", "Challenge")):
                    return "Aliyun WAF JS challenge"
            except Exception:
                pass
    return None


# ========================= Fingerprint Generation =========================

SCREEN_PRESETS = {
    "1920x1080": "1920|1080|283|1080|158|0|1920|1080|1920|922|0|0",
    "1470x956":  "1470|956|283|797|158|0|1470|956|1470|798|0|0",
    "2560x1440": "2560|1440|283|1440|158|0|2560|1440|2560|1282|0|0",
}

PLATFORM_PRESETS = {
    "macIntel": {
        "platform": "MacIntel",
        "webglRenderer": (
            "ANGLE (Apple, ANGLE Metal Renderer: Apple M4, Unspecified Version)"
            "|Google Inc. (Apple)"
        ),
        "vendor": "Google Inc.",
    },
    "macM1": {
        "platform": "MacIntel",
        "webglRenderer": (
            "ANGLE (Apple, ANGLE Metal Renderer: Apple M1, Unspecified Version)"
            "|Google Inc. (Apple)"
        ),
        "vendor": "Google Inc.",
    },
    "win64": {
        "platform": "Win32",
        "webglRenderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)|Google Inc. (NVIDIA)",
        "vendor": "Google Inc.",
    },
}

HASH_FIELDS = {
    16: "split",
    17: "full",
    18: "full",
    31: "full",
    34: "full",
    36: "full",
}


def _generate_device_id():
    return "".join(random.choice("0123456789abcdef") for _ in range(20))


def _generate_hash():
    return random.randint(0, 0xFFFFFFFF)


_SCREEN_LIST = list(SCREEN_PRESETS.values())
_PLATFORM_LIST = ["macIntel", "macM1", "win64"]


def generate_fingerprint(options=None):
    if options is None:
        options = {}

    # Default to MacIntel + zh-CN â€” looks like the typical Qwen web user,
    # improves WAF bypass rate vs. Win32 + en-US.
    platform_key = options.get("platform") or random.choice(["macIntel", "macM1"])
    preset = PLATFORM_PRESETS.get(platform_key, PLATFORM_PRESETS["macIntel"])

    config = {
        "deviceId": _generate_device_id(),
        "sdkVersion": "websdk-2.3.15d",
        "initTimestamp": str(int(time.time() * 1000)),
        "field3": "91",
        "field4": "1|15",
        "language": "zh-CN",
        "timezoneOffset": "-480",
        "colorDepth": "16705151|12791",
        "screenInfo": random.choice(_SCREEN_LIST),
        "field9": "5",
        "platform": preset["platform"],
        "field11": "10",
        "webglRenderer": preset["webglRenderer"],
        "field13": "30|30",
        "field14": "0",
        "field15": "28",
        "pluginCount": "5",
        "vendor": preset["vendor"],
        "field29": "8",
        "touchInfo": "-1|0|0|0|0",
        "field32": "11",
        "field35": "0",
        "mode": "P",
    }
    config.update(options.get("custom", {}))

    current_timestamp = int(time.time() * 1000)
    plugin_hash = _generate_hash()
    canvas_hash = _generate_hash()
    ua_hash1 = _generate_hash()
    ua_hash2 = _generate_hash()
    url_hash = _generate_hash()
    doc_hash = random.randint(10, 100)

    fields = [
        config["deviceId"], config["sdkVersion"], config["initTimestamp"],
        config["field3"], config["field4"], config["language"],
        config["timezoneOffset"], config["colorDepth"], config["screenInfo"],
        config["field9"], config["platform"], config["field11"],
        config["webglRenderer"], config["field13"], config["field14"],
        config["field15"],
        f'{config["pluginCount"]}|{plugin_hash}',
        canvas_hash, ua_hash1,
        "1", "0", "1", "0", config["mode"],
        "0", "0", "0", "416",
        config["vendor"], config["field29"], config["touchInfo"],
        ua_hash2, config["field32"], current_timestamp,
        url_hash, config["field35"], doc_hash,
    ]
    return "^".join(map(str, fields))


# ========================= LZW Compression =========================

CUSTOM_BASE64_CHARS = "DGi0YA7BemWnQjCl4_bR3f8SKIF9tUz/xhr2oEOgPpac=61ZqwTudLkM5vHyNXsVJ"


def _lzw_compress(data, bits, char_func):
    if data is None:
        return ""
    dictionary = {}
    dict_to_create = {}
    c = ""
    wc = ""
    w = ""
    enlarge_in = 2
    dict_size = 3
    num_bits = 2
    result = []
    value = 0
    position = 0

    for i in range(len(data)):
        c = data[i]
        if c not in dictionary:
            dictionary[c] = dict_size
            dict_size += 1
            dict_to_create[c] = True
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            if w in dict_to_create:
                if ord(w[0]) < 256:
                    for _ in range(num_bits):
                        value = (value << 1)
                        if position == bits - 1:
                            position = 0
                            result.append(char_func(value))
                            value = 0
                        else:
                            position += 1
                    char_code = ord(w[0])
                    for _ in range(8):
                        value = (value << 1) | (char_code & 1)
                        if position == bits - 1:
                            position = 0
                            result.append(char_func(value))
                            value = 0
                        else:
                            position += 1
                        char_code >>= 1
                else:
                    char_code = 1
                    for _ in range(num_bits):
                        value = (value << 1) | char_code
                        if position == bits - 1:
                            position = 0
                            result.append(char_func(value))
                            value = 0
                        else:
                            position += 1
                        char_code = 0
                    char_code = ord(w[0])
                    for _ in range(16):
                        value = (value << 1) | (char_code & 1)
                        if position == bits - 1:
                            position = 0
                            result.append(char_func(value))
                            value = 0
                        else:
                            position += 1
                        char_code >>= 1
                enlarge_in -= 1
                if enlarge_in == 0:
                    enlarge_in = 2 ** num_bits
                    num_bits += 1
                del dict_to_create[w]
            else:
                char_code = dictionary[w]
                for _ in range(num_bits):
                    value = (value << 1) | (char_code & 1)
                    if position == bits - 1:
                        position = 0
                        result.append(char_func(value))
                        value = 0
                    else:
                        position += 1
                    char_code >>= 1
            enlarge_in -= 1
            if enlarge_in == 0:
                enlarge_in = 2 ** num_bits
                num_bits += 1
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w != "":
        if w in dict_to_create:
            if ord(w[0]) < 256:
                for _ in range(num_bits):
                    value = (value << 1)
                    if position == bits - 1:
                        position = 0
                        result.append(char_func(value))
                        value = 0
                    else:
                        position += 1
                char_code = ord(w[0])
                for _ in range(8):
                    value = (value << 1) | (char_code & 1)
                    if position == bits - 1:
                        position = 0
                        result.append(char_func(value))
                        value = 0
                    else:
                        position += 1
                    char_code >>= 1
            else:
                char_code = 1
                for _ in range(num_bits):
                    value = (value << 1) | char_code
                    if position == bits - 1:
                        position = 0
                        result.append(char_func(value))
                        value = 0
                    else:
                        position += 1
                    char_code = 0
                char_code = ord(w[0])
                for _ in range(16):
                    value = (value << 1) | (char_code & 1)
                    if position == bits - 1:
                        position = 0
                        result.append(char_func(value))
                        value = 0
                    else:
                        position += 1
                    char_code >>= 1
            enlarge_in -= 1
            if enlarge_in == 0:
                enlarge_in = 2 ** num_bits
                num_bits += 1
            del dict_to_create[w]
        else:
            char_code = dictionary[w]
            for _ in range(num_bits):
                value = (value << 1) | (char_code & 1)
                if position == bits - 1:
                    position = 0
                    result.append(char_func(value))
                    value = 0
                else:
                    position += 1
                char_code >>= 1
            enlarge_in -= 1
            if enlarge_in == 0:
                enlarge_in = 2 ** num_bits
                num_bits += 1

    char_code = 2
    for _ in range(num_bits):
        value = (value << 1) | (char_code & 1)
        if position == bits - 1:
            position = 0
            result.append(char_func(value))
            value = 0
        else:
            position += 1
        char_code >>= 1

    while True:
        value = (value << 1)
        if position == bits - 1:
            result.append(char_func(value))
            break
        position += 1

    return "".join(result)


def _custom_encode(data, url_safe=True):
    if data is None:
        return ""
    compressed = _lzw_compress(data, 6, lambda index: CUSTOM_BASE64_CHARS[index])
    if not url_safe:
        mod = len(compressed) % 4
        if mod == 1:
            return compressed + "==="
        if mod == 2:
            return compressed + "=="
        if mod == 3:
            return compressed + "="
    return compressed


# ========================= Cookie Generation =========================

def generate_cookies(fingerprint=None):
    if fingerprint is None:
        fingerprint = generate_fingerprint()
    fields = fingerprint.split("^")
    processed = list(fields)
    current_timestamp = int(time.time() * 1000)
    for idx, typ in HASH_FIELDS.items():
        if idx >= len(processed):
            continue
        if typ == "split":
            val = str(processed[idx])
            parts = val.split("|")
            if len(parts) == 2:
                processed[idx] = f"{parts[0]}|{_generate_hash()}"
        elif typ == "full":
            if idx == 36:
                processed[idx] = random.randint(10, 100)
            else:
                processed[idx] = _generate_hash()
    if 33 < len(processed):
        processed[33] = current_timestamp

    ssxmod_itna_data = "^".join(map(str, processed))
    ssxmod_itna = "1-" + _custom_encode(ssxmod_itna_data, True)

    ssxmod_itna2_data = "^".join(map(str, [
        processed[0], processed[1], processed[23],
        0, "", 0, "", "", 0, 0,
        processed[32], processed[33],
        0, 0, 0, 0, 0
    ]))
    ssxmod_itna2 = "1-" + _custom_encode(ssxmod_itna2_data, True)

    return {
        "ssxmod_itna": ssxmod_itna,
        "ssxmod_itna2": ssxmod_itna2,
        "rawData": ssxmod_itna_data,
        "timestamp": current_timestamp,
    }


# ========================= bx-ua Generation =========================

def generate_bx_ua(fingerprint):
    if not fingerprint:
        return ""
    try:
        version = "231"
        timestamp = int(time.time() * 1000)
        fields = fingerprint.split("^")
        payload = {
            "v": version,
            "ts": timestamp,
            "fp": fingerprint,
            "d": {
                "deviceId": fields[0] if len(fields) > 0 else "",
                "sdkVer": fields[1] if len(fields) > 1 else "",
                "lang": fields[5] if len(fields) > 5 else "",
                "tz": fields[6] if len(fields) > 6 else "",
                "platform": fields[10] if len(fields) > 10 else "",
                "renderer": fields[12] if len(fields) > 12 else "",
                "mode": fields[23] if len(fields) > 23 else "",
                "vendor": fields[28] if len(fields) > 28 else "",
            },
            "rnd": random.randint(1000, 9999),
            "seq": 1,
        }
        checksum_str = f"{fingerprint}{timestamp}{payload['rnd']}"
        payload["cs"] = hashlib.md5(checksum_str.encode()).hexdigest()[:8]
        payload_json = json.dumps(payload, separators=(',', ':'))
        seed_hash = hashlib.sha256(fingerprint.encode()).digest()
        key = seed_hash[:16]
        iv = seed_hash[16:32]
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(payload_json.encode(), AES.block_size))
        encrypted_b64 = base64.b64encode(encrypted).decode()
        return f"{version}!{encrypted_b64}"
    except ImportError:
        logger.warning("pycryptodome not installed, skipping bx-ua generation")
        return ""
    except Exception as e:
        logger.warning(f"Failed to generate bx-ua: {e}")
        return ""


# ========================= Session Headers =========================

def build_session_headers(bx_ua=""):
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": QWEN_URL,
        "referer": f"{QWEN_URL}/",
        "sec-ch-ua": '"Google Chrome";v="138", "Chromium";v="138", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        ),
        "x-requested-with": "XMLHttpRequest",
        "source": "web",
        "version": "0.2.63",
        "X-Accel-Buffering": "no",
    }
    if bx_ua:
        headers["bx-ua"] = bx_ua
    return headers


# ========================= Midtoken =========================

_midtoken_cache = {"token": None, "uses": 0}


def get_midtoken(session, force_refresh=False):
    token = _midtoken_cache["token"]
    uses = _midtoken_cache["uses"]
    if token and uses < 50 and not force_refresh:
        _midtoken_cache["uses"] = uses + 1
        return token
    try:
        resp = session.get("https://sg-wum.alibaba.com/w/wu.json", timeout=10)
        resp.encoding = "utf-8"
        if resp.status_code == 200:
            match = re.search(r"(?:umx\.wu|__fycb)\('([^']+)'\)", resp.text)
            if match:
                _midtoken_cache["token"] = match.group(1)
                _midtoken_cache["uses"] = 1
                return match.group(1)
    except Exception as e:
        logger.warning(f"Error fetching midtoken: {e}")
    return None


# ========================= Session Management (Pool) =========================
#
# We maintain a pool of browser-mimicking sessions.  Each session has a unique
# fingerprint, cookies, and bx-umidtoken, so Qwen's free-tier rate limiter
# sees them as independent browsers.  Sessions are round-robin'd and retired
# after SESSION_MSG_LIMIT messages to stay well under the ~20-msg free limit.
#
# A background thread refills the pool to keep POOL_TARGET_SIZE entries warm.

_session_pool = []   # list of dicts: {session, cookies, created_at, msg_count}
_pool_lock = threading.Lock()

POOL_TARGET_SIZE = 6
SESSION_MSG_LIMIT = 14   # retire at 14 to stay under Qwen's ~20-msg per-identity cap
SESSION_TTL = 900        # 15 minutes absolute TTL
_POOL_REFILL_INTERVAL = 120
_pool_refill_thread_started = False


def _create_fresh_session():
    """Build a brand-new session with unique fingerprint and cookies.

    Uses curl_cffi with impersonate='chrome' when available so that TLS
    fingerprints match a real Chrome browser â€” this is the primary WAF
    bypass mechanism for Aliyun WAF on chat.qwen.ai.
    """
    cookies_data = generate_cookies()
    bx_ua = generate_bx_ua(cookies_data.get("rawData", ""))
    headers = build_session_headers(bx_ua)

    if _USE_CURL_CFFI:
        session = _CurlSession(impersonate="chrome", headers=headers, proxies={"https": QWEN_PROXY_URL, "http": QWEN_PROXY_URL} if QWEN_PROXY_URL else {})
    else:
        session = requests.Session()
        session.headers.update(headers)

    cookie_dict = {
        "ssxmod_itna": cookies_data["ssxmod_itna"],
        "ssxmod_itna2": cookies_data["ssxmod_itna2"],
    }
    for k, v in cookie_dict.items():
        session.cookies.set(k, v, domain="chat.qwen.ai")

    # Use a plain requests session for the midtoken fetch (curl_cffi
    # sessions are not reused across threads safely for this helper)
    midtoken_session = requests.Session()
    midtoken_session.headers.update(headers)
    midtoken = get_midtoken(midtoken_session)
    if midtoken:
        session.headers["bx-umidtoken"] = midtoken
        session.headers["bx-v"] = "2.5.36"
    session.headers["x-request-id"] = str(uuid.uuid4())

    try:
        warmup = session.get(f"{QWEN_URL}/", timeout=15, allow_redirects=True)
        logger.info(f"Qwen warmup: {warmup.status_code}")
    except Exception as e:
        logger.warning(f"Qwen warmup failed: {e}")

    return session, cookies_data


def _add_pool_entry():
    """Create a fresh session, add to pool."""
    session, cookies = _create_fresh_session()
    entry = {
        'session': session,
        'cookies': cookies,
        'created_at': time.time(),
        'msg_count': 0,
    }
    _session_pool.append(entry)
    return entry


def _prune_pool():
    """Remove expired or overused entries from pool."""
    now = time.time()
    _session_pool[:] = [
        e for e in _session_pool
        if e['msg_count'] < SESSION_MSG_LIMIT
        and (now - e['created_at']) < SESSION_TTL
    ]


def _pool_refill_loop():
    """Background thread: keep the pool at target size."""
    while True:
        time.sleep(_POOL_REFILL_INTERVAL)
        try:
            with _pool_lock:
                _prune_pool()
                need = POOL_TARGET_SIZE - len(_session_pool)
            for _ in range(need):
                try:
                    with _pool_lock:
                        _add_pool_entry()
                except Exception as e:
                    logger.error(f"Pool refill failed: {e}")
                    break
            if need > 0:
                logger.info(f"Pool refill: added {need} sessions (pool={len(_session_pool)})")
        except Exception as e:
            logger.error(f"Pool refill loop error: {e}")


def _start_refill_thread():
    global _pool_refill_thread_started
    if _pool_refill_thread_started:
        return
    _pool_refill_thread_started = True
    t = threading.Thread(target=_pool_refill_loop, daemon=True, name='qwen-pool-refill')
    t.start()
    logger.info("Qwen session pool refill thread started")


def _get_session():
    """Return the least-used session from the pool (creates one if empty)."""
    with _pool_lock:
        _prune_pool()
        if not _session_pool:
            _add_pool_entry()
        # sort by msg_count ascending so least-used session is returned
        _session_pool.sort(key=lambda e: e['msg_count'])
        winner = _session_pool[0]
        return winner['session'], winner['cookies']


def _mark_failed(session):
    """Retire a session immediately (quota error, etc.)."""
    with _pool_lock:
        before = len(_session_pool)
        _session_pool[:] = [e for e in _session_pool if e['session'] is not session]
        gone = before - len(_session_pool)
        if gone:
            logger.info(f"Session retired (pool now {len(_session_pool)})")


def _mark_used(session):
    """Increment message count for the given session."""
    with _pool_lock:
        for entry in _session_pool:
            if entry['session'] is session:
                entry['msg_count'] += 1
                break


def _reset_session():
    """Clear the entire pool (legacy helper)."""
    with _pool_lock:
        _session_pool.clear()


# Kick off the refill thread at import time (safe because it's a daemon thread)
_start_refill_thread()


# ========================= Chat API =========================

def create_chat(session, model=None, _pool_session=None):
    if model is None:
        from .qwen_utils.models import get_default_model
        model = get_default_model()
    now = int(time.time() * 1000)
    payload = {
        "title": "New Chat",
        "models": [model],
        "chat_mode": "normal",
        "chat_type": "t2t",
        "timestamp": now,
        "project_id": "",
    }
    try:
        resp = session.post(f"{QWEN_URL}/api/v2/chats/new", json=payload, timeout=30)
        waf_err = _check_waf_response(resp)
        if waf_err:
            logger.error(f"Qwen create_chat WAF blocked: {waf_err}")
            if _pool_session:
                _mark_failed(_pool_session)
            return None
        if resp.status_code != 200:
            logger.error(f"Qwen chat creation failed: {resp.status_code} {resp.text[:300]}")
            if _pool_session:
                _mark_failed(_pool_session)
            return None
        data = resp.json()
        if not data.get("success"):
            logger.error(f"Qwen chat creation unsuccessful: {data}")
            if _pool_session:
                _mark_failed(_pool_session)
            return None
        return data["data"]["id"]
    except Exception as e:
        logger.error(f"Qwen chat creation exception: {e}")
        if _pool_session:
            _mark_failed(_pool_session)
        return None


def _model_thinking_required(model_id):
    if not model_id:
        return False
    if model_id.startswith('qwen3.8'):
        # qwen3.8-max (and its preview) requires thinking — the strict JSON
        # protocol for the background agent depends on auto-thinking being on.
        return True
    try:
        from .qwen_utils.models import fetch_models
        for m in fetch_models():
            if m.get('id') == model_id and m.get('capabilities', {}).get('thinking'):
                return True
    except Exception:
        pass
    return False


def send_message(session, chat_id, message, model=None, parent_id=None,
                 max_tokens=500, uploaded_files=None, system_prompt=None,
                 _pool_session=None, thinking_mode="auto"):
    if model is None:
        from .qwen_utils.models import get_default_model
        model = get_default_model()
    if system_prompt:
        full_prompt = system_prompt + "\n\n" + message
    else:
        full_prompt = message
    msg_id = str(uuid.uuid4())
    from .qwen_utils.message_builder import build_msg_payload, build_feature_config
    mode = str(thinking_mode or "auto").strip().lower()
    if mode not in ("auto", "thinking", "fast"):
        mode = "auto"
    thinking_enabled = _model_thinking_required(model)
    if mode == "fast":
        thinking_enabled = False
    elif mode == "thinking":
        thinking_enabled = True
    elif mode == "auto":
        mode = None
    feature_config = build_feature_config(thinking_enabled=thinking_enabled, mode=mode)
    payload = build_msg_payload(
        chat_id=chat_id,
        model=model,
        full_prompt=full_prompt,
        parent_id=parent_id,
        uploaded_files=uploaded_files or [],
        chat_type="t2t",
        chat_mode="normal",
        feature_config=feature_config,
        stream=True,
    )
    try:
        resp = session.post(
            f"{QWEN_URL}/api/v2/chat/completions?chat_id={chat_id}",
            json=payload,
            timeout=120,
            stream=True,
        )
        if resp.status_code != 200:
            logger.error(f"Qwen chat completions failed: {resp.status_code} {resp.text[:300]}")
            if _pool_session:
                _mark_failed(_pool_session)
            return None
        result = _parse_stream(resp, session=_pool_session)
        if _pool_session:
            _mark_used(_pool_session)
        return result
    except Exception as e:
        logger.error(f"Qwen chat completions exception: {e}")
        return None


def _parse_stream(response, session=None):
    full_text = ""
    reasoning_text = ""
    parent_id = None
    had_quota_error = False
    raw_lines_seen = 0
    json_chunks_seen = 0
    errors_seen = []
    error_text_total = ""

    # curl_cffi's iter_lines() returns bytes (decode_unicode=True is not
    # supported), so we decode manually. plain requests returns strings.
    for raw_line in response.iter_lines():
        if isinstance(raw_line, bytes):
            line = raw_line.decode("utf-8", errors="replace")
        else:
            line = raw_line
        if not line:
            continue
        line = line.strip()
        if line.startswith(":"):
            continue
        if not line.startswith("data: "):
            continue
        raw_lines_seen += 1
        chunk_str = line[6:]
        if chunk_str == "[DONE]":
            break
        try:
            chunk = json.loads(chunk_str)
        except json.JSONDecodeError:
            continue
        json_chunks_seen += 1

        if "error" in chunk:
            err_text = str(chunk['error'])
            error_text_total += err_text
            logger.error(f"Qwen stream error: {err_text}")
            if 'quota' in err_text.lower():
                had_quota_error = True

        if "response.created" in chunk:
            resp_id = chunk.get("response.created", {}).get("response_id")
            if resp_id:
                parent_id = resp_id

        choices = chunk.get("choices", [])
        if not choices:
            continue
        choice = choices[0]
        delta = choice.get("delta", {})
        content = delta.get("content")
        phase = delta.get("phase")
        finish_reason = choice.get("finish_reason")

        if content:
            if phase == "think" or phase == "web_search":
                reasoning_text += content
            else:
                full_text += content

        if finish_reason:
            break

    if not full_text and reasoning_text:
        full_text = reasoning_text

    if had_quota_error:
        if session:
            _mark_failed(session)
            logger.info("Session retired due to quota error")
        # A quota/overload error interrupts the model's JSON protocol and the
        # stream falls back to plain narrative. Returning that garbage as if
        # it were valid would let the agent run on broken output — treat the
        # attempt as failed so the caller retries with a fresh session.
        return None

    result = full_text.strip() if full_text else None
    if result is None:
        logger.warning(
            "Qwen empty stream: raw_lines=%d json_chunks=%d errors=%s parent_id=%s",
            raw_lines_seen, json_chunks_seen, (error_text_total[:300] or 'none'), parent_id,
        )
    return result


# ========================= Public API =========================

def call_qwen(system_prompt, user_message, model="qwen3.8-max", max_tokens=500,
               file_paths=None, thinking_mode="auto"):
    """Call Qwen AI directly (no proxy needed). Returns response text or None.

    This function manages its own browser session, creating a fresh one
    when needed and rotating it on errors.

    Args:
        system_prompt: System instructions (prepended to user message).
        user_message: The user's message text.
        model: Qwen model ID (default qwen3.8-max).
        max_tokens: Rough character cap for the response.
        file_paths: Optional list of local file paths to upload to Qwen OSS.
                   Supports images, PDFs, audio, and video files.
    """
    full_message = ""
    if system_prompt:
        full_message = f"[System Instructions]\n{system_prompt}\n\n[User Message]\n{user_message}"
    else:
        full_message = user_message

    from .qwen_utils.file_upload import upload_file, MAX_FILES_PER_MESSAGE

    max_attempts = 3
    for attempt in range(max_attempts):
        session = None
        try:
            session, cookies = _get_session()
            midtoken = get_midtoken(session, force_refresh=(attempt > 0))
            if midtoken:
                session.headers["bx-umidtoken"] = midtoken
                session.headers["bx-v"] = "2.5.36"
            session.headers["x-request-id"] = str(uuid.uuid4())

            # Upload files if provided
            uploaded_files = []
            if file_paths:
                req_headers = dict(session.headers)
                for fp in file_paths[:MAX_FILES_PER_MESSAGE]:
                    file_obj = upload_file(fp, session, req_headers)
                    if file_obj:
                        uploaded_files.append(file_obj)

            chat_id = create_chat(session, model, _pool_session=session)
            if not chat_id:
                logger.warning(f"Qwen chat creation failed (attempt {attempt + 1})")
                _mark_failed(session)
                time.sleep(2 * (attempt + 1))
                continue

            result = send_message(
                session, chat_id, full_message, model, max_tokens=max_tokens,
                uploaded_files=uploaded_files if uploaded_files else None,
                _pool_session=session, thinking_mode=thinking_mode,
            )
            if result:
                logger.info(f"Qwen response received ({len(result)} chars)")
                return result

            logger.warning(f"Qwen empty response (attempt {attempt + 1})")
            _mark_failed(session)
            # A cached OSS upload may have expired mid-run (STS URLs are
            # short-lived) — the chat endpoint silently drops those
            # attachments, yielding an instant empty stream. Drop the cache
            # so the next attempt re-uploads fresh URLs.
            if file_paths:
                from .qwen_utils import file_upload as _fu
                from pathlib import Path
                for fp in file_paths[:MAX_FILES_PER_MESSAGE]:
                    try:
                        data = open(fp, "rb").read()
                        _fu._drop_upload(hashlib.md5(data).hexdigest())
                    except Exception:
                        pass
            time.sleep(2 * (attempt + 1))
        except Exception as e:
            logger.error(f"Qwen call exception (attempt {attempt + 1}): {e}")
            if session:
                _mark_failed(session)
            time.sleep(2 * (attempt + 1))

    return None