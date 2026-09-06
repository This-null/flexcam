package com.flexcam

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.core.content.FileProvider
import org.json.JSONObject
import java.io.File
import java.net.URL

object Updater {
    private const val VERSION_URL =
        "https://raw.githubusercontent.com/This-null/flexcam/main/version.json"
    private const val RELEASES_API =
        "https://api.github.com/repos/This-null/flexcam/releases/latest"

    data class Info(val available: Boolean, val latest: String, val url: String)

    fun apkUrl(): String? {
        return try {
            val conn = URL(RELEASES_API).openConnection().apply {
                connectTimeout = 8000
                readTimeout = 8000
                setRequestProperty("User-Agent", "FlexCam")
            }
            val obj = JSONObject(conn.getInputStream().bufferedReader().use { it.readText() })
            val assets = obj.getJSONArray("assets")
            for (i in 0 until assets.length()) {
                val a = assets.getJSONObject(i)
                if (a.getString("name").endsWith(".apk", true)) {
                    return a.getString("browser_download_url")
                }
            }
            null
        } catch (_: Exception) {
            null
        }
    }

    fun downloadApk(ctx: Context, url: String, onProgress: (Int) -> Unit): File? {
        return try {
            val dir = File(ctx.cacheDir, "updates").apply {
                mkdirs()
                listFiles()?.forEach { it.delete() }
            }
            val out = File(dir, "FlexCam.apk")
            val conn = URL(url).openConnection().apply {
                connectTimeout = 15000
                readTimeout = 30000
                setRequestProperty("User-Agent", "FlexCam")
            }
            val total = conn.contentLength
            conn.getInputStream().use { input ->
                out.outputStream().use { sink ->
                    val buf = ByteArray(65536)
                    var done = 0L
                    while (true) {
                        val n = input.read(buf)
                        if (n <= 0) break
                        sink.write(buf, 0, n)
                        done += n
                        if (total > 0) onProgress((done * 100 / total).toInt())
                    }
                }
            }
            if (total > 0 && out.length() < total) {
                out.delete()
                null
            } else {
                out
            }
        } catch (_: Exception) {
            null
        }
    }

    fun installApk(ctx: Context, apk: File): Boolean {
        return try {
            val uri: Uri = FileProvider.getUriForFile(
                ctx, ctx.packageName + ".updates", apk
            )
            val intent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(uri, "application/vnd.android.package-archive")
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            ctx.startActivity(intent)
            true
        } catch (_: Exception) {
            false
        }
    }

    fun check(ctx: Context): Info? {
        return try {
            val conn = URL(VERSION_URL).openConnection().apply {
                connectTimeout = 4000
                readTimeout = 4000
            }
            val text = conn.getInputStream().bufferedReader().use { it.readText() }
            val obj = JSONObject(text)
            val latest = obj.optString("version")
            val url = obj.optString("url", Config.GITHUB_URL)
            val current = ctx.packageManager
                .getPackageInfo(ctx.packageName, 0).versionName ?: "0"
            Info(latest.isNotEmpty() && isNewer(latest, current), latest, url)
        } catch (_: Exception) {
            null
        }
    }

    private fun isNewer(latest: String, current: String): Boolean {
        val a = latest.split(".").map { it.toIntOrNull() ?: 0 }
        val b = current.split(".").map { it.toIntOrNull() ?: 0 }
        for (i in 0 until maxOf(a.size, b.size)) {
            val x = a.getOrElse(i) { 0 }
            val y = b.getOrElse(i) { 0 }
            if (x != y) return x > y
        }
        return false
    }
}
