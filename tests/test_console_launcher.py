#!/usr/bin/env python3
import http.client
import os
import pathlib
import re
import subprocess
import socket
import sys
import time
import unittest

HERE = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = HERE / "scripts" / "run_console.py"
with socket.socket() as port_probe:
    port_probe.bind(("127.0.0.1", 0))
    PORT = port_probe.getsockname()[1]


class ConsoleLauncherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.Popen([sys.executable, str(SCRIPT), "--no-open", "--port", str(PORT)], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for _ in range(40):
            try:
                cls.request("GET", "/")
                break
            except OSError:
                time.sleep(0.05)
        else:
            error = cls.proc.stderr.read()
            cls.proc.terminate()
            cls.proc.wait(timeout=3)
            if "Operation not permitted" in error:
                raise unittest.SkipTest("sandbox denies localhost socket binds")
            raise RuntimeError(error)

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.proc.wait(timeout=3)

    @staticmethod
    def request(method, path, host="127.0.0.1:%d" % PORT):
        conn = http.client.HTTPConnection("127.0.0.1", PORT, timeout=2)
        conn.request(method, path, headers={"Host": host})
        response = conn.getresponse()
        body = response.read()
        conn.close()
        return response, body

    def test_loopback_get_head_and_root_redirect(self):
        response, body = self.request("GET", "/")
        self.assertEqual(response.status, 302)
        self.assertEqual(response.getheader("Location"), "/console/")
        self.assertEqual(body, b"")
        response, body = self.request("GET", "/console/")
        self.assertEqual(response.status, 200)
        self.assertIn(b"Assessment console", body)
        chunks = re.findall(rb'src="([^" ]*/_next/static/chunks/app/console/page-[^" ]+\.js)"', body)
        self.assertEqual(len(chunks), 1, "rendered console must reference its current app chunk")
        response, body = self.request("GET", chunks[0].decode("ascii"))
        self.assertEqual(response.status, 200)
        self.assertGreater(len(body), 1000)
        response, body = self.request("GET", "/console-evidence/managed-replay.json")
        self.assertEqual(response.status, 200)
        self.assertIn(b"receipt", body)
        response, body = self.request("HEAD", "/console/")
        self.assertEqual(response.status, 200)
        self.assertEqual(body, b"")

    def test_boundaries_and_methods(self):
        response, _ = self.request("GET", "/../scripts/run_console.py")
        self.assertEqual(response.status, 404)
        response, _ = self.request("GET", "/%2e%2e/scripts/run_console.py")
        self.assertEqual(response.status, 404)
        response, _ = self.request("GET", "/_next/")
        self.assertEqual(response.status, 404)
        response, _ = self.request("GET", "/missing")
        self.assertEqual(response.status, 404)
        response, _ = self.request("POST", "/console/")
        self.assertEqual(response.status, 405)
        response, _ = self.request("GET", "/console/", host="evil.example")
        self.assertEqual(response.status, 403)

    def test_only_known_media_redirects(self):
        for name in ("praeva-bnb-hack-final-v2.mp4", "praeva-bnb-hack-final.mp4"):
            response, body = self.request("GET", "/media/" + name)
            self.assertEqual(response.status, 302)
            self.assertEqual(response.getheader("Location"), "https://praeva.dyplux.com/media/" + name)
            self.assertEqual(body, b"")
        response, _ = self.request("GET", "/media/other.mp4")
        self.assertEqual(response.status, 404)

    def test_no_server_side_provider_hooks_or_bundled_videos(self):
        self.assertFalse(list((HERE / "web").rglob("*.mp4")))
        source = SCRIPT.read_text()
        for token in ("fetch(", "server action", "provider", "wallet"):
            self.assertNotIn(token, source.lower())


class LauncherContractTests(unittest.TestCase):
    def test_static_contract_without_socket(self):
        source = SCRIPT.read_text()
        for text in ("127.0.0.1", "localhost", "GET", "HEAD", "403", "404", "405", "/console/", "commonpath", "media/praeva-bnb-hack-final-v2.mp4", "media/praeva-bnb-hack-final.mp4"):
            self.assertIn(text, source)

    def test_private_package_has_no_bundled_media_or_node_modules(self):
        self.assertFalse(list((HERE / "web").rglob("*.mp4")))
        self.assertFalse((HERE / "web" / "node_modules").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
