import hmac
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

PREVIEW_PORT = 8475


class PreviewServer:
    def __init__(self, get_frame, token):
        self._get = get_frame
        self._token = token
        self._httpd = None

    def start(self):
        get = self._get
        token = self._token
        hosts = (f"127.0.0.1:{PREVIEW_PORT}", f"localhost:{PREVIEW_PORT}")

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                url = urlparse(self.path)
                given = parse_qs(url.query).get("t", [""])[0]
                host = (self.headers.get("Host") or "").lower()
                ok = (
                    url.path == "/preview"
                    and host in hosts
                    and hmac.compare_digest(given.encode(), token.encode())
                )
                if ok:
                    self._stream()
                else:
                    self.send_response(403)
                    self.end_headers()

            def _stream(self):
                try:
                    self.send_response(200)
                    self.send_header(
                        "Content-Type",
                        "multipart/x-mixed-replace; boundary=frame",
                    )
                    self.send_header("Cache-Control", "no-cache")
                    self.end_headers()
                    while True:
                        jpeg = get()
                        if jpeg:
                            self.wfile.write(b"--frame\r\n")
                            self.wfile.write(b"Content-Type: image/jpeg\r\n")
                            self.wfile.write(
                                b"Content-Length: " + str(len(jpeg)).encode() + b"\r\n\r\n"
                            )
                            self.wfile.write(jpeg)
                            self.wfile.write(b"\r\n")
                        time.sleep(0.05)
                except Exception:
                    pass

        try:
            self._httpd = ThreadingHTTPServer(("127.0.0.1", PREVIEW_PORT), Handler)
            threading.Thread(target=self._httpd.serve_forever, daemon=True).start()
        except Exception:
            pass
