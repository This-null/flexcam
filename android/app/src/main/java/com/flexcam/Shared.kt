package com.flexcam

import android.content.Context
import java.security.SecureRandom

object FrameBus {
    @Volatile
    var jpeg: ByteArray? = null
}

object Pin {
    private const val CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    private const val KEY = "pin"
    private const val LOCK = "pin_locked"
    private val rnd = SecureRandom()

    private fun prefs(ctx: Context) =
        ctx.getSharedPreferences("flexcam", Context.MODE_PRIVATE)

    fun get(ctx: Context): String =
        prefs(ctx).getString(KEY, null) ?: generate(ctx)

    fun rotate(ctx: Context): String {
        if (isLocked(ctx)) return get(ctx)
        return generate(ctx)
    }

    fun isLocked(ctx: Context): Boolean = prefs(ctx).getBoolean(LOCK, false)

    fun setLocked(ctx: Context, locked: Boolean) {
        prefs(ctx).edit().putBoolean(LOCK, locked).apply()
    }

    private fun generate(ctx: Context): String {
        val pin = (1..4).map { CHARS[rnd.nextInt(CHARS.length)] }.joinToString("")
        prefs(ctx).edit().putString(KEY, pin).apply()
        return pin
    }
}
