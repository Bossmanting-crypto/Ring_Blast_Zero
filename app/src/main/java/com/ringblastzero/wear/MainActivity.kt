package com.ringblastzero.wear

import android.annotation.SuppressLint
import android.app.Activity
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.os.VibrationEffect
import android.os.Vibrator
import android.view.InputDevice
import android.view.MotionEvent
import android.view.WindowManager
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import android.window.OnBackInvokedDispatcher
import androidx.webkit.WebViewAssetLoader

/**
 * Ring Blast Zero for Wear OS: a full-screen WebView running the watch build of the game from the app's assets.
 * The game talks to the watch through window.RZNative (keep the screen on during play, vibrate), and the
 * activity forwards the crown/bezel (rotary input) and the back button to the game.
 */
class MainActivity : Activity() {

    private lateinit var web: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Serve assets from a proper https origin so localStorage (save data) behaves like a normal site.
        val assets = WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(this))
            .build()

        web = WebView(this).apply {
            setBackgroundColor(Color.BLACK)
            isVerticalScrollBarEnabled = false
            isHorizontalScrollBarEnabled = false
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.mediaPlaybackRequiresUserGesture = false
            webViewClient = object : WebViewClient() {
                override fun shouldInterceptRequest(view: WebView, request: WebResourceRequest): WebResourceResponse? =
                    assets.shouldInterceptRequest(request.url)
            }
            addJavascriptInterface(Bridge(), "RZNative")
            // Crown / rotating bezel: one detent swaps the loaded node during play, scrolls lists elsewhere.
            setOnGenericMotionListener { _, ev ->
                if (ev.action == MotionEvent.ACTION_SCROLL && ev.isFromSource(InputDevice.SOURCE_ROTARY_ENCODER)) {
                    val d = if (-ev.getAxisValue(MotionEvent.AXIS_SCROLL) > 0) 1 else -1
                    evaluateJavascript("window.rzRotary && window.rzRotary($d)", null)
                    true
                } else false
            }
        }
        setContentView(web)
        web.loadUrl("https://appassets.androidplatform.net/assets/index.html")
        web.requestFocus()

        if (Build.VERSION.SDK_INT >= 33) {
            onBackInvokedDispatcher.registerOnBackInvokedCallback(OnBackInvokedDispatcher.PRIORITY_DEFAULT) { handleBack() }
        }
    }

    /** Let the game use the back press (close a sheet, pause, resume); on its main menu the app closes. */
    private fun handleBack() {
        web.evaluateJavascript("window.rzBack ? window.rzBack() : false") { r -> if (r != "true") finish() }
    }

    @Deprecated("Used below API 33")
    override fun onBackPressed() { handleBack() }

    override fun onResume() { super.onResume(); web.onResume() }
    override fun onPause() { web.onPause(); window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON); super.onPause() }
    override fun onDestroy() { web.destroy(); super.onDestroy() }

    inner class Bridge {
        @JavascriptInterface
        fun keepAwake(on: Boolean) = runOnUiThread {
            if (on) window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            else window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        }

        @JavascriptInterface
        fun vibrate(ms: Int) {
            @Suppress("DEPRECATION")
            val v = getSystemService(VIBRATOR_SERVICE) as? Vibrator ?: return
            v.vibrate(VibrationEffect.createOneShot(ms.coerceIn(5, 200).toLong(), VibrationEffect.DEFAULT_AMPLITUDE))
        }
    }
}
