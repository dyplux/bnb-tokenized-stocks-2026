import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


CANDIDATE = Path(__file__).resolve().parents[1]
SCRIPT = CANDIDATE / "scripts" / "praeva_mcp.py"
PRAEVA = CANDIDATE


def load_server():
    spec = importlib.util.spec_from_file_location("praeva_mcp_test_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProtocolTests(unittest.TestCase):
    def run_server(self, messages):
        # Tool requests follow the initialized notification required by MCP.
        if messages and messages[0].get("method") == "initialize" and not any(m.get("method") == "notifications/initialized" for m in messages):
            messages = messages[:1] + [{"jsonrpc": "2.0", "method": "notifications/initialized"}] + messages[1:]
        payload = b"".join(json.dumps(message, separators=(",", ":")).encode() + b"\n" for message in messages)
        process = subprocess.run([sys.executable, str(SCRIPT), "--praeva-root", str(PRAEVA)],
                                 input=payload, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 check=True)
        return [json.loads(line) for line in process.stdout.splitlines()], process.stderr.decode()

    def test_initialize_list_and_all_offline_tools(self):
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                         "clientInfo": {"name": "test", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "praeva_replay", "arguments": {"case": "observed_need_human"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
             "params": {"name": "praeva_replay", "arguments": {"case": "observed_deny"}}},
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call",
             "params": {"name": "praeva_replay", "arguments": {"case": "synthetic_allow"}}},
        ]
        output, _ = self.run_server(messages)
        self.assertEqual(output[0]["result"]["protocolVersion"], "2025-06-18")
        self.assertEqual([tool["name"] for tool in output[1]["result"]["tools"]], [
            "praeva_replay", "praeva_verify_receipt", "praeva_assess"])
        decisions = [json.loads(item["result"]["content"][0]["text"])["receipt"]["decision"]
                     for item in output[2:]]
        self.assertEqual(decisions, ["NEED_HUMAN", "DENY", "ALLOW"])

    def test_receipt_verification_and_hashes(self):
        observed = json.loads((PRAEVA / "docs/judge/observed-unsafe.json").read_text())
        synthetic = json.loads((PRAEVA / "docs/judge/synthetic-safe.json").read_text())
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": "2025-06-18", "capabilities": {},
                "clientInfo": {"name": "test", "version": "1"}}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
                "name": "praeva_verify_receipt", "arguments": {
                    "receipt": observed, "expected_sha256": observed["receipt"]["receipt_sha256"]}}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                "name": "praeva_verify_receipt", "arguments": {"receipt": synthetic}}},
        ]
        output, _ = self.run_server(messages)
        first = json.loads(output[1]["result"]["content"][0]["text"])
        second = json.loads(output[2]["result"]["content"][0]["text"])
        self.assertEqual(first["integrity"], "INTEGRITY_MATCH")
        self.assertEqual(second["integrity"], "INTEGRITY_MATCH")

    def test_unknown_method_tool_and_extra_arguments(self):
        output, _ = self.run_server([
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": "future", "capabilities": {}, "clientInfo": {"name": "t", "version": "1"}}},
            {"jsonrpc": "2.0", "id": 2, "method": "unknown", "params": {}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                "name": "nope", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {
                "name": "praeva_replay", "arguments": {"case": "synthetic_allow", "extra": 1}}},
        ])
        self.assertEqual(output[0]["result"]["protocolVersion"], "2025-06-18")
        self.assertEqual([item["error"]["code"] for item in output[1:]], [-32601, -32602, -32602])

    def test_lifecycle_requires_initialized_notification(self):
        server = load_server()
        state = {"initialized": True, "ready": False}
        with self.assertRaises(server.McpError) as error:
            server._dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, state, PRAEVA)
        self.assertEqual(error.exception.label, "SERVER_NOT_INITIALIZED")

    def test_tool_error_is_sanitized_content(self):
        server = load_server()
        response = server._dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
            "name": "praeva_assess", "arguments": {"provider": "ondo", "notional_usdt": "10",
            "max_notional_usdt": "10", "max_price_impact_percent": "0.5"}}},
            {"initialized": True, "ready": True}, PRAEVA, credentials_fn=lambda _: False)
        self.assertTrue(response["result"]["isError"])
        data = json.loads(response["result"]["content"][0]["text"])
        self.assertEqual(data, {"error": "CREDENTIALS_REQUIRED", "decision": None})

    def test_duplicate_nan_and_oversize(self):
        raw = b'{"jsonrpc":"2.0","id":1,"method":"ping","method":"ping"}\n'
        raw += b'{"jsonrpc":"2.0","id":2,"method":"ping","params":{"n":NaN}}\n'
        raw += b'{"jsonrpc":"2.0","id":3,"method":"ping","params":{}}' + b" " * (64 * 1024) + b"\n"
        process = subprocess.run([sys.executable, str(SCRIPT), "--praeva-root", str(PRAEVA)],
                                 input=raw, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        self.assertEqual(process.returncode, 2)
        output = [json.loads(line) for line in process.stdout.splitlines()]
        self.assertEqual([item["error"]["message"] for item in output],
                         ["DUPLICATE_JSON_KEY", "NONFINITE_JSON_NUMBER", "MESSAGE_TOO_LARGE"])


class LiveGuardTests(unittest.TestCase):
    def setUp(self):
        self.server = load_server()
        self.server._live_calls.clear()

    def request(self):
        return {"provider": "bstock", "notional_usdt": "100", "max_notional_usdt": "100",
                "max_price_impact_percent": "0.5"}

    def test_fake_injected_review_parity_and_error(self):
        seen = []

        def fake_review(value):
            seen.append(value)
            return {"decision": "NEED_HUMAN", "receipt": {"decision": "NEED_HUMAN"}}

        result = self.server.call_tool("praeva_assess", self.request(), PRAEVA,
                                       review_fn=fake_review, credentials_fn=lambda _: True)
        self.assertEqual(result["decision"], "NEED_HUMAN")
        self.assertEqual(seen[0]["provider"], "bstock")

        def broken(_value):
            raise RuntimeError("secret should not escape")

        with self.assertRaises(self.server.McpError) as raised:
            self.server.call_tool("praeva_assess", self.request(), PRAEVA,
                                  review_fn=broken, credentials_fn=lambda _: True)
        self.assertEqual(raised.exception.label, "LIVE_REVIEW_ERROR")

    def test_credentials_before_network_and_four_call_rate_limit(self):
        called = []

        def fake_review(_value):
            called.append(True)
            return {"decision": "NEED_HUMAN"}

        for _ in range(4):
            self.server.call_tool("praeva_assess", self.request(), PRAEVA,
                                  review_fn=fake_review, credentials_fn=lambda _: True)
        with self.assertRaises(self.server.McpError) as raised:
            self.server.call_tool("praeva_assess", self.request(), PRAEVA,
                                  review_fn=fake_review, credentials_fn=lambda _: True)
        self.assertEqual(raised.exception.label, "LIVE_RATE_LIMIT")
        self.assertEqual(len(called), 4)
        with self.assertRaises(self.server.McpError) as raised:
            self.server.call_tool("praeva_assess", self.request(), PRAEVA,
                                  review_fn=fake_review, credentials_fn=lambda _: False)
        self.assertEqual(raised.exception.label, "CREDENTIALS_REQUIRED")


if __name__ == "__main__":
    unittest.main()
