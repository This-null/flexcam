package com.flexcam

import android.util.Base64
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import okio.ByteString
import okio.ByteString.Companion.toByteString
import org.json.JSONObject
import java.nio.ByteBuffer
import java.util.concurrent.TimeUnit
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec
import kotlin.concurrent.thread

object Quality {
    @Volatile var jpeg = Config.JPEG_QUALITY
    @Volatile var fps = 15
    @Volatile var width = 640
    @Volatile var height = 480
    @Volatile var onChange: (() -> Unit)? = null
}

class RemoteClient(
    private val url: String,
    private val secretHex: String,
    private val frames: () -> ByteArray?,
    private val onState: (String, String) -> Unit,
) {
    @Volatile private var running = false
    private var socket: WebSocket? = null
    private var sender: Thread? = null

    companion object {
        fun parseCode(raw: String): Pair<String, String>? {
            val text = raw.trim()
            if (text.startsWith("{")) {
                return try {
                    val o = JSONObject(text)
                    Pair(o.getString("u"), o.getString("k"))
                } catch (_: Exception) {
                    null
                }
            }
            val dot = text.indexOf('.')
            if (dot <= 0 || dot == text.length - 1) return null
            val sub = text.substring(0, dot)
            var key = text.substring(dot + 1).uppercase()
            while (key.length % 8 != 0) key += "="
            val bytes = try {
                Base64.decode(base32ToBase64(key), Base64.DEFAULT)
            } catch (_: Exception) {
                null
            } ?: return null
            val hex = bytes.joinToString("") { "%02x".format(it) }
            return Pair("https://$sub.trycloudflare.com", hex)
        }

        private const val B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

        private fun base32ToBase64(s: String): String {
            var bits = 0
            var value = 0
            val out = ArrayList<Byte>()
            for (c in s) {
                if (c == '=') continue
                val idx = B32.indexOf(c)
                if (idx < 0) continue
                value = (value shl 5) or idx
                bits += 5
                if (bits >= 8) {
                    bits -= 8
                    out.add(((value shr bits) and 0xFF).toByte())
                }
            }
            return Base64.encodeToString(out.toByteArray(), Base64.NO_WRAP)
        }
    }

    fun start() {
        if (running) return
        running = true
        val client = OkHttpClient.Builder()
            .readTimeout(0, TimeUnit.MILLISECONDS)
            .pingInterval(20, TimeUnit.SECONDS)
            .build()
        val wsUrl = url.replace("https://", "wss://").replace("http://", "ws://")
        onState("connecting", "")
        client.newWebSocket(Request.Builder().url(wsUrl).build(), Listener())
    }

    fun stop() {
        running = false
        try {
            socket?.close(1000, null)
        } catch (_: Exception) {
        }
        socket = null
        onState("stopped", "")
    }

    fun isRunning(): Boolean = running

    private fun hmac(nonceHex: String): String {
        val key = ByteArray(secretHex.length / 2) {
            secretHex.substring(it * 2, it * 2 + 2).toInt(16).toByte()
        }
        val nonce = ByteArray(nonceHex.length / 2) {
            nonceHex.substring(it * 2, it * 2 + 2).toInt(16).toByte()
        }
        val mac = Mac.getInstance("HmacSHA256")
        mac.init(SecretKeySpec(key, "HmacSHA256"))
        return mac.doFinal(nonce).joinToString("") { "%02x".format(it) }
    }

    private fun startSending(ws: WebSocket) {
        sender = thread(name = "remote-send") {
            var last: ByteArray? = null
            while (running) {
                val delay = 1000L / Quality.fps.coerceIn(1, 30)
                val jpeg = frames()
                if (jpeg != null && jpeg !== last) {
                    last = jpeg
                    val buf = ByteBuffer.allocate(8 + jpeg.size)
                    buf.putDouble(System.currentTimeMillis() / 1000.0)
                    buf.put(jpeg)
                    if (!ws.send(buf.array().toByteString())) break
                }
                try {
                    Thread.sleep(delay)
                } catch (_: InterruptedException) {
                    break
                }
            }
        }
    }

    private inner class Listener : WebSocketListener() {
        private var authed = false

        override fun onOpen(webSocket: WebSocket, response: Response) {
            socket = webSocket
        }

        override fun onMessage(webSocket: WebSocket, text: String) {
            if (!authed) {
                if (text.startsWith("{")) {
                    authed = true
                    applyConfig(text)
                    onState("connected", "")
                    startSending(webSocket)
                } else if (text == "denied") {
                    running = false
                    onState("denied", "")
                    webSocket.close(1000, null)
                } else {
                    webSocket.send(hmac(text))
                }
            }
        }

        override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
            running = false
            onState("error", t.message ?: "")
        }

        override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
            if (running) {
                running = false
                onState("stopped", "")
            }
        }
    }

    private fun applyConfig(json: String) {
        try {
            val o = JSONObject(json)
            Quality.jpeg = o.optInt("q", Quality.jpeg)
            Quality.fps = o.optInt("fps", Quality.fps)
            val w = o.optInt("w", Quality.width)
            val h = o.optInt("h", Quality.height)
            if (w != Quality.width || h != Quality.height) {
                Quality.width = w
                Quality.height = h
                Quality.onChange?.invoke()
            }
        } catch (_: Exception) {
        }
    }
}
