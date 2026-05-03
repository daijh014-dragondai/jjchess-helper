[app]

# 应用信息
title = JJChessAssistant
package.name = jjchesshelper
package.domain = org.jjchess.assistant
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0

# Python 依赖
requirements = python3,kivy==2.3.1,hostpython3,pyjnius,android

# 权限
android.permissions = SYSTEM_ALERT_WINDOW,INTERNET
android.api = 34
android.minapi = 29
android.ndk = 25b
android.ndk_api = 29

# 包名
android.package_name = jjchesshelper

# ARM64
android.archs = arm64-v8a

# 语言
android.language = zh

# 后台保活
android.foreground = True

# 屏幕方向
android.orientation = landscape

# 不要唤醒锁
android.wakelock = False

# 调试模式
android.debug = True
android.console = True

# 日志
android.logcat_filters = *:S python:V

# 使用Surface渲染
android.use_surface = True

# 窗口背景透明
android.window_background = 00000000

[buildozer]

log_level = 2
build_dir = ../.buildozer
bin_dir = ./bin
android.build_timeout = 600
warn_on_root = True
