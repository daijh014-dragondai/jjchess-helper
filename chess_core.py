"""
chess_core.py - 中国象棋核心逻辑与 API 集成
支持：FEN解析/生成、UCCI走法与中文记谱互转、
      API查询（chessdb.cn）、棋盘状态管理
"""

import urllib.request
import urllib.parse

# ─── 常量定义 ───

API_URL = "http://www.chessdb.cn/chessdb.php"

# 棋子中文名
RED_NAMES = {'R': '车', 'N': '马', 'B': '相', 'A': '仕', 'K': '帅', 'C': '炮', 'P': '兵'}
BLACK_NAMES = {'r': '车', 'n': '马', 'b': '象', 'a': '士', 'k': '将', 'c': '炮', 'p': '卒'}
ALL_NAMES = {**RED_NAMES, **BLACK_NAMES}

# 中文数字
RED_DIGITS = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']
BLACK_DIGITS = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# 初始局面 FEN（FEN 格式：row 0=棋盘顶端=黑方底线，row 9=棋盘底端=红方底线）
INITIAL_FEN = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"


# ─── 棋盘操作 ───

def fen_to_board(fen: str) -> list:
    """将 FEN 字符串解析为 10x9 棋盘数组 board[board_row][col]
    
    FEN 编码: row 0=棋盘顶端(黑方底线), row 9=棋盘底端(红方底线)
    UCCI 编码: row 0=棋盘底端(红方底线), row 9=棋盘顶端(黑方底线)
    
    board[i] 与 FEN 保持一致: board[0]=顶端, board[9]=底端
    """
    board_part = fen.split(' ')[0]
    rows = board_part.split('/')
    board = []
    for row_str in rows:
        row = []
        for ch in row_str:
            if ch.isdigit():
                row.extend([''] * int(ch))
            else:
                row.append(ch)
        board.append(row)
    return board


def board_to_fen(board: list, turn: str = 'w') -> str:
    """将 10x9 棋盘数组转回 FEN 字符串"""
    rows = []
    for row in board:
        fen_row = ''
        empty = 0
        for cell in row:
            if cell == '':
                empty += 1
            else:
                if empty > 0:
                    fen_row += str(empty)
                    empty = 0
                fen_row += cell
        if empty > 0:
            fen_row += str(empty)
        rows.append(fen_row)
    return '/'.join(rows) + f' {turn} - - 0 1'


def copy_board(board: list) -> list:
    """深拷贝棋盘"""
    return [row[:] for row in board]


def ucci_to_board_row(ucci_row: int) -> int:
    """UCCI 行号 → 棋盘数组索引
    
    UCCI: row 0=底端(红方), row 9=顶端(黑方)
    棋盘: index 0=顶端(黑方), index 9=底端(红方)
    """
    return 9 - ucci_row


def board_to_ucci_row(board_row: int) -> int:
    """棋盘数组索引 → UCCI 行号"""
    return 9 - board_row


# ─── 中文记谱 ↔ UCCI 转换 ───

def ucci_to_chinese(board: list, ucci_move: str, is_red: bool) -> str:
    """
    将 UCCI 走法转为中文记谱法。
    UCCI格式: 'b2e2' (源列源行目标列目标行，行0=底端)
    中文格式: '炮二平五'
    """
    # 解析 UCCI
    src_col = ord(ucci_move[0]) - ord('a')  # 0-8
    src_row_ucci = int(ucci_move[1])        # 0-9 (UCCI: 0=底端)
    dst_col = ord(ucci_move[2]) - ord('a')
    dst_row_ucci = int(ucci_move[3])
    
    # 转棋盘索引
    src_row = ucci_to_board_row(src_row_ucci)
    dst_row = ucci_to_board_row(dst_row_ucci)
    
    piece = board[src_row][src_col]
    if not piece:
        return None
    
    piece_lower = piece.lower()
    
    # 棋子中文名
    piece_name = RED_NAMES.get(piece) if is_red else BLACK_NAMES.get(piece)
    if not piece_name:
        return None
    
    # 列号（中文记谱）
    digits = RED_DIGITS if is_red else BLACK_DIGITS
    if is_red:
        src_col_ch = digits[9 - src_col]  # UCCI col a(0) = 红方9路
    else:
        src_col_ch = digits[src_col + 1]  # UCCI col a(0) = 黑方1路
    
    # 方向（UCCI: row小=底端/红方; row大=顶端/黑方）
    if src_row_ucci == dst_row_ucci:
        direction = '平'
    elif is_red:
        # 红方：进 = UCCI row 增大（向顶端/黑方前进）
        direction = '进' if dst_row_ucci > src_row_ucci else '退'
    else:
        # 黑方：进 = UCCI row 减小（向底端/红方前进）
        direction = '进' if dst_row_ucci < src_row_ucci else '退'
    
    # 目标值
    if direction == '平':
        if is_red:
            dst_val = RED_DIGITS[9 - dst_col]
        else:
            dst_val = BLACK_DIGITS[dst_col + 1]
    elif piece_lower in ('n', 'b', 'a'):
        # 马、象/相、士/仕：目标值是列号
        if is_red:
            dst_val = RED_DIGITS[9 - dst_col]
        else:
            dst_val = BLACK_DIGITS[dst_col + 1]
    else:
        # 车、炮、兵/卒、帅/将：目标值是步数
        steps = abs(dst_row_ucci - src_row_ucci)
        if is_red:
            dst_val = RED_DIGITS[steps]
        else:
            dst_val = BLACK_DIGITS[steps]
    
    return f'{piece_name}{src_col_ch}{direction}{dst_val}'


def apply_ucci_move(board: list, ucci_move: str) -> list:
    """在棋盘上应用 UCCI 走法，返回新棋盘"""
    src_col = ord(ucci_move[0]) - ord('a')
    src_row_ucci = int(ucci_move[1])
    dst_col = ord(ucci_move[2]) - ord('a')
    dst_row_ucci = int(ucci_move[3])
    
    src_row = ucci_to_board_row(src_row_ucci)
    dst_row = ucci_to_board_row(dst_row_ucci)
    
    new_board = copy_board(board)
    piece = new_board[src_row][src_col]
    new_board[src_row][src_col] = ''
    new_board[dst_row][dst_col] = piece
    return new_board


# ─── API 集成 ───

def query_api(action: str, fen: str) -> str:
    """
    调用 chessdb.cn API。
    
    参数:
        action: 'querybest' | 'queryall'
        fen: 当前局面 FEN
        
    返回:
        API 原始响应文本
    """
    params = urllib.parse.urlencode({
        'action': action,
        'board': fen
    })
    url = f'{API_URL}?{params}'
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'JJChessHelper/1.0',
            'Accept': '*/*'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8').strip().rstrip('\x00').strip()
    except urllib.error.URLError as e:
        return f'error: 网络错误 - {str(e)}'
    except Exception as e:
        return f'error: {str(e)}'


def query_best_move(fen: str) -> dict:
    """
    查询当前局面的最佳走法。
    
    返回:
        {
            'success': True/False,
            'ucci': 'b2e2',
            'chinese': '炮八平五',
            'raw': 'move:b2e2'
        }
    """
    raw = query_api('querybest', fen)
    
    result = {
        'success': False,
        'ucci': None,
        'chinese': None,
        'raw': raw
    }
    
    if raw.startswith('move:'):
        ucci = raw[5:].strip()
        result['success'] = True
        result['ucci'] = ucci
        
        # 转换成中文记谱
        board = fen_to_board(fen)
        is_red = fen.split(' ')[1] == 'w'
        chinese = ucci_to_chinese(board, ucci, is_red)
        result['chinese'] = chinese
    
    return result


def query_all_moves(fen: str) -> dict:
    """
    查询当前局面的所有合法走法。
    
    返回:
        {
            'success': True/False,
            'moves': [{'ucci': '...', 'chinese': '...', 'score': 1}, ...],
            'raw': '...'
        }
    """
    raw = query_api('queryall', fen)
    
    result = {
        'success': False,
        'moves': [],
        'raw': raw
    }
    
    if not raw or raw.startswith('error'):
        result['raw'] = raw
        return result
    
    board = fen_to_board(fen)
    is_red = fen.split(' ')[1] == 'w'
    
    parts = raw.split('|')
    moves = []
    for part in parts:
        if not part.startswith('move:'):
            continue
        fields = part.split(',')
        ucci = None
        score = None
        rank = None
        for f in fields:
            if f.startswith('move:'):
                ucci = f[5:]
            elif f.startswith('score:'):
                score = int(f[6:])
            elif f.startswith('rank:'):
                rank = int(f[5:])
        
        if ucci:
            chinese = ucci_to_chinese(board, ucci, is_red)
            moves.append({
                'ucci': ucci,
                'chinese': chinese or '?',
                'score': score,
                'rank': rank
            })
    
    if moves:
        result['success'] = True
        result['moves'] = moves
    
    return result


def apply_move_and_query(fen: str, opponent_move_chinese: str) -> dict:
    """
    完整流程：用户输入对方走法 → 更新棋盘 → 查询我方最佳应对。
    此函数也会自动应用我方最佳走法，保持棋盘同步。

    返回:
        {
            'success': True/False,
            'suggestion': '马二进三',       # 我方建议走法(中文)
            'suggestion_ucci': 'h0g2',      # 我方建议走法(UCCI)
            'new_fen': '...',               # 更新后的完整FEN(已应用双方走法)
            'message': '...'                # 错误提示
        }
    """
    board = fen_to_board(fen)
    
    # 获取当前方所有合法走法
    all_moves = query_all_moves(fen)
    if not all_moves['success']:
        return {
            'success': False,
            'suggestion': None,
            'new_fen': fen,
            'message': f'API查询失败: {all_moves["raw"]}'
        }
    
    # 精确匹配中文走法
    opp_ucci = None
    for m in all_moves['moves']:
        if m['chinese'] == opponent_move_chinese:
            opp_ucci = m['ucci']
            break
    
    if not opp_ucci:
        available = ', '.join([m['chinese'] for m in all_moves['moves'][:8]])
        return {
            'success': False,
            'suggestion': None,
            'new_fen': fen,
            'message': f'未找到走法"{opponent_move_chinese}"。当前合法走法：{available}...'
        }
    
    # 应用对方走法 → 轮到本方面对
    after_opponent = apply_ucci_move(board, opp_ucci)
    is_opponent_red = fen.split(' ')[1] == 'w'
    our_turn = 'b' if is_opponent_red else 'w'
    our_fen = board_to_fen(after_opponent, our_turn)
    
    # 查询我方最佳走法
    best = query_best_move(our_fen)
    
    if not best['success']:
        return {
            'success': False,
            'suggestion': None,
            'new_fen': our_fen,
            'message': f'最佳走法查询失败: {best["raw"]}'
        }
    
    # 应用我方走法 → 保持棋盘同步
    final_board = apply_ucci_move(after_opponent, best['ucci'])
    next_turn = 'w' if is_opponent_red else 'b'
    new_fen = board_to_fen(final_board, next_turn)
    
    return {
        'success': True,
        'suggestion': best['chinese'],
        'suggestion_ucci': best['ucci'],
        'new_fen': new_fen,
        'message': None
    }


# ─── 测试代码 ───

if __name__ == '__main__':
    import sys
    
    print("=" * 50)
    print("       象棋核心模块测试")
    print("=" * 50)
    print()
    
    # 测试1：FEN 解析与重建
    board = fen_to_board(INITIAL_FEN)
    fen_back = board_to_fen(board)
    print(f"[测试1] FEN 解析一致性")
    print(f"  原始: {INITIAL_FEN}")
    print(f"  重建: {fen_back}")
    ok = INITIAL_FEN == fen_back
    print(f"  一致: {'OK' if ok else 'FAIL'}")
    print()
    
    # 测试2：API querybest
    print("[测试2] 调用 API querybest...")
    best = query_best_move(INITIAL_FEN)
    print(f"  响应: {best}")
    print()
    
    # 测试3：API queryall（前10个）
    print("[测试3] 调用 API queryall...")
    all_moves = query_all_moves(INITIAL_FEN)
    if all_moves['success']:
        for m in all_moves['moves'][:10]:
            print(f"  {m['chinese']:>6} ({m['ucci']:>4}) score={'+' if m['score'] and m['score']>0 else ''}{m['score']}")
    print(f"  ...共 {len(all_moves['moves'])} 个合法走法")
    print()
    
    # 测试4：搜索炮二平五
    print("[测试4] 搜索走法 '炮二平五'")
    result = query_all_moves(INITIAL_FEN)
    found = [m for m in result['moves'] if m['chinese'] == '炮二平五']
    if found:
        print(f"  找到: {found[0]}")
    else:
        print("  未找到炮二平五（炮八平五才是这道题的答案）")
    print()
    
    # 测试5：完整流程（假设红方走了炮二平五，查询黑方最佳应对）
    print("[测试5] 输入对方\"炮二平五\" → 查询我方最佳应对")
    # 构建局面：初始FEN，但轮到黑方走
    # 实际上用户输入的是对方走法，我们用queryall查红方走法后更新棋盘
    result = apply_move_and_query(INITIAL_FEN, '炮二平五')
    if result['success']:
        print(f"  我方建议: {result['suggestion']} ({result['suggestion_ucci']})")
    else:
        print(f"  失败: {result['message']}")
    
    # 如果炮二平五不匹配，试炮八平五
    if not result.get('success'):
        print()
        print("[测试5b] 尝试\"炮八平五\"")
        result = apply_move_and_query(INITIAL_FEN, '炮八平五')
        if result['success']:
            print(f"  我方建议: {result['suggestion']} ({result['suggestion_ucci']})")
        else:
            print(f"  失败: {result['message']}")
    print()
    
    # 测试6：打印棋盘
    print("[测试6] 棋盘布局验证")
    print("  红方底线(row9): RNBAKABNR")
    print(f"  board[9] = {''.join(board[9])}")
    print("  黑方底线(row0): rnbakabnr")
    print(f"  board[0] = {''.join(board[0])}")
    print()
    print("  UCCI b2e2 (炮八平五):")
    src_c, src_r, dst_c, dst_r = 1, 2, 4, 2  # UCCI coords
    brd_src_r = ucci_to_board_row(src_r)
    brd_dst_r = ucci_to_board_row(dst_r)
    src_col_letter = chr(ord('a') + src_c)
    dst_col_letter = chr(ord('a') + dst_c)
    print(f"    UCCI: {src_col_letter}{src_r} = col{src_c} UCCI-row{src_r} -> board[{brd_src_r}]")
    print(f"    board[{brd_src_r}][{src_c}] = '{board[brd_src_r][src_c]}'")
    print(f"    UCCI: {dst_col_letter}{dst_r} = col{dst_c} UCCI-row{dst_r} -> board[{brd_dst_r}]")
    print(f"    board[{brd_dst_r}][{dst_c}] = '{board[brd_dst_r][dst_c]}'")
