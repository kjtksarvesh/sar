[app]
title = Tamil Voice Assistant
package.name = tamilvoiceassistant
package.domain = org.example
source.include_exts = py
version = 1.0
source.dir = .
requirements = python3,kivy,speechrecognition,pyttsx3,pyaudio,re,certifi,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 23b
android.ndk_flags = -Wno-macro-redefined
android.ndk_path = /root/.buildozer/android/platform/android-ndk-r23b
android.sdk_path = /root/.buildozer/android/platform/android-sdk
p4a.branch = master
p4a.fork = kivy/python-for-android
android.archs = arm64-v8a, armeabi-v7a
android.gradle_dependencies = com.android.support:support-v4:28.0.0

[buildozer]
log_level = 2
warn_on_root = 1
