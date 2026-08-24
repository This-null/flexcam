package com.flexcam

import java.io.BufferedOutputStream
import java.net.ServerSocket
import java.net.Socket
import kotlin.concurrent.thread

class MjpegServer(
    private val port: Int,
    private val frameSource: () -> ByteArray?,
    private val control: (String) -> Unit = {},
    private val authKey: String = "",
) {
    @Volatile private var running = false
    private var server: ServerSocket? = null

    fun start() {
        running = true
        thread(name = "mjpeg-accept") {
            val s = try {
                ServerSocket(port)
            } catch (_: Exception) {
                running = false
                return@thread
            }
            server = s
            while (running) {
                try {
                    val client = s.accept()
                    thread(name = "mjpeg-client") { serve(client) }
                } catch (_: Exception) {
                    if (running) continue else break
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
    }

    private fun serve(client: Socket) {
        try {
            client.use {
                val requestLine = it.getInputStream().bufferedReader().readLine() ?: ""
                val target = requestLine.split(" ").getOrNull(1) ?: "/"
                val path = target.substringBefore("?")
                val query = target.substringAfter("?", "")

                val loopback = it.inetAddress?.isLoopbackAddress ?: false
                if (!loopback && authKey.isNotEmpty()) {
                    val key = query.split("&")
                        .firstOrNull { q -> q.startsWith("key=") }
                        ?.substringAfter("key=") ?: ""
                    if (key != authKey) {
                        it.getOutputStream().write(
                            "HTTP/1.0 403 Forbidden\r\nContent-Length: 9\r\n\r\nForbidden".toByteArray()
                        )
                        it.getOutputStream().flush()
                        return
                    }
                }

                if (path.startsWith("/stop") || path.startsWith("/start")) {
                    control(if (path.startsWith("/stop")) "stop" else "start")
                    val ok = "HTTP/1.0 200 OK\r\nContent-Length: 2\r\n\r\nOK"
                    it.getOutputStream().write(ok.toByteArray())
                    it.getOutputStream().flush()
                    return
                }
                val out = BufferedOutputStream(it.getOutputStream())
                val header = "HTTP/1.0 200 OK\r\n" +
                    "Cache-Control: no-cache\r\n" +
                    "Content-Type: multipart/x-mixed-replace; boundary=${Config.BOUNDARY}\r\n\r\n"
                out.write(header.toByteArray())
                out.flush()
                while (running && !it.isClosed) {
                    val jpeg = frameSource()
                    if (jpeg == null) {
                        Thread.sleep(10)
                        continue
                    }
                    val part = "--${Config.BOUNDARY}\r\n" +
                        "Content-Type: image/jpeg\r\n" +
                        "Content-Length: ${jpeg.size}\r\n\r\n"
                    out.write(part.toByteArray())
                    out.write(jpeg)
                    out.write("\r\n".toByteArray())
                    out.flush()
                    Thread.sleep(33)
                }
            }
        } catch (_: Exception) {
        }
    }
}
