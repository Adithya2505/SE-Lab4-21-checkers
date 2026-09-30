SIZE = 8


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    direction = -1 if player == "R" else 1
    return (
        board[er][ec] == "." and
        abs(er - sr) == 1 and abs(ec - sc) == 1 and
        er - sr == direction
    )


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    direction = -1 if player == "R" else 1
    mr, mc = (sr + er) // 2, (sc + ec) // 2
    return (
        board[er][ec] == "." and
        abs(er - sr) == 2 and abs(ec - sc) == 2 and
        er - sr == 2 * direction and
        board[mr][mc] not in (".", player, player + "K")    
    )


def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"

def has_legal_move(board, player):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] in (player, player + "K"):
                for dr in (-2, -1, 1, 2):
                    for dc in (-2, -1, 1, 2):
                        er, ec = r + dr, c + dc
                        if 0 <= er < SIZE and 0 <= ec < SIZE:
                            if simple_move(board, player, (r, c), (er, ec)) or \
                               capture_move(board, player, (r, c), (er, ec)):
                                return True
    return False