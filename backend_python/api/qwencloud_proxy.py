"""Proxy for qwencloud.com/try-ai anonymous chat (Alibaba Qwen Cloud).

Reverse of the Try-AI playground. Anonymous (no login) flow, all calls are
``POST /data/api.json`` on ``https://cs-data.qwencloud.com`` carrying an RPC
envelope ``{product:'sfm_bailian', action:'IntlBroadScopeAspnGateway',
region:'ap-southeast-1', params:JSON({Api, Data:{... , cornerstoneParam},
V:'1.0'})}`` plus ``?product=&action=&api=`` query params::

    cornerstoneParam = {domain:'www.qwencloud.com', consoleSite:'QWENCLOUD',
        console:'ONE_CONSOLE', xsp_lang:'en-US', protocol:'V2',
        productCode:'p_efm', 'X-Anonymous-Id':<16 alnum, minted per session>}

The same anonymous id is also sent as the ``x-anonymous-id`` HTTP header on
every call — the inference backend rejects predicts without it.

Per chat turn (fresh access tokens are single-use, so one is minted per
predict)::

    agentSessionRpcService.createApi  {session:{bizId:'',label,bizType:'TextGeneration'}}
    agentSessionTabRpcService.create  {sessionTabDTO:{sessionId, modelId}}
    streamGatewayConsoleService.generateAccessToken  {source:''}
    POST https://cs-stream.qwencloud.com/sse/console4Json/{accessToken}
        {messageId, data:[{type:'JSON_TEXT', value:JSON(
            {Api:'agentPredictRpcService.predict',
             Data:{predictRequest:{modelId,sessionId,tabCode,
                   contentList:[{type:'text',content}],
                   predictConfig:{modelParam:{systemMessage,top_p,temperature,
                       enable_search,enable_thinking,thinking_budget,
                       result_format:'message'},chatType:'t2t'},
                   reGenerate:False,chatLogCode,modelTypeIds,isAiCenterRequest:False},
                  cornerstoneParam}})]}

Response frames are cumulative ``messageList[0].contentList`` parts addressed
by ``jsonPath`` (``/contentList/<i>/content``); part type ``DeepThink`` is
reasoning, ``Text`` is the answer. The server closes the stream after the
final frame (no ``[DONE]`` sentinel, though one is tolerated).

Multi-turn: turns after the first reuse the same ``(session_id, tab_code)``
so the server-side tab keeps the history; only the new user message is sent.
For stateless callers a fresh tab is opened per call and the transcript is
flattened into a single prompt (same trick as geminiweb). Callers that want
server-side history can persist ``session_id``/``tab_code`` (yielded as a
``session`` chunk) and pass them back.

Auth: every cs-data call needs a ``bx-umidtoken`` header (Alibaba risk-device
token). Set ``QWENCLOUD_UMIDTOKEN`` env var; without it all calls fail with a
clear error telling the operator how to refresh it (open try-ai in a browser,
copy the ``bx-umidtoken`` request header from any ``/data/api.json`` call).
"""

import json
import logging
import os
import random
import string
import uuid
from typing import Dict, Generator, List, Optional

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

DATA_BASE = "https://cs-data.qwencloud.com"
STREAM_BASE = "https://cs-stream.qwencloud.com"
PAGE_URL = "https://www.qwencloud.com/try-ai?scene=chat"

PREDICT_API = "zeldaEasy.bmp.agentPredictRpcService.predict"
SESSION_CREATE_API = "zeldaEasy.bmp.agentSessionRpcService.createApi"
TAB_CREATE_API = "zeldaEasy.bmp.agentSessionTabRpcService.create"
TOKEN_API = "zeldaEasy.cornerstoneStreamGateway.streamGatewayConsoleService.generateAccessToken"
UMID_API = "zeldaEasy.cornerstoneStreamGateway.streamGatewayConsoleService.getXUmidNumber"

REQUEST_TIMEOUT = 300
RESPONSE_TIMEOUT = 180

DEFAULT_MODEL = "qwen3.8-max"

MODELS = [
    {"id": "qwen3.8-max", "name": "Qwen3.8 Max", "reasoning": True},
    {"id": "qwen3.7-max", "name": "Qwen3.7 Max", "reasoning": True},
    {"id": "qwen3.6-plus", "name": "Qwen3.6 Plus", "reasoning": True},
    {"id": "qwen3.6-plus-2026-04-02", "name": "Qwen3.6 Plus (2026-04-02)", "reasoning": True},
    {"id": "qwen3.7-plus", "name": "Qwen3.7 Plus", "reasoning": True},
    {"id": "qwen3.5-plus", "name": "Qwen3.5 Plus", "reasoning": True},
    {"id": "qwen3-max", "name": "Qwen3 Max", "reasoning": True},
    {"id": "qwen-plus", "name": "Qwen Plus", "reasoning": True},
    {"id": "qwen-flash", "name": "Qwen Flash", "reasoning": False},
    {"id": "qwen3-coder-plus", "name": "Qwen3 Coder Plus", "reasoning": True},
    {"id": "qwen3-coder-flash", "name": "Qwen3 Coder Flash", "reasoning": False},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_UMIDTOKEN_ENV = "QWENCLOUD_UMIDTOKEN"
_umidtoken_cache: Optional[str] = None

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def _umidtoken() -> str:
    global _umidtoken_cache
    if _umidtoken_cache:
        return _umidtoken_cache
    token = (os.environ.get(_UMIDTOKEN_ENV) or "").strip()
    if token:
        _umidtoken_cache = token
        return token
    raise RuntimeError(
        "qwencloud: no risk token configured. Set the QWENCLOUD_UMIDTOKEN "
        "environment variable to a fresh 'bx-umidtoken' request header value "
        "(open https://www.qwencloud.com/try-ai?scene=chat in a browser, send "
        "one chat, copy bx-umidtoken from any /data/api.json request)."
    )


def _new_session() -> CurlSession:
    s = CurlSession(impersonate="chrome")
    s.headers.update({
        "origin": "https://www.qwencloud.com",
        "referer": PAGE_URL,
        "user-agent": _UA,
        "accept": "application/json, text/plain, */*",
        "bx-umidtoken": _umidtoken(),
    })
    s.get(PAGE_URL, timeout=30)
    return s


def _anon_id() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=16))


def _cornerstone(anon: str) -> Dict:
    return {"domain": "www.qwencloud.com", "consoleSite": "QWENCLOUD",
            "console": "ONE_CONSOLE", "xsp_lang": "en-US",
            "protocol": "V2", "productCode": "p_efm",
            "X-Anonymous-Id": anon}


def _rpc(session: CurlSession, anon: str, api: str, data: Dict) -> Dict:
    body = {"product": "sfm_bailian", "action": "IntlBroadScopeAspnGateway",
            "sec_token": "", "region": "ap-southeast-1",
            "params": json.dumps({"Api": api,
                                  "Data": {**data, "cornerstoneParam": _cornerstone(anon)},
                                  "V": "1.0"})}
    resp = session.post(
        f"{DATA_BASE}/data/api.json",
        params={"product": "sfm_bailian", "action": "IntlBroadScopeAspnGateway", "api": api},
        data=body, headers={"x-anonymous-id": anon}, timeout=REQUEST_TIMEOUT)
    if resp.status_code != 200:
        raise RuntimeError(f"qwencloud RPC {api} HTTP {resp.status_code}: {resp.text[:200]}")
    try:
        outer = resp.json()
        inner = outer["data"]["DataV2"]["data"]
    except (ValueError, KeyError, TypeError):
        raise RuntimeError(f"qwencloud RPC {api} bad envelope: {resp.text[:200]}")
    if inner.get("codeEnum") not in (None, "SUCCESS"):
        raise RuntimeError(f"qwencloud RPC {api} error {inner.get('codeEnum')}: "
                           f"{str(inner.get('message'))[:200]}")
    payload = inner.get("data", inner)
    if isinstance(payload, dict) and payload.get("success") is False:
        raise RuntimeError(f"qwencloud RPC {api} failed: {str(payload)[:200]}")
    return payload


def _open_tab(session: CurlSession, anon: str, model: str, label: str):
    sess = _rpc(session, anon, SESSION_CREATE_API,
                {"session": {"bizId": "", "label": label[:256], "bizType": "TextGeneration"}})
    session_id = sess["sessionId"] if "sessionId" in sess else sess["data"]["sessionId"]
    tab = _rpc(session, anon, TAB_CREATE_API,
               {"sessionTabDTO": {"sessionId": session_id, "modelId": model}})
    tab_code = tab["code"] if "code" in tab else tab["data"]["code"]
    return session_id, tab_code


def _fresh_token(session: CurlSession, anon: str) -> str:
    tok = _rpc(session, anon, TOKEN_API, {"source": ""})
    return tok["accessToken"] if "accessToken" in tok else tok["data"]["accessToken"]


def _predict_request(model: str, session_id: str, tab_code: str, text: str,
                     system_prompt: str, thinking: bool, thinking_budget: int,
                     temperature: float, top_p: float, enable_search: bool) -> Dict:
    model_param = {"top_p": top_p, "temperature": temperature,
                   "enable_search": enable_search, "enable_thinking": thinking,
                   "thinking_budget": thinking_budget, "result_format": "message"}
    if system_prompt:
        model_param["systemMessage"] = system_prompt[:8000]
    type_ids = ["Reasoning", "VU", "TG"] if model == "qwen3.8-max" else ((["Reasoning"] if thinking else []) + ["TG"])
    return {"modelId": model, "sessionId": session_id, "tabCode": tab_code,
            "contentList": [{"type": "text", "content": text}],
            "predictConfig": {"modelParam": model_param, "chatType": "t2t"},
            "reGenerate": False, "chatLogCode": uuid.uuid4().hex,
            "modelTypeIds": type_ids, "isAiCenterRequest": False}


def _flatten_transcript(messages: List[Dict]) -> str:
    lines = []
    for m in messages or []:
        if not isinstance(m, dict):
            continue
        role = (m.get("role") or "").lower()
        content = (m.get("content") or "").strip()
        if not content or role not in ("user", "assistant", "system"):
            continue
        if role == "system":
            continue
        lines.append(f"{'User' if role == 'user' else 'Assistant'}: {content}")
    return "\n\n".join(lines)


def _extract_system(messages: List[Dict]) -> str:
    for m in messages or []:
        if isinstance(m, dict) and (m.get("role") or "").lower() == "system" and m.get("content"):
            return str(m["content"])
    return ""


def _stream_predict(session: CurlSession, anon: str, model: str, session_id: str,
                    tab_code: str, text: str, system_prompt: str, thinking: bool,
                    thinking_budget: int, temperature: float, top_p: float,
                    enable_search: bool) -> Generator[Dict, None, None]:
    token = _fresh_token(session, anon)
    preq = _predict_request(model, session_id, tab_code, text, system_prompt,
                            thinking, thinking_budget, temperature, top_p, enable_search)
    body = {"messageId": uuid.uuid4().hex,
            "data": [{"type": "JSON_TEXT",
                      "value": json.dumps({"Api": PREDICT_API,
                                           "Data": {"predictRequest": preq,
                                                    "cornerstoneParam": _cornerstone(anon)},
                                           "V": "1.0"})}]}
    resp = session.post(f"{STREAM_BASE}/sse/console4Json/{token}", json=body,
                        headers={"Accept": "text/event-stream",
                                 "x-anonymous-id": anon},
                        stream=True, timeout=RESPONSE_TIMEOUT)
    if resp.status_code == 401:
        yield {"type": "error", "error": "qwencloud: access token rejected (401); retry the turn"}
        return
    if resp.status_code != 200:
        yield {"type": "error",
               "error": f"qwencloud SSE HTTP {resp.status_code}: {resp.text[:200]}"}
        return
    prev_answer = ""
    prev_reasoning = ""
    saw_any = False
    stream_done = False
    try:
        buffer = ""
        for chunk in resp.iter_content():
            if chunk is None:
                continue
            buffer += chunk.decode("utf-8", errors="replace")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip("\r")
                if not line.startswith("data:"):
                    continue
                raw = line[5:].strip()
                if not raw:
                    continue
                if raw == "[DONE]":
                    stream_done = True
                    break
                try:
                    outer_ev = json.loads(raw)
                    inner = json.loads(outer_ev["data"][0]["value"])
                except (ValueError, KeyError, TypeError, IndexError):
                    continue
                if not inner.get("success", True):
                    yield {"type": "error",
                           "error": f"qwencloud: {str(inner.get('message'))[:200]}"}
                    return
                try:
                    messages_out = inner["data"]["messageList"]
                except (KeyError, TypeError):
                    continue
                for msg in messages_out:
                    if not isinstance(msg, dict) or msg.get("role") != "assistant":
                        continue
                    parts = {}
                    for p in msg.get("contentList") or []:
                        if not isinstance(p, dict):
                            continue
                        jp = p.get("jsonPath") or ""
                        segs = jp.strip("/").split("/")
                        if len(segs) == 3 and segs[0] == "contentList" and segs[1].isdigit():
                            parts.setdefault(int(segs[1]), {})[segs[2]] = p.get(segs[2], p.get("content"))
                    for idx in sorted(parts):
                        part = parts[idx]
                        ptype = ""
                        for p in msg.get("contentList") or []:
                            jp = (p.get("jsonPath") or "")
                            if jp == f"/contentList/{idx}/type":
                                ptype = p.get("content") or ""
                        text_val = str(part.get("content") or "")
                        if idx == 0 and ptype == "DeepThink":
                            saw_any = True
                            if text_val.startswith(prev_reasoning):
                                delta = text_val[len(prev_reasoning):]
                            else:
                                delta = text_val
                            prev_reasoning = text_val
                            if delta.strip():
                                yield {"type": "thought", "content": delta}
                        elif ptype in ("Text", "text", ""):
                            saw_any = True
                            if text_val.startswith(prev_answer):
                                delta = text_val[len(prev_answer):]
                            else:
                                delta = text_val
                            prev_answer = text_val
                            if delta.strip():
                                yield {"type": "text", "content": delta}
                if stream_done:
                    break
            if stream_done:
                break
    except Exception as exc:
        if saw_any:
            logger.warning("qwencloud stream ended after content: %s", exc)
        else:
            yield {"type": "error", "error": f"qwencloud stream failed: {exc}"}
            return
    if not saw_any:
        hint = ""
        try:
            q = quota()
            if q.get("ok") and q.get("limit") and (q.get("used") or 0) >= q["limit"]:
                hint = (f" (risk-token quota exhausted: {q['used']}/{q['limit']} — "
                        f"refresh the {_UMIDTOKEN_ENV} env var with a fresh bx-umidtoken)")
        except Exception:
            pass
        yield {"type": "error", "error": f"qwencloud: stream ended without content{hint}"}
        return
    yield {"type": "done", "finish_reason": "stop"}


def stream_chat(
    messages: List[Dict],
    model: str = DEFAULT_MODEL,
    system_prompt: str = "",
    thinking: bool = True,
    thinking_budget: int = 4000,
    temperature: float = 0.7,
    top_p: float = 0.8,
    enable_search: bool = False,
    session_id: Optional[str] = None,
    tab_code: Optional[str] = None,
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return
    thinking_budget = max(1, min(32768, int(thinking_budget or 4000)))
    sys_from_history = _extract_system(messages)
    system_prompt = system_prompt or sys_from_history
    try:
        session = _new_session()
    except Exception as exc:
        yield {"type": "error", "error": f"qwencloud: cannot reach upstream ({exc})"}
        return
    anon = _anon_id()
    try:
        if session_id and tab_code:
            yield {"type": "session", "session_id": session_id, "tab_code": tab_code}
            turns = [(messages[-1].get("content", "") if messages else "")]
            for text in turns:
                for chunk in _stream_predict(session, anon, model, session_id, tab_code, text,
                                             system_prompt, thinking, thinking_budget,
                                             temperature, top_p, enable_search):
                    if chunk.get("type") == "done":
                        continue
                    yield chunk
            yield {"type": "done", "finish_reason": "stop"}
            return
        prompt = _flatten_transcript(messages)
        if not prompt.strip():
            yield {"type": "error", "error": "qwencloud: no user content to send"}
            return
        label = (messages[-1].get("content", "") if messages else "")[:256]
        session_id, tab_code = _open_tab(session, anon, model, label or "chat")
        yield {"type": "session", "session_id": session_id, "tab_code": tab_code}
        for chunk in _stream_predict(session, anon, model, session_id, tab_code, prompt,
                                     system_prompt, thinking, thinking_budget,
                                     temperature, top_p, enable_search):
            yield chunk
    except Exception as exc:
        yield {"type": "error", "error": f"qwencloud: {exc}"}
        return


def simple_chat(
    user_message: str,
    model: str = DEFAULT_MODEL,
    system_prompt: str = "",
    thinking: bool = False,
    thinking_budget: int = 4000,
    timeout: int = RESPONSE_TIMEOUT,
    max_tokens: int = 0,
    **_: object,
) -> str:
    texts: List[str] = []
    for chunk in stream_chat(
        [{"role": "user", "content": user_message}], model=model,
        system_prompt=system_prompt, thinking=thinking,
        thinking_budget=thinking_budget):
        if chunk.get("type") == "text":
            texts.append(chunk.get("content", ""))
        elif chunk.get("type") == "error":
            return f"[Error] {chunk.get('error', 'unknown error')}"
    return "".join(texts)


def get_models() -> List[Dict]:
    return [
        {"id": m["id"], "name": m["name"],
         "capabilities": {"chat": True, "stream": True, "vision": False,
                          "thinking": m.get("reasoning", False), "tools": False,
                          "web_search": False}}
        for m in MODELS
    ]


def quota() -> Dict:
    try:
        session = _new_session()
    except RuntimeError as exc:
        return {"ok": False, "error": str(exc)}
    anon = _anon_id()
    try:
        info = _rpc(session, anon, UMID_API, {})
        data = info.get("data", info)
        return {"ok": True, "used": data.get("xUmidNumber"), "limit": data.get("limit")}
    except RuntimeError as exc:
        return {"ok": False, "error": str(exc)}
