package com.flexcam

import android.content.Context

object FrameBus {
    @Volatile
    var jpeg: ByteArray? = null
}

object Pin {
    private const val CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

    fun get(ctx: Context): String {
        val p = ctx.getSharedPreferences("flexcam", Context.MODE_PRIVATE)
        var pin = p.getString("pin", null)
        if (pin == null) {
            pin = (1..4).map { CHARS.random() }.joinToString("")
            p.edit().putString("pin", pin).apply()
        }
        return pin
    }
}
