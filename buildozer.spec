[app]

# 应用信息
title = JJ象棋AI悬浮助手
package.name = jjchesshelper
package.domain = org.jjchess.assistant
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# Python 依赖（Buildozer自动编译）
requirements = python3,kivy==2.3.1,hostpython3,pyjnius,android

# 权限
android.permissions = SYSTEM_ALERT_WINDOW,INTERNET
android.api = 31
android.minapi = 29
android.ndk = 25b
android.ndk_api = 29

# 包名
android.package_name = jjchesshelper

# AndroidX（必需）
android.enable_androidx = True
android.gradle_dependencies = 'androidx.core:core:1.9.0'

# ARM64（华为麒麟/骁龙）
android.archs = arm64-v8a

# 语言
android.language = zh

# 后台保活（悬浮窗服务）
android.foreground = True
android.foreground_service = True

# 屏幕方向
android.orientation = portrait

# 不要唤醒锁
android.wakelock = False

# 发布模式
android.debug = False
android.console = False

# 日志
android.logcat_filters = *:S python:V

# 签名（发布时需要，测试使用debug key即可）
# android.keystore = 
# android.keystore.alias = 

# 使用Surface渲染
android.use_surface = True

# 窗口背景透明
android.window_background = 00000000

[buildozer]

log_level = 2
build_dir = ../.buildozer
bin_dir = ./bin
android.arch = arm64-v8a
android.build_timeout = 600
warn_on_root = True

# Docker 构建命令：
# docker run --rm -v ${PWD}:/app -v ~/.buildozer:/home/user/.buildozer ghcr.io/kivy/buildozer:latest android debug
