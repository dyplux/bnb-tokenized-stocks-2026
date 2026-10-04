#!/usr/bin/env python3
"""Local-only judge surface for one read-only RWA policy decision."""

import json
import sys
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.safety_service import review  # noqa: E402

APP = Path(__file__).resolve().parent
lock = threading.Lock()
attempts = deque()
MAX_BODY = 4096


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, body, mime="application/json; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; base-uri 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(body)

    def json_error(self, status, message):
        self.respond(status, json.dumps({"error": message}).encode())

    def do_GET(self):
        if self.path == "/api/dated-example":
            fixture = APP / "fixtures/safety-nvdab-2026-10-04.json"
            self.respond(200, fixture.read_bytes())
            return
        paths = {"/": ("safety.html", "text/html; charset=utf-8"),
                 "/safety.js": ("safety.js", "text/javascript; charset=utf-8"),
                 "/safety.css": ("safety.css", "text/css; charset=utf-8")}
        if self.path not in paths:
            self.json_error(404, "Not found")
            return
        name, mime = paths[self.path]
        self.respond(200, (APP / name).read_bytes(), mime)

    def do_POST(self):
        if self.path != "/api/safety-check":
            self.json_error(404, "Not found")
            return
        origin = self.headers.get("Origin")
        if origin and origin not in ("http://127.0.0.1:8001", "http://localhost:8001"):
            self.json_error(403, "This local check only accepts its own page")
            return
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            self.json_error(415, "Send JSON")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length < 1 or length > MAX_BODY:
            self.json_error(413, "Request must be under 4 KB")
            return
        if not lock.acquire(blocking=False):
            self.json_error(429, "Another live check is running. Try again shortly.")
            return
        try:
            now = time.monotonic()
            while attempts and now - attempts[0] > 60:
                attempts.popleft()
            if len(attempts) >= 4:
                self.json_error(429, "Four live checks per minute is the local limit.")
                return
            request = json.loads(self.rfile.read(length))
            from app.safety_service import validate
            validate(request)
            attempts.append(now)
            result = review(request)
            self.respond(200, json.dumps(result, ensure_ascii=False).encode())
        except (ValueError, json.JSONDecodeError) as exc:
            self.json_error(400, str(exc)[:160])
        except Exception as exc:
            print("Safety check failed: %s" % type(exc).__name__, file=sys.stderr)
            self.json_error(502, "Live source unavailable. No safety decision was made. Retry later.")
        finally:
            lock.release()


if __name__ == "__main__":
    print("Read-only safety check: http://127.0.0.1:8001")
    ThreadingHTTPServer(("127.0.0.1", 8001), Handler).serve_forever()
