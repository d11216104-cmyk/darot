# gomoku_cli.py
# Python 3.x
# 15x15 命令列五子棋（雙人對戰）

SIZE = 15
EMPTY = "."
P1 = "X"  # 黑
P2 = "O"  # 白

def new_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def print_board(board):
    # 顯示欄號 1..15
    header = "    " + " ".join(f"{i:2d}" for i in range(1, SIZE + 1))
    print(header)
    for r in range(SIZE):
        row_label = f"{r+1:2d}  "
        print(row_label + " " + " ".join(f"{board[r][c]:2s}" for c in range(SIZE)))

def in_bounds(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE

def count_dir(board, r, c, dr, dc, stone):
    cnt = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == stone:
        cnt += 1
        rr += dr
        cc += dc
    return cnt

def is_win(board, r, c):
    stone = board[r][c]
    if stone == EMPTY:
        return False

    # 四個方向：水平、垂直、兩條斜線
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # 往正向與反向計數（包含自己）
        total = (
            count_dir(board, r, c, dr, dc, stone) +
            count_dir(board, r, c, -dr, -dc, stone) - 1
        )
        if total >= 5:
            return True
    return False

def parse_move(s):
    """
    允許輸入：
    - "8 8"
    - "8,8"
    - "8, 8"
    回傳 (r, c) 為 0-based
    """
    s = s.strip().replace(",", " ")
    parts = [p for p in s.split() if p]
    if len(parts) != 2:
        return None
    try:
        r = int(parts[0]) - 1
        c = int(parts[1]) - 1
    except ValueError:
        return None
    if not in_bounds(r, c):
        return None
    return r, c

def main():
    board = new_board()
    player = 1
    moves = 0
    max_moves = SIZE * SIZE

    print("五子棋（命令列 15x15）")
    print("輸入格式：row col（例如：8 8）或 row,col（例如：8,8）")
    print("先手 X（黑），後手 O（白）\n")

    while True:
        print_board(board)
        stone = P1 if player == 1 else P2
        prompt = f"\n玩家 {player} ({stone}) 請落子："

        raw = input(prompt)
        mv = parse_move(raw)
        if mv is None:
            print("輸入格式錯誤或超出範圍，請重試。\n")
            continue

        r, c = mv
        if board[r][c] != EMPTY:
            print("此位置已有棋子，請重試。\n")
            continue

        board[r][c] = stone
        moves += 1

        if is_win(board, r, c):
            print_board(board)
            print(f"\n玩家 {player} ({stone}) 獲勝！")
            break

        if moves >= max_moves:
            print_board(board)
            print("\n平手（棋盤已滿）")
            break

        player = 2 if player == 1 else 1
        print()

if __name__ == "__main__":
    main()
