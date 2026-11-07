package com.flexcam

import android.net.LocalServerSocket
import java.io.BufferedOutputStream
import java.io.InputStream
import java.io.OutputStream
import java.net.ServerSocket
import java.security.MessageDigest
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.atomic.AtomicInteger
import kotlin.concurrent.thread

class MjpegServer(
    private val port: Int,
    private val frameSource: () -> ByteArray?,
    private val control: (String) -> Unit = {},
    private val authKey: String = "",
) {
    companion object {
        const val SOCKET_NAME = "flexcam"
        private const val MAX_CLIENTS = 8
        private const val MAX_FAILS = 5
        private const val LOCK_MS = 60_000L
        private const val MAX_LINE = 2048
        private const val READ_TIMEOUT_MS = 5000
        private val TRUSTED_UIDS = setOf(0, 2000)
    }

    @Volatile private var running = false
    private var server: ServerSocket? = null
    private var local: LocalServerSocket? = null
    private val active = AtomicInteger(0)
    private val strikes = ConcurrentHashMap<String, LongArray>()

    fun start() {
        running = true
        thread(name = "mjpeg-accept") {
            val s = try {
                ServerSocket(port)
            } catch (_: Exception) {
                return@thread
            }
            server = s
            while (running) {
                try {
                    val client = s.accept()
                    client.soTimeout = READ_TIMEOUT_MS
                    val ip = client.inetAddress?.hostAddress ?: "?"
                    thread(name = "mjpeg-client") {
                        client.use { handle(it.getInputStream(), it.getOutputStream(), false, ip) }
                    }
                } catch (_: Exception) {
                    if (!running) break
                }
            }
        }
        thread(name = "mjpeg-local") {
            val s = try {
                LocalServerSocket(SOCKET_NAME)
            } catch (_: Exception) {
                return@thread
            }
            local = s
            while (running) {
                try {
                    val client = s.accept()
                    val uid = try {
                        client.peerCredentials.uid
                    } catch (_: Exception) {
                        -1
                    }
                    if (uid !in TRUSTED_UIDS) {
                        client.close()
                        continue
                    }
                    thread(name = "mjpeg-local-client") {
                        client.use { handle(it.inputStream, it.outputStream, true, "usb") }
                    }
                } catch (_: Exception) {
                    if (!running) break
                }
            }
        }
    }

    fun stop() {
        running = false
        try {
            server?.close()
        } catch (_: Exception) {
        }
        try {
            local?.close()
        } catch (_: Exception) {
        }
    }

    private fun locked(ip: String): Boolean =
        (strikes[ip]?.get(1) ?: 0L) > System.currentTimeMillis()

    private fun fail(ip: String) {
        strikes.compute(ip) { _, v ->
            val a = v ?: LongArray(2)
            a[0]++
            if (a[0] >= MAX_FAILS) {
                a[0] = 0
                a[1] = System.currentTimeMillis() + LOCK_MS
            }
            a
        }
    }

    private fun sameKey(candidate: String): Boolean =
        authKey.isNotEmpty() && MessageDigest.isEqual(
            candidate.toByteArray(), authKey.toByteArray()
        )

    private fun reply(out: OutputStream, status: String, body: String) {
        try {
            out.write(
                "HTTP/1.0 $status\r\nContent-Length: ${body.length}\r\n\r\n$body".toByteArray()
            )
            out.flush()
        } catch (_: Exception) {
        }
    }

    private fun readLine(inp: InputStream): String? {
        val sb = StringBuilder()
        while (sb.length <= MAX_LINE) {
            val b = inp.read()
            if (b < 0) return null
            if (b == '\n'.code) return sb.toString().trimEnd('\r')
            sb.append(b.toChar())
        }
        return null
    }

    private fun handle(inp: InputStream, out: OutputStream, trusted: Boolean, ip: String) {
        if (active.incrementAndGet() > MAX_CLIENTS) {
            active.decrementAndGet()
            reply(out, "503 Service Unavailable", "busy")
            return
        }
        try {
            if (!trusted && locked(ip)) {
                reply(out, "429 Too Many Requests", "locked")
                return
            }
            val requestLine = try {
                readLine(inp)
            } catch (_: Exception) {
                null
            }
            if (requestLine == null) {
                reply(out, "400 Bad Request", "bad")
                return
            }
            val target = requestLine.split(" ").getOrNull(1) ?: "/"
            val path = target.substringBefore("?")
            val query = target.substringAfter("?", "")

            if (!trusted) {
                val key = query.split("&")
                    .firstOrNull { it.startsWith("key=") }
                    ?.substringAfter("key=") ?: ""
                if (!sameKey(key)) {
                    fail(ip)
                    reply(out, "403 Forbidden", "Forbidden")
                    return
                }
                strikes.remove(ip)
            }

            if (path.startsWith("/stop") || path.startsWith("/start")) {
                control(if (path.startsWith("/stop")) "stop" else "start")
                reply(out, "200 OK", "OK")
                return
            }
            stream(out)
        } catch (_: Exception) {
        } finally {
            active.decrementAndGet()
        }
    }

    private fun stream(raw: OutputStream) {
        val out = BufferedOutputStream(raw)
        out.write(
            ("HTTP/1.0 200 OK\r\n" +
                "Cache-Control: no-cache\r\n" +
                "Content-Type: multipart/x-mixed-replace; boundary=${Config.BOUNDARY}\r\n\r\n")
                .toByteArray()
        )
        out.flush()
        while (running) {
            val jpeg = frameSource()
            if (jpeg == null) {
                Thread.sleep(10)
                continue
            }
            out.write(
                ("--${Config.BOUNDARY}\r\nContent-Type: image/jpeg\r\n" +
                    "Content-Length: ${jpeg.size}\r\n\r\n").toByteArray()
            )
            out.write(jpeg)
            out.write("\r\n".toByteArray())
            out.flush()
            Thread.sleep(33)
        }
    }
}
