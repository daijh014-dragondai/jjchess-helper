"""
main.py - JJ象棋AI悬浮助手 入口文件
"""
import sys
import os
import logging

# Android环境下，日志输出到文件方便调试
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crash.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

try:
    # 确保当前目录在模块搜索路径中
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    logging.info('Starting JJ Chess Assistant...')

    from chess_helper import JJChessApp

    if __name__ == '__main__':
        logging.info('Creating app instance...')
        app = JJChessApp()
        logging.info('Running app...')
        app.run()
except Exception as e:
    logging.exception('Fatal startup error')
    # 也输出到stdout（adb logcat能看到）
    print(f'CRASH: {e}', flush=True)
    import traceback
    traceback.print_exc()
