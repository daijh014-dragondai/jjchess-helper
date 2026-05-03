[app]

title = JJChessAssistant
package.name = jjchesshelper
package.domain = org.jjchess.assistant
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = hostpython3,python3,kivy==2.3.1,pyjnius,android

# 权限
android.permissions = SYSTEM_ALERT_WINDOW,INTERNET

# SDK/NDK
android.api = 34
android.minapi = 29
android.ndk = 25b
android.ndk_api = 33

android.archs = arm64-v8a
android.orientation = portrait

# 调试模式
android.debug = True
android.console = True

# 禁用 AndroidX（新版Buildozer默认开启，但会导致Gradle错误）
android.enable_androidx = False

# 日志
android.logcat_filters = *:V python:V

[buildozer]
log_level = 2
build_dir = ../.buildozer
bin_dir = ./bin
android.build_timeout = 600
warn_on_root = True
