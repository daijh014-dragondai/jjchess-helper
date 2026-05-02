"""
chess_helper.py - JJ象棋AI悬浮助手 主程序
"""

import os
import sys
import threading

# ─── Windows控制台编码 ───
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from chess_core import INITIAL_FEN, apply_move_and_query as move_query

# ═══ 关键：设置 Kivy 默认字体支持中文 ═══
import kivy
kivy.require('2.2.0')

from kivy.config import Config

# 查找系统中文字体
_CJK_FONT_PATH = None
if sys.platform == 'win32':
    win_dir = os.environ.get('WINDIR', 'C:\\Windows')
    for f in ['msyh.ttc', 'msyhbd.ttc', 'simsun.ttc', 'simhei.ttf']:
        p = os.path.join(win_dir, 'Fonts', f)
        if os.path.exists(p):
            _CJK_FONT_PATH = p
            break
elif sys.platform == 'darwin':
    for f in ['/System/Library/Fonts/PingFang.ttc',
              '/System/Library/Fonts/STHeiti Light.ttc']:
        if os.path.exists(f):
            _CJK_FONT_PATH = f
            break
else:
    for f in ['/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
              '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']:
        if os.path.exists(f):
            _CJK_FONT_PATH = f
            break

if _CJK_FONT_PATH:
    # 在Kivy启动前设置默认字体（格式: [字体名, 字体路径]）
    Config.set('kivy', 'default_font', ['CJK', _CJK_FONT_PATH])

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform as kivy_platform
from kivy.logger import Logger

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

ANDROID = kivy_platform == 'android'

# 默认字体名
_FONT_NAME = 'CJK'  # 与Config.default_font设置一致


# ============================================================
# 对局状态管理
# ============================================================

class GameState:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.current_fen = INITIAL_FEN
        self.history = []
        self.move_count = 0
    
    def process(self, opponent_move: str) -> dict:
        result = move_query(self.current_fen, opponent_move)
        if result.get('success'):
            self.current_fen = result.get('new_fen', self.current_fen)
            self.history.append({
                'opponent': opponent_move,
                'our': result['suggestion'],
            })
            self.move_count += 1
        return result


# ============================================================
# 自定义中文控件（强制使用中文字体）
# ============================================================

class CJKLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_name', _FONT_NAME)
        super().__init__(**kwargs)

class CJKButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_name', _FONT_NAME)
        super().__init__(**kwargs)

class CJKTextInput(TextInput):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_name', _FONT_NAME)
        super().__init__(**kwargs)


# ============================================================
# 桌面悬浮窗界面
# ============================================================

class ChessOverlay(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = GameState()
        self._busy = False
        self._build()
    
    def _build(self):
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(320), dp(230))
        self.spacing = dp(3)
        self.padding = [dp(10), dp(6)]
        
        # 半透明背景
        with self.canvas.before:
            Color(1, 1, 1, 0.30)
            self.bg = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(12)]
            )
        self.bind(pos=self._upd_bg, size=self._upd_bg)
        
        # ── 标题栏 ──
        tb = BoxLayout(orientation='horizontal',
                       size_hint=(1, None), height=dp(28))
        
        self.tl = CJKLabel(
            text='♪ JJ象棋AI悬浮助手',
            size_hint=(0.65, 1),
            halign='left', valign='middle',
            color=(0.15, 0.15, 0.15, 1),
            font_size=dp(13), bold=True
        )
        self.tl.bind(size=self.tl.setter('text_size'))
        
        self.bm = CJKButton(
            text='－', size_hint=(0.15, 1),
            background_color=(0.5, 0.5, 0.5, 0.4),
            color=(0.3, 0.3, 0.3, 1), font_size=dp(16)
        )
        self.bm.bind(on_press=self._mini)
        
        self.bx = CJKButton(
            text='×', size_hint=(0.20, 1),
            background_color=(0.7, 0.2, 0.2, 0.5),
            color=(1, 1, 1, 1), font_size=dp(16), bold=True
        )
        self.bx.bind(on_press=lambda x: App.get_running_app().stop())
        
        tb.add_widget(self.tl)
        tb.add_widget(self.bm)
        tb.add_widget(self.bx)
        
        # ── 输入框 ──
        self.ti = CJKTextInput(
            hint_text='输入对手走法（如：马8进7）',
            size_hint=(1, None), height=dp(38),
            multiline=False, font_size=dp(15),
            padding=[dp(10), dp(8)],
            background_color=(1, 1, 1, 0.55),
            foreground_color=(0.05, 0.05, 0.05, 1),
            hint_text_color=(0.4, 0.4, 0.4, 0.7)
        )
        self.ti.bind(on_text_validate=self._click)
        
        # ── 按钮行 ──
        br = BoxLayout(orientation='horizontal',
                       size_hint=(1, None), height=dp(40),
                       spacing=dp(5))
        
        self.bs = CJKButton(
            text='[ 获取建议 ]',
            size_hint=(0.65, 1),
            background_color=(0.12, 0.42, 0.72, 0.75),
            color=(1, 1, 1, 1),
            font_size=dp(16), bold=True
        )
        self.bs.bind(on_press=self._click)
        
        self.br = CJKButton(
            text='[ 重置 ]',
            size_hint=(0.35, 1),
            background_color=(0.5, 0.5, 0.5, 0.45),
            color=(0.15, 0.15, 0.15, 1),
            font_size=dp(14)
        )
        self.br.bind(on_press=self._reset)
        
        br.add_widget(self.bs)
        br.add_widget(self.br)
        
        # ── 结果区域 ──
        self.lr = CJKLabel(
            text='等待输入对方走法...',
            size_hint=(1, 1),
            halign='center', valign='middle',
            color=(0.05, 0.05, 0.05, 1),
            font_size=dp(24), bold=True
        )
        self.lr.bind(size=self.lr.setter('text_size'))
        
        self.add_widget(tb)
        self.add_widget(self.ti)
        self.add_widget(br)
        self.add_widget(self.lr)
    
    def _upd_bg(self, *a):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def _mini(self, *a):
        self.opacity = 0.1
    
    def _click(self, *a):
        if self._busy:
            return
        mv = self.ti.text.strip()
        if not mv:
            self.lr.text = '请输入对手走法'
            return
        
        self._busy = True
        self.lr.text = '查询中...'
        self.bs.disabled = True
        self.bs.text = '[ 查询中 ]'
        
        threading.Thread(target=self._do, args=(mv,), daemon=True).start()
    
    def _do(self, mv):
        try:
            r = self.game.process(mv)
            Clock.schedule_once(lambda dt: self._res(r), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._err(str(e)), 0)
    
    def _res(self, r):
        if r.get('success'):
            self.lr.text = '我方建议：' + r['suggestion']
        else:
            self.lr.text = r.get('message', '未知错误')
        self._busy = False
        self.bs.disabled = False
        self.bs.text = '[ 获取建议 ]'
    
    def _err(self, m):
        self.lr.text = '错误：' + m
        self._busy = False
        self.bs.disabled = False
        self.bs.text = '[ 获取建议 ]'
    
    def _reset(self, *a):
        self.game.reset()
        self.ti.text = ''
        self.lr.text = '已重置，重新开始'
        self._busy = False
        self.bs.disabled = False
        self.bs.text = '[ 获取建议 ]'


# ============================================================
# Kivy 应用主入口
# ============================================================

class JJChessApp(App):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.widget = None
        self._drag_from = None
    
    def build(self):
        if ANDROID:
            Window.clearcolor = (0, 0, 0, 0)
            Window.size = (dp(100), dp(100))
            Window.borderless = True
            from kivy.uix.widget import Widget
            return Widget()
        
        # 桌面模式：无边框 + 置顶
        Window.size = (dp(340), dp(250))
        Window.clearcolor = (0.92, 0.92, 0.92, 0.15)
        try:
            Window.borderless = True
        except:
            pass
        try:
            Window.set_always_on_top(True)
        except:
            pass
        
        root = FloatLayout()
        self.widget = ChessOverlay()
        root.add_widget(self.widget)
        
        # 拖动
        root.bind(on_touch_down=self._drag_start,
                  on_touch_move=self._drag_move)
        
        return root
    
    def _drag_start(self, w, t):
        if self.widget and self.widget.collide_point(*t.pos):
            self._drag_from = (t.x - self.widget.x, t.y - self.widget.y)
    
    def _drag_move(self, w, t):
        if self._drag_from and self.widget:
            self.widget.x = t.x - self._drag_from[0]
            self.widget.y = t.y - self._drag_from[1]
    
    def on_pause(self):
        return True


if __name__ == '__main__':
    JJChessApp().run()
