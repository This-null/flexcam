import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mjpeg_client import MjpegParser


def _multipart(jpegs, boundary=b"frame"):
    out = b""
    for j in jpegs:
        out += b"--" + boundary + b"\r\n"
        out += b"Content-Type: image/jpeg\r\n"
        out += b"Content-Length: " + str(len(j)).encode() + b"\r\n\r\n"
        out += j + b"\r\n"
    return out


def test_extracts_two_frames_split_across_chunks():
    jpeg_a = b"\xff\xd8" + b"AAAA" + b"\xff\xd9"
    jpeg_b = b"\xff\xd8" + b"BBBBBB" + b"\xff\xd9"
    stream = _multipart([jpeg_a, jpeg_b])
    p = MjpegParser()
    mid = len(stream) // 2
    p.feed(stream[:mid])
    p.feed(stream[mid:])
    got = list(p.frames())
    assert got == [jpeg_a, jpeg_b]


def test_partial_frame_not_emitted():
    p = MjpegParser()
    p.feed(b"--frame\r\n\r\n\xff\xd8\xff")  # SOI var, EOI yok
    assert list(p.frames()) == []
    p.feed(b"\xd9\r\n")                      # EOI tamamlandı
    assert list(p.frames()) == [b"\xff\xd8\xff\xd9"]
