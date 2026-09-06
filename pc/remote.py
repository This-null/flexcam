import asyncio
import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import socket
import struct
import subprocess
import sys
import threading
import time

import websockets

TUNNEL_RE = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")
MAX_AUTH_FAILURES = 5
HANDSHAKE_TIMEOUT = 10
TUNNEL_TIMEOUT = 30
CODE_TTL = 600

QUALITY = {
    "low": {"w": 640, "h": 480, "q": 50, "fps": 12},
    "medium": {"w": 640, "h": 480, "q": 60, "fps": 15},
    "high": {"w": 1280, "h": 720, "q": 60, "fps": 15},
}


def cloudflared_path():
    base = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(base, "bin", "cloudflared.exe"),
              os.path.join(base, "cloudflared.exe")):
        if os.path.exists(p):
            return p
    return None


def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class RemoteSession:
    def __init__(self, on_frame=None, on_state=None, quality="medium"):
        self._on_frame = on_frame or (lambda jpeg: None)
        self._on_state = on_state or (lambda state, detail: None)
        self.quality = quality if quality in QUALITY else "medium"
        self.url = None
        self.secret = None
        self._port = None
        self._proc = None
        self._loop = None
        self._server = None
        self._thread = None
        self._running = False
        self._connected = False
        self._failures = 0
        self._started_at = 0

    def is_running(self):
        return self._running

    def is_connected(self):
        return self._connected

    def expired(self):
        return (not self._connected and self._started_at
                and time.time() - self._started_at > CODE_TTL)

    def set_quality(self, quality):
        if quality in QUALITY:
            self.quality = quality

    def pairing_payload(self):
        if not self.url or not self.secret:
            return None
        return json.dumps({"u": self.url, "k": self.secret}, separators=(",", ":"))

    def pairing_code(self):
        if not self.url or not self.secret:
            return None
        sub = self.url.split("://", 1)[1].split(".", 1)[0]
        key = base64.b32encode(bytes.fromhex(self.secret)).decode().rstrip("=")
        return f"{sub}.{key}"

    @staticmethod
    def parse_code(code):
        sub, _, key = (code or "").strip().partition(".")
        if not sub or not key:
            return None
        pad = "=" * (-len(key) % 8)
        try:
            secret = base64.b32decode(key.upper() + pad).hex()
        except Exception:
            return None
        return {"u": f"https://{sub}.trycloudflare.com", "k": secret}

    def start(self):
        if self._running:
            return False
        exe = cloudflared_path()
        if not exe:
            self._on_state("error", "no_cloudflared")
            return False
        self._running = True
        self._failures = 0
        self._connected = False
        self.secret = secrets.token_bytes(16).hex()
        self._port = _free_port()
        self._on_state("starting", "")
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()
        if not self._start_tunnel(exe):
            self.stop()
            return False
        self._started_at = time.time()
        self._on_state("ready", self.url)
        return True

    def _start_tunnel(self, exe):
        try:
            self._proc = subprocess.Popen(
                [exe, "tunnel", "--url", f"http://127.0.0.1:{self._port}",
                 "--no-autoupdate"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                creationflags=0x08000000, text=True, errors="replace", bufsize=1,
            )
        except Exception:
            self._on_state("error", "tunnel_failed")
            return False
        deadline = time.time() + TUNNEL_TIMEOUT
        while time.time() < deadline:
            line = self._proc.stdout.readline()
            if not line:
                if self._proc.poll() is not None:
                    break
                continue
            found = TUNNEL_RE.search(line)
            if found:
                self.url = found.group(0)
                threading.Thread(target=self._drain, daemon=True).start()
                if self._wait_ready(self.url):
                    return True
                self._on_state("error", "tunnel_failed")
                return False
        self._on_state("error", "tunnel_failed")
        return False

    def _wait_ready(self, url, timeout=45):
        host = url.split("://", 1)[1]
        deadline = time.time() + timeout
        while time.time() < deadline and self._running:
            try:
                socket.getaddrinfo(host, 443)
            except Exception:
                time.sleep(1)
                continue
            try:
                import urllib.request
                req = urllib.request.Request(url, method="HEAD",
                                             headers={"User-Agent": "FlexCam"})
                urllib.request.urlopen(req, timeout=6)
                return True
            except Exception as e:
                if getattr(e, "code", None):
                    return True
                time.sleep(1)
        return False

    def _drain(self):
        try:
            for _ in self._proc.stdout:
                if not self._running:
                    break
        except Exception:
            pass

    def _serve(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._run_server())
        except Exception:
            pass
        finally:
            try:
                self._loop.close()
            except Exception:
                pass

    async def _run_server(self):
        async with websockets.serve(
            self._handler, "127.0.0.1", self._port, max_size=None,
            ping_interval=20, ping_timeout=20,
        ) as server:
            self._server = server
            while self._running:
                await asyncio.sleep(0.3)

    async def _handler(self, ws):
        if self._failures >= MAX_AUTH_FAILURES or self._connected:
            await ws.close()
            return
        nonce = secrets.token_bytes(16)
        try:
            await ws.send(nonce.hex())
            reply = await asyncio.wait_for(ws.recv(), timeout=HANDSHAKE_TIMEOUT)
        except Exception:
            return
        expect = hmac.new(bytes.fromhex(self.secret), nonce,
                          hashlib.sha256).hexdigest()
        if not hmac.compare_digest(str(reply).strip(), expect):
            self._failures += 1
            await asyncio.sleep(min(2 ** self._failures, 30))
            try:
                await ws.close()
            except Exception:
                pass
            if self._failures >= MAX_AUTH_FAILURES:
                self._on_state("error", "too_many_attempts")
            return
        self._failures = 0
        self._connected = True
        self._on_state("connected", "")
        try:
            await ws.send(json.dumps({"ok": True, **QUALITY[self.quality]}))
            async for msg in ws:
                if not self._running:
                    break
                if isinstance(msg, (bytes, bytearray)) and len(msg) > 8:
                    self._on_frame(bytes(msg[8:]))
        except Exception:
            pass
        finally:
            self._connected = False
            if self._running:
                self._on_state("ready", self.url)

    def stop(self):
        self._running = False
        self._connected = False
        if self._proc is not None:
            try:
                self._proc.terminate()
                self._proc.wait(timeout=5)
            except Exception:
                try:
                    self._proc.kill()
                except Exception:
                    pass
            self._proc = None
        self.url = None
        self.secret = None
        self._started_at = 0
        self._on_state("stopped", "")
