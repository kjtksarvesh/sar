[app]
title = Tamil Form Fill AI
package.name = tamil_form_ai
package.domain = org.tamilbot
source.include_exts = py,png,jpg,kv,atlas
python = 3.9
android.sdk_path = /root/.buildozer/android/platform/android-sdk
android.ndk_path = /root/.buildozer/android/platform/android-ndk

# (str) Source code directory
source.dir = .

# (list) Permissions
android.permissions = INTERNET, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (bool) Enable Android logcat
android.logcat = 1

# (str) Package format: 'apk', 'aab'
android.package_type = apk

# (str) Application versioning
version = 1.0.0

# (str) Supported platforms
requirements = python3, kivy, speechrecognition, pyttsx3, numpy, android

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (str) Application icon (replace with your own icon)
icon.filename = icon.png

# (bool) Disable the Android presplash screen
android.disable_presplash = 1

# (list) Add assets folder for additional files
android.add_asset_dirs = assets

# (str) Minimum API level (e.g., 21 for Android 5.0+)
android.minapi = 21

# (str) Target API level
android.api = 33

android.pip = https://github.com/johnnewto/pyaudio_android/archive/master.zip


# (str) Architecture (armeabi-v7a, arm64-v8a, x86, x86_64)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Indicate whether to use OpenGL ES 2
android.opengl_es = 2
