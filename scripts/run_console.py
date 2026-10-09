#!/usr/bin/env python3
"""Serve the prebuilt Praeva viewer on loopback only."""
import argparse
import http.server
import mimetypes
import os
import socketserver
import sys
import threading
import urllib.parse
import webbrowser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web", "static"))
MEDIA = {
    "/media/praeva-bnb-hack-final-v2.mp4": "https://praeva.dyplux.com/media/praeva-bnb-hack-final-v2.mp4",
    "/media/praeva-bnb-hack-final.mp4": "https://praeva.dyplux.com/media/praeva-bnb-hack-final.mp4",
}


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "PraevaLocal/1.0"

    def _allowed_host(self):
        host = self.headers.get("Host", "").split(":", 1)[0].lower().strip("[]")
        return host in {"localhost", "127.0.0.1"}

    def _send(self, status, body=b"", content_type="text/plain; charset=utf-8", headers=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _request(self):
        if not self._allowed_host():
            return self._send(403, b"Forbidden\n")
        if self.command not in {"GET", "HEAD"}:
            return self._send(405, b"Method Not Allowed\n", headers={"Allow": "GET, HEAD"})
        path = urllib.parse.urlsplit(self.path).path
        if path == "/":
            return self._send(302, headers={"Location": "/console/"})
        if path in MEDIA:
            return self._send(302, headers={"Location": MEDIA[path]})
        if path.endswith("/"):
            path += "index.html"
        relative = urllib.parse.unquote(path.lstrip("/"))
        candidate = os.path.realpath(os.path.join(ROOT, relative))
        if os.path.commonpath((ROOT, candidate)) != ROOT or not os.path.isfile(candidate):
            return self._send(404, b"Not Found\n")
        with open(candidate, "rb") as stream:
            body = stream.read()
        content_type = mimetypes.guess_type(candidate)[0] or "application/octet-stream"
        return self._send(200, body, content_type)

    do_GET = _request
    do_HEAD = _request
    do_POST = _request
    do_PUT = _request
    do_DELETE = _request
    do_PATCH = _request

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = False


def main(argv=None):
    parser = argparse.ArgumentParser(description="Serve the prebuilt Praeva console on localhost.")
    parser.add_argument("--port", type=int, default=8937)
    parser.add_argument("--no-open", action="store_true", help="Do not open /console/ in a browser.")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    try:
        server = Server(("127.0.0.1", args.port), Handler)
    except OSError as exc:
        print("Could not start Praeva console on 127.0.0.1:%d: %s" % (args.port, exc), file=sys.stderr)
        return 1
    url = "http://127.0.0.1:%d/console/" % args.port
    print("Praeva console: %s" % url, flush=True)
    if not args.no_open:
        threading.Timer(0.2, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPraeva console stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
