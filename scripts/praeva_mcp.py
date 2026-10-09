#!/usr/bin/env python3
"""Read-only MCP stdio adapter for Praeva."""

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import time
from collections import deque
from pathlib import Path

PROTOCOL_VERSION = "2025-06-18"
MAX_MESSAGE_BYTES = 64 * 1024
MAX_LIVE_CALLS = 4
LIVE_WINDOW_SECONDS = 60.0
SERVER_NAME = "praeva"
SERVER_VERSION = "0.1.0"

TOOLS = (
    {
        "name": "praeva_replay",
        "description": "Replay one fixed Praeva judge fixture without network access.",
        "inputSchema": {
            "type": "object", "properties": {
                "case": {"type": "string", "enum": [
                    "observed_need_human", "observed_deny", "synthetic_allow"]
                }
            }, "required": ["case"], "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False},
    },
    {
        "name": "praeva_verify_receipt",
        "description": "Verify a supplied Praeva receipt JSON offline and without a file path.",
        "inputSchema": {
            "type": "object", "properties": {
                "receipt": {"type": "object"},
                "expected_sha256": {"type": "string"},
            }, "required": ["receipt"], "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False},
    },
    {
        "name": "praeva_assess",
        "description": "Run an explicit read-only live Praeva safety review; no signing or broadcast.",
        "inputSchema": {
            "type": "object", "properties": {
                "provider": {"type": "string", "enum": ["bstock", "ondo"]},
                "notional_usdt": {"type": "string"},
                "max_notional_usdt": {"type": "string"},
                "max_price_impact_percent": {"type": "string"},
            }, "required": ["provider", "notional_usdt", "max_notional_usdt",
                             "max_price_impact_percent"], "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False},
    },
)
TOOL_MAP = {tool["name"]: tool for tool in TOOLS}
_live_calls = deque()


class McpError(Exception):
    def __init__(self, code, label):
        super().__init__(label)
        self.code = code
        self.label = label


def log(code):
    print("PRAEVA_MCP " + code, file=sys.stderr, flush=True)


def _load_module(path, name):
    root = str(Path(path).resolve().parents[1])
    if root not in sys.path:
        sys.path.insert(0, root)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise McpError(-32603, "INTERNAL_ERROR")
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(sys.stderr):
        spec.loader.exec_module(module)
    return module


def _root_from(args):
    value = args.get("praeva_root") if isinstance(args, dict) else None
    return Path(value).resolve() if isinstance(value, str) and value else None


def _json_text(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _result(value, is_error=False):
    return {"content": [{"type": "text", "text": _json_text(value)}],
            "isError": bool(is_error)}


def _strict_json(raw):
    def duplicate(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise McpError(-32600, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def constant(_value):
        raise McpError(-32600, "NONFINITE_JSON_NUMBER")

    try:
        return json.loads(raw, object_pairs_hook=duplicate, parse_constant=constant)
    except McpError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError):
        raise McpError(-32700, "PARSE_ERROR")


def _require_object(value, label):
    if not isinstance(value, dict):
        raise McpError(-32602, label)


def _exact_args(args, required):
    _require_object(args, "INVALID_ARGUMENTS")
    if set(args) != set(required):
        raise McpError(-32602, "INVALID_ARGUMENTS")


def _fixture(root, case):
    names = {
        "observed_need_human": "observed-unsafe.json",
        "observed_deny": "observed-mandate-deny.json",
        "synthetic_allow": "synthetic-safe.json",
    }
    if case not in names:
        raise McpError(-32602, "INVALID_CASE")
    path = root / "docs" / "judge" / names[case]
    try:
        raw = path.read_bytes()
    except (OSError, ValueError):
        raise McpError(-32603, "FIXTURE_UNAVAILABLE")
    if len(raw) > MAX_MESSAGE_BYTES:
        raise McpError(-32603, "FIXTURE_TOO_LARGE")
    return _strict_json(raw)


def _verify(root, args):
    _exact_args(args, {"receipt", "expected_sha256"} if "expected_sha256" in args else {"receipt"})
    receipt = args.get("receipt")
    if not isinstance(receipt, dict):
        raise McpError(-32602, "INVALID_RECEIPT")
    expected = args.get("expected_sha256")
    if expected is not None and (not isinstance(expected, str) or len(expected) != 64 or
                                 any(char not in "0123456789abcdefABCDEF" for char in expected)):
        raise McpError(-32602, "INVALID_EXPECTED_SHA256")
    verify = _load_module(root / "scripts" / "verify_receipt.py", "praeva_verify_receipt")
    handle = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", delete=True)
    try:
        json.dump(receipt, handle, ensure_ascii=True, allow_nan=False)
        handle.flush()
        result, exit_code = verify.verify(handle.name, expected)
    except (TypeError, ValueError, OSError, OverflowError, RecursionError):
        raise McpError(-32602, "INVALID_RECEIPT")
    finally:
        handle.close()
    if exit_code == 2:
        raise McpError(-32602, "INVALID_RECEIPT")
    return result


def _credentials(root):
    server = _load_module(root / "app" / "server.py", "praeva_server")
    with contextlib.redirect_stdout(sys.stderr):
        return bool(server.binance_credentials(root))


def _take_live_slot(now=None):
    now = time.monotonic() if now is None else now
    while _live_calls and now - _live_calls[0] >= LIVE_WINDOW_SECONDS:
        _live_calls.popleft()
    if len(_live_calls) >= MAX_LIVE_CALLS:
        raise McpError(-32029, "LIVE_RATE_LIMIT")
    _live_calls.append(now)


def _assess(root, args, review_fn=None, credentials_fn=None):
    _exact_args(args, {"provider", "notional_usdt", "max_notional_usdt", "max_price_impact_percent"})
    for key in args:
        if not isinstance(args[key], str):
            raise McpError(-32602, "INVALID_ARGUMENTS")
    if args["provider"] not in ("bstock", "ondo"):
        raise McpError(-32602, "INVALID_PROVIDER")
    if credentials_fn is None:
        credentials_fn = _credentials
    if not credentials_fn(root):
        log("CREDENTIALS_REQUIRED")
        raise McpError(-32010, "CREDENTIALS_REQUIRED")
    _take_live_slot()
    if review_fn is None:
        service = _load_module(root / "app" / "safety_service.py", "praeva_safety_service")
        review_fn = service.review
    try:
        with contextlib.redirect_stdout(sys.stderr):
            value = review_fn(args)
    except (ValueError, TypeError, RuntimeError, OSError, TimeoutError):
        log("LIVE_REVIEW_ERROR")
        raise McpError(-32011, "LIVE_REVIEW_ERROR")
    if not isinstance(value, dict):
        log("LIVE_REVIEW_ERROR")
        raise McpError(-32011, "LIVE_REVIEW_ERROR")
    return value


def call_tool(name, args, root, review_fn=None, credentials_fn=None):
    if name not in TOOL_MAP:
        raise McpError(-32602, "UNKNOWN_TOOL")
    if not isinstance(root, Path):
        raise McpError(-32602, "PRAEVA_ROOT_REQUIRED")
    if name == "praeva_replay":
        _exact_args(args, {"case"})
        return _fixture(root, args["case"])
    if name == "praeva_verify_receipt":
        return _verify(root, args)
    return _assess(root, args, review_fn, credentials_fn)


def _initialize(params):
    _require_object(params, "INVALID_INITIALIZE")
    allowed = {"protocolVersion", "capabilities", "clientInfo"}
    if set(params) - allowed or "protocolVersion" not in params:
        raise McpError(-32602, "INVALID_INITIALIZE")
    requested = params["protocolVersion"]
    if requested != PROTOCOL_VERSION:
        log("PROTOCOL_VERSION_NEGOTIATED")
    return {"protocolVersion": PROTOCOL_VERSION, "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}}


def _dispatch(message, state, root, review_fn=None, credentials_fn=None):
    if not isinstance(message, dict) or set(message) - {"jsonrpc", "id", "method", "params"}:
        raise McpError(-32600, "INVALID_REQUEST")
    if message.get("jsonrpc") != "2.0" or "method" not in message:
        raise McpError(-32600, "INVALID_REQUEST")
    method = message["method"]
    request_id = message.get("id")
    if not isinstance(method, str) or ("id" in message and (isinstance(request_id, bool) or not isinstance(request_id, (str, int, type(None))))):
        raise McpError(-32600, "INVALID_REQUEST")
    if method == "notifications/initialized":
        if "id" in message:
            raise McpError(-32600, "INVALID_NOTIFICATION")
        if not state["initialized"]:
            raise McpError(-32002, "SERVER_NOT_INITIALIZED")
        if message.get("params", {}) != {}:
            raise McpError(-32602, "INVALID_ARGUMENTS")
        state["ready"] = True
        return None
    if method == "initialize":
        if state["initialized"] or "id" not in message:
            raise McpError(-32600, "INVALID_INITIALIZE")
        result = _initialize(message.get("params"))
        state["initialized"] = True
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    if method == "ping":
        if "id" not in message:
            return None
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if not state["initialized"]:
        raise McpError(-32002, "SERVER_NOT_INITIALIZED")
    if method in ("tools/list", "tools/call") and not state["ready"]:
        raise McpError(-32002, "SERVER_NOT_INITIALIZED")
    if method == "tools/list":
        if "id" not in message:
            raise McpError(-32600, "INVALID_REQUEST")
        if set(message.get("params", {})):
            raise McpError(-32602, "INVALID_ARGUMENTS")
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": list(TOOLS)}}
    if method == "tools/call":
        if "id" not in message:
            raise McpError(-32600, "INVALID_REQUEST")
        params = message.get("params")
        _require_object(params, "INVALID_ARGUMENTS")
        if set(params) - {"name", "arguments"} or "name" not in params:
            raise McpError(-32602, "INVALID_ARGUMENTS")
        try:
            value = call_tool(params["name"], params.get("arguments", {}), root,
                              review_fn, credentials_fn)
            result = _result(value)
        except McpError as error:
            if error.code not in (-32010, -32011, -32029):
                raise
            result = _result({"error": error.label, "decision": None}, True)
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    raise McpError(-32601, "METHOD_NOT_FOUND")


def _error(request_id, error):
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": error.code, "message": error.label}}


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--praeva-root", default=str(Path(__file__).resolve().parents[1]))
    options = parser.parse_args(argv)
    root = Path(options.praeva_root).resolve()
    state = {"initialized": False, "ready": False}
    output = sys.stdout
    while True:
        raw = sys.stdin.buffer.readline(MAX_MESSAGE_BYTES + 2)
        if not raw:
            break
        request_id = None
        if len(raw) > MAX_MESSAGE_BYTES:
            response = _error(None, McpError(-32600, "MESSAGE_TOO_LARGE"))
            output.write(_json_text(response) + "\n")
            output.flush()
            return 2
        else:
            try:
                message = _strict_json(raw)
                request_id = message.get("id") if isinstance(message, dict) else None
                with contextlib.redirect_stdout(sys.stderr):
                    response = _dispatch(message, state, root)
            except McpError as error:
                log(error.label)
                response = _error(request_id, error)
            except Exception:
                log("INTERNAL_ERROR")
                response = _error(None, McpError(-32603, "INTERNAL_ERROR"))
        if response is not None:
            encoded = (_json_text(response) + "\n").encode("utf-8")
            if len(encoded) > MAX_MESSAGE_BYTES:
                encoded = (_json_text(_error(None, McpError(-32603, "RESPONSE_TOO_LARGE"))) + "\n").encode()
            output.buffer.write(encoded)
            output.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
