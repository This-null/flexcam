package com.flexcam

import android.content.Context
import org.json.JSONObject
import java.net.URL

object Updater {
    private const val VERSION_URL =
        "https://raw.githubusercontent.com/This-null/flexcam/main/version.json"

    data class Info(val available: Boolean, val latest: String, val url: String)

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
