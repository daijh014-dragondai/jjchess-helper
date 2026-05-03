[app]

# 应用信息
title = JJChessAssistant
package.name = jjchesshelper
package.domain = org.jjchess.assistant
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0

# Python 依赖
requirements = hostpython3,python3,kivy==2.3.1,pyjnius,android

# 权限
android.permissions = SYSTEM_ALERT_WINDOW,INTERNET
android.api = 34
android.minapi = 29
android.ndk = 25b
android.ndk_api = 33

# 包名
android.package_name = jjchesshelper

# ARM64
android.archs = arm64-v8a

# 屏幕方向
android.orientation = landscape

# 调试模式（开console方便抓崩溃日志）
android.debug = True
android.console = True

# 日志全开
android.logcat_filters = *:V python:V

[buildozer]
log_level = 2
build_dir = ../.buildozer
bin_dir = ./bin
android.build_timeout = 600
warn_on_root = True
