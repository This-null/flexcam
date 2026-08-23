class MjpegParser:
    SOI = b"\xff\xd8"
    EOI = b"\xff\xd9"

    def __init__(self):
        self._buf = bytearray()
        self._ready = []

    def feed(self, chunk: bytes) -> None:
        self._buf.extend(chunk)
        while True:
            start = self._buf.find(self.SOI)
            if start < 0:
                if len(self._buf) > 2:
                    del self._buf[:-1]
                return
            end = self._buf.find(self.EOI, start + 2)
            if end < 0:
                if start > 0:
                    del self._buf[:start]
                return
            end += 2
            self._ready.append(bytes(self._buf[start:end]))
            del self._buf[:end]

    def frames(self):
        while self._ready:
            yield self._ready.pop(0)
