"""Model Context Protocol (MCP) client bridge for NEB Background Agent.

Connects to external MCP JSON-RPC servers (over HTTP/SSE) to discover tools
and invoke them during coding agent sessions.
"""
from __future__ import annotations

import json
import logging
import os
import urllib.request
import urllib.error
import uuid
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class McpBridgeClient:
    def __init__(self, endpoint_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30):
        self.endpoint_url = endpoint_url.strip()
        self.headers = headers or {}
        self.timeout = timeout

    def _call_rpc(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        req_id = str(uuid.uuid4())
        payload = {
            'jsonrpc': '2.0',
            'id': req_id,
            'method': method,
            'params': params or {}
        }
        data = json.dumps(payload).encode('utf-8')
        req_headers = {
            'Content-Type': 'application/json',
            **self.headers
        }
        req = urllib.request.Request(self.endpoint_url, data=data, headers=req_headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode('utf-8')
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', errors='replace')
            raise RuntimeError(f'MCP HTTP {e.code}: {err_body}')
        except Exception as e:
            raise RuntimeError(f'MCP connection error: {e}')

    def list_tools(self) -> List[Dict[str, Any]]:
        resp = self._call_rpc('tools/list')
        if 'error' in resp and resp['error']:
            raise RuntimeError(f"MCP RPC Error: {resp['error']}")
        result = resp.get('result', {})
        return result.get('tools', [])

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._call_rpc('tools/call', {'name': name, 'arguments': arguments})
        if 'error' in resp and resp['error']:
            raise RuntimeError(f"MCP RPC Error: {resp['error']}")
        return resp.get('result', {})
