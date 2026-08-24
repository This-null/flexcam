package com.flexcam

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageFormat
import android.graphics.Matrix
import android.graphics.Rect
import android.graphics.YuvImage
import android.provider.Settings
import android.view.OrientationEventListener
import android.view.Surface
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import androidx.lifecycle.LifecycleOwner
import java.io.ByteArrayOutputStream
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicReference

class CameraCapture(
    private val context: Context,
    private val lifecycleOwner: LifecycleOwner,
) {
    private val executor = Executors.newSingleThreadExecutor()
    private val latest = AtomicReference<ByteArray?>(null)
    private var provider: ProcessCameraProvider? = null
    private var analysis: ImageAnalysis? = null
    private var orientationListener: OrientationEventListener? = null

    private var lensFacing = CameraSelector.LENS_FACING_BACK
    @Volatile private var paused = false

    fun latestJpeg(): ByteArray? = if (paused) null else latest.get()

    fun pause() {
        paused = true
        latest.set(null)
        FrameBus.jpeg = null
        ContextCompat.getMainExecutor(context).execute { provider?.unbindAll() }
    }

    fun resume() {
        paused = false
        ContextCompat.getMainExecutor(context).execute { bindCurrent() }
    }

    fun isFront(): Boolean = lensFacing == CameraSelector.LENS_FACING_FRONT

    fun start() {
        val future = ProcessCameraProvider.getInstance(context)
        future.addListener({
            provider = future.get()
            if (analysis == null) {
                analysis = ImageAnalysis.Builder()
                    .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                    .setOutputImageFormat(ImageAnalysis.OUTPUT_IMAGE_FORMAT_YUV_420_888)
                    .setTargetRotation(Surface.ROTATION_0)
                    .build().also { a ->
                        a.setAnalyzer(executor) { image ->
                            val j = yuvToJpeg(image)
                            latest.set(j)
                            FrameBus.jpeg = j
                            image.close()
                        }
                    }
            }
            bindCurrent()
        }, ContextCompat.getMainExecutor(context))
        setupOrientationListener()
    }

    private fun setupOrientationListener() {
        if (orientationListener != null) return
        orientationListener = object : OrientationEventListener(context) {
            override fun onOrientationChanged(orientation: Int) {
                if (orientation == ORIENTATION_UNKNOWN) return
                val a = analysis ?: return
                val autoRotate = try {
                    Settings.System.getInt(
                        context.contentResolver,
                        Settings.System.ACCELEROMETER_ROTATION, 0
                    ) == 1
                } catch (_: Exception) {
                    false
                }
                val rotation = if (!autoRotate) {
                    Surface.ROTATION_0
                } else when (orientation) {
                    in 60 until 120 -> Surface.ROTATION_270
                    in 150 until 210 -> Surface.ROTATION_180
                    in 240 until 300 -> Surface.ROTATION_90
                    in 330..360, in 0 until 30 -> Surface.ROTATION_0
                    else -> return
                }
                if (a.targetRotation != rotation) {
                    a.targetRotation = rotation
                }
            }
        }.also { if (it.canDetectOrientation()) it.enable() }
    }

    fun switchCamera() {
        lensFacing = if (lensFacing == CameraSelector.LENS_FACING_BACK) {
            CameraSelector.LENS_FACING_FRONT
        } else {
            CameraSelector.LENS_FACING_BACK
        }
        ContextCompat.getMainExecutor(context).execute { bindCurrent() }
    }

    private fun bindCurrent() {
        val p = provider ?: return
        val useCase = analysis ?: return
        val selector = CameraSelector.Builder().requireLensFacing(lensFacing).build()
        try {
            p.unbindAll()
            p.bindToLifecycle(lifecycleOwner, selector, useCase)
        } catch (_: Exception) {
        }
    }

    fun stop() {
        orientationListener?.disable()
        orientationListener = null
        provider?.unbindAll()
        executor.shutdown()
    }

    private fun yuvToJpeg(image: ImageProxy): ByteArray {
        val nv21 = yuv420ToNv21(image)
        val yuv = YuvImage(nv21, ImageFormat.NV21, image.width, image.height, null)
        val out = ByteArrayOutputStream()
        yuv.compressToJpeg(
            Rect(0, 0, image.width, image.height), Config.JPEG_QUALITY, out
        )
        val jpeg = out.toByteArray()
        val rotation = image.imageInfo.rotationDegrees
        if (rotation == 0) return jpeg
        return rotateJpeg(jpeg, rotation)
    }

    private fun rotateJpeg(jpeg: ByteArray, degrees: Int): ByteArray {
        val src = BitmapFactory.decodeByteArray(jpeg, 0, jpeg.size) ?: return jpeg
        val matrix = Matrix().apply { postRotate(degrees.toFloat()) }
        val rotated = Bitmap.createBitmap(
            src, 0, 0, src.width, src.height, matrix, true
        )
        val out = ByteArrayOutputStream()
        rotated.compress(Bitmap.CompressFormat.JPEG, Config.JPEG_QUALITY, out)
        if (rotated != src) rotated.recycle()
        src.recycle()
        return out.toByteArray()
    }

    private fun yuv420ToNv21(image: ImageProxy): ByteArray {
        val width = image.width
        val height = image.height
        val nv21 = ByteArray(width * height * 3 / 2)

        val yPlane = image.planes[0]
        val uPlane = image.planes[1]
        val vPlane = image.planes[2]
        val yBuf = yPlane.buffer
        val uBuf = uPlane.buffer
        val vBuf = vPlane.buffer

        var pos = 0
        val yRowStride = yPlane.rowStride
        if (yRowStride == width) {
            yBuf.get(nv21, 0, width * height)
            pos = width * height
        } else {
            for (row in 0 until height) {
                yBuf.position(row * yRowStride)
                yBuf.get(nv21, pos, width)
                pos += width
            }
        }

        val uvRowStride = uPlane.rowStride
        val uvPixelStride = uPlane.pixelStride
        val uvHeight = height / 2
        val uvWidth = width / 2
        for (row in 0 until uvHeight) {
            for (col in 0 until uvWidth) {
                val vuIndex = row * uvRowStride + col * uvPixelStride
                nv21[pos++] = vBuf.get(vuIndex)
                nv21[pos++] = uBuf.get(vuIndex)
            }
        }
        return nv21
    }
}
