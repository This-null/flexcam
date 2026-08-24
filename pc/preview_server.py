import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PREVIEW_PORT = 8475


class PreviewServer:
    def __init__(self, get_frame):
        self._get = get_frame
        self._httpd = None

    def start(self):
        get = self._get

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                if self.path.startswith("/preview"):
                    self._stream()
                else:
                    self.send_response(404)
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
