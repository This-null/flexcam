package com.flexcam

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.content.res.ColorStateList
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import kotlin.concurrent.thread
import androidx.core.content.ContextCompat.getColor
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.content.ContextCompat
import androidx.core.os.LocaleListCompat
import java.net.Inet4Address
import java.net.NetworkInterface
import java.util.Collections

class MainActivity : AppCompatActivity() {

    private var serviceStarted = false
    private var userStopped = false

    private val permLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { result ->
        if (result[Manifest.permission.CAMERA] == true) {
            maybeStartService()
        } else {
            status(getString(R.string.status_perm_denied))
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        findViewById<Button>(R.id.switchButton).setOnClickListener {
            if (!serviceStarted) return@setOnClickListener
            val intent = Intent(this, WebcamService::class.java)
                .setAction(Config.ACTION_SWITCH_CAMERA)
            startService(intent)
        }

        findViewById<Button>(R.id.toggleButton).setOnClickListener {
            if (serviceStarted) {
                userStopped = true
                stopWebcam()
            } else {
                userStopped = false
                if (hasCameraPermission()) maybeStartService() else requestPermissions()
            }
        }

        val ip = wifiIp()
        val base = if (ip != null) {
            getString(R.string.hint_with_ip, ip, Config.PORT)
        } else {
            getString(R.string.hint_no_ip, Config.PORT)
        }
        findViewById<TextView>(R.id.hintText).text =
            base + "\n" + getString(R.string.access_code, Pin.get(this))

        findViewById<Button>(R.id.btnGithub).setOnClickListener { open(Config.GITHUB_URL) }
        findViewById<Button>(R.id.btnDiscord).setOnClickListener { open(Config.DISCORD_URL) }
        findViewById<Button>(R.id.btnInsta).setOnClickListener { open(Config.INSTAGRAM_URL) }
        findViewById<Button>(R.id.btnDonate).setOnClickListener { open(Config.DONATE_URL) }
        findViewById<Button>(R.id.langButton).apply {
            text = currentLangLabel()
            setOnClickListener { showLangDialog() }
        }

        if (!hasCameraPermission()) requestPermissions()
    }

    private val langCodes = listOf("en", "tr", "de", "fr", "pt", "es", "az", "zh", "ja", "hi")
    private val langLabels = listOf(
        "🇬🇧 English", "🇹🇷 Türkçe", "🇩🇪 Deutsch", "🇫🇷 Français", "🇵🇹 Português",
        "🇪🇸 Español", "🇦🇿 Azərbaycan", "🇨🇳 中文", "🇯🇵 日本語", "🇮🇳 हिन्दी"
    )

    private fun currentLangLabel(): String {
        val tag = AppCompatDelegate.getApplicationLocales().toLanguageTags()
        val code = if (tag.length >= 2) tag.substring(0, 2)
        else resources.configuration.locales[0].language
        val i = langCodes.indexOf(code)
        return "🌐 " + if (i >= 0) langLabels[i] else langLabels[0]
    }

    private fun showLangDialog() {
        AlertDialog.Builder(this, R.style.FlexDialog)
            .setTitle("Dil / Language")
            .setItems(langLabels.toTypedArray()) { _, i ->
                AppCompatDelegate.setApplicationLocales(
                    LocaleListCompat.forLanguageTags(langCodes[i])
                )
            }
            .show()
    }

    private fun open(url: String) {
        try {
            startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
        } catch (_: Exception) {
        }
    }

    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (hasFocus && !userStopped) maybeStartService()
    }

    @Volatile private var previewing = false

    override fun onResume() {
        super.onResume()
        if (previewing) return
        previewing = true
        val view = findViewById<ImageView>(R.id.preview)
        thread(name = "preview") {
            while (previewing) {
                val j = FrameBus.jpeg
                if (j != null) {
                    val bmp = try {
                        BitmapFactory.decodeByteArray(j, 0, j.size)
                    } catch (_: Exception) {
                        null
                    }
                    if (bmp != null) runOnUiThread { view.setImageBitmap(bmp) }
                }
                Thread.sleep(66)
            }
        }
    }

    override fun onPause() {
        super.onPause()
        previewing = false
    }

    private fun requestPermissions() {
        val needed = mutableListOf(Manifest.permission.CAMERA)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            needed.add(Manifest.permission.POST_NOTIFICATIONS)
        }
        permLauncher.launch(needed.toTypedArray())
    }

    private fun hasCameraPermission(): Boolean =
        ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) ==
            PackageManager.PERMISSION_GRANTED

    private fun maybeStartService() {
        if (serviceStarted || userStopped || !hasCameraPermission()) return
        val intent = Intent(this, WebcamService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        serviceStarted = true
        findViewById<Button>(R.id.toggleButton).text = getString(R.string.btn_stop)
        setDot(R.color.green)
        status(getString(R.string.status_running, Config.PORT))
    }

    private fun stopWebcam() {
        stopService(Intent(this, WebcamService::class.java))
        serviceStarted = false
        findViewById<Button>(R.id.toggleButton).text = getString(R.string.btn_start)
        setDot(R.color.gray)
        status(getString(R.string.status_stopped))
    }

    private fun setDot(colorRes: Int) {
        findViewById<View>(R.id.statusDot).backgroundTintList =
            ColorStateList.valueOf(getColor(this, colorRes))
    }

    private fun wifiIp(): String? {
        try {
            for (nif in Collections.list(NetworkInterface.getNetworkInterfaces())) {
                if (!nif.isUp || nif.isLoopback) continue
                for (addr in Collections.list(nif.inetAddresses)) {
                    if (addr is Inet4Address && addr.isSiteLocalAddress) {
                        return addr.hostAddress
                    }
                }
            }
        } catch (_: Exception) {
        }
        return null
    }

    private fun status(msg: String) {
        findViewById<TextView>(R.id.statusText).text = msg
    }
}
