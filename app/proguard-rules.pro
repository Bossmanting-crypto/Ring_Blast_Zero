# Keep the methods the game calls through window.RZNative
-keepclassmembers class com.ringblastzero.wear.MainActivity$Bridge {
    @android.webkit.JavascriptInterface <methods>;
}
