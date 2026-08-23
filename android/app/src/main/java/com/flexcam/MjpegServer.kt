package com.flexcam

import java.io.BufferedOutputStream
import java.net.ServerSocket
import java.net.Socket
import kotlin.concurrent.thread

class MjpegServer(
    private val port: Int,
    private val frameSource: () -> ByteArray?,
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
