# ♟ JJ象棋AI悬浮助手

> 华为Mate系列手机专用 - JJ象棋智能辅助工具

## 功能

- **悬浮窗模式**：半透明悬浮窗常驻屏幕最上层，不遮挡棋盘
- **AI 棋力分析**：输入对手走法，返回大师级最优应对
- **30% 透明度**：半透明白色背景，不干扰游戏视线
- **零侵入**：仅申请悬浮窗和网络权限，不读取屏幕、不操控游戏

## 截图

| 桌面测试版 | 手机效果 |
|-----------|---------|
| 带半透明背景的小窗口，可拖动、可最小化 | 悬浮在JJ象棋之上的半透明助手 |

## 安装说明

### 方案一：桌面测试（Windows/Mac/Linux）

```bash
# 1. 进入项目目录
cd chess_ai

# 2. 安装依赖
pip install kivy pillow

# 3. 运行
python main.py
```

### 方案二：安卓APK安装（推荐）

#### 步骤1：生成APK文件

**方式A - Docker（最简单，无需安装环境）**：
```bash
# 在 chess_ai 目录下执行
docker run --rm \
  -v ${PWD}:/app \
  -v ~/.buildozer:/home/user/.buildozer \
  ghcr.io/kivy/buildozer:latest \
  android debug
```

**方式B - Linux 原生**：
```bash
# Ubuntu/Debian
sudo apt install python3-pip openjdk-17-jdk unzip
pip3 install buildozer cython
buildozer android debug
```

**方式C - Windows WSL2**：
```powershell
# 在 WSL2 Ubuntu 中执行
sudo apt update
sudo apt install python3-pip openjdk-17-jdk unzip
pip3 install buildozer cython
cd /path/to/chess_ai
buildozer android debug
```

编译完成后，APK 文件生成在 `chess_ai/bin/` 目录下，文件名类似 `JJChessHelper-1.0.0-xxxx-debug.apk`。

#### 步骤2：传输APK到手机

将 APK 文件传到华为手机（USB、微信、蓝牙等均可）。

#### 步骤3：开启安装未知来源应用

1. 打开 **设置** → **安全** → **更多安全设置**
2. 开启 **安装未知来源应用**
3. 找到文件管理器或你使用的传输工具，开启 **允许安装应用**

#### 步骤4：开启悬浮窗权限

安装后，首次启动需要授权悬浮窗权限：

1. 打开 **设置** → **应用** → **应用管理**
2. 找到 **JJ象棋AI悬浮助手**
3. 点击 **权限** → 开启 **悬浮窗**

或者：
1. 打开 **设置** → **应用** → **权限管理**
2. 点击右上角 **⚙️** → **特殊访问权限**
3. 选择 **显示在其他应用的上层**
4. 找到 **JJ象棋AI悬浮助手** 并开启

#### 步骤5：使用

1. 打开 JJ象棋，开始对局
2. 切回助手APP，点击启动悬浮窗
3. 对手走棋后，在悬浮窗输入对手走法
4. 点击「获取建议」获取大师级应对

## 使用方法

### 基本流程

1. 启动应用后，悬浮窗出现在屏幕上方
2. 在JJ象棋中开始对局
3. **轮到对手走棋时**：对手落子后，在悬浮窗输入框输入对手的走法
4. 点击 **「获取建议」** 按钮
5. 悬浮窗底部显示推荐走法（如「我方建议：炮二平五」）
6. 按照建议在JJ象棋中落子

### 走法输入格式

- **红方走法**：炮**二**平五、马**二**进三、车**一**进一
- **黑方走法**：马**8**进7、车**9**平8、炮**8**进2

> 红方用中文一~九，黑方用阿拉伯数字1~9，与JJ象棋完全一致

### 示例

```
JJ象棋中对手走了：炮二平五
悬浮窗输入：炮二平五
点击获取建议 → 显示：我方建议：马8进7
```

## 常见问题

**Q: 悬浮窗不显示？**
A: 请确保已在系统设置中开启「显示悬浮窗」权限

**Q: 提示未知来源无法安装？**
A: 在「设置 → 安全」中开启「安装未知来源应用」

**Q: 华为鸿蒙系统是否兼容？**
A: 兼容，Android 10+ / HarmonyOS 均可使用

**Q: AI 建议不准确？**
A: chessdb 数据库收录了数十万大师对局，提供大师级水平的走法建议。但象棋没有绝对最优解，仅供参考

## 项目文件

```
chess_ai/
├── chess_core.py        # 象棋引擎 + API 集成
├── chess_helper.py      # Kivy 界面 + Android悬浮窗
├── main.py              # 启动入口
├── buildozer.spec       # APK 打包配置
├── test_app.py          # 功能测试
└── README.md            # 本文件
```

## 技术说明

- 开发语言：Python 3.12
- 界面框架：Kivy 2.3.1
- 打包工具：Buildozer
- API 数据源：http://www.chessdb.cn/ （免费象棋数据库）
- 最低系统：Android 10（API 29）
- 推荐系统：Android 11+ / HarmonyOS 3+
