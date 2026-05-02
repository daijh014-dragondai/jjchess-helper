"""
main.py - JJ象棋AI悬浮助手 入口文件
Buildozer 需要此文件作为启动入口
"""
import sys
import os

# 确保当前目录在模块搜索路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chess_helper import JJChessApp

if __name__ == '__main__':
    JJChessApp().run()
