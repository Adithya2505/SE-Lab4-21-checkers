from board import initial_board, move_piece, SIZE
from rules import simple_move, capture_move, promote, has_legal_move, has_capture

class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"
        self.chain = None

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def run(self):
        print("Checkers — move: sr sc er ec")
        while True:
            self.print_board()
            if not has_legal_move(self.board, self.player):
                winner = "B" if self.player == "R" else "R"
                print(f"{self.player} has no pieces or no legal moves. {winner} wins!")
                return
            try:
                raw = input(f"{self.player}> ").strip().lower().split()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                return
            if raw == ["q"]:
                print("\nGoodbye.")
                return
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue
            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            start, end = (sr, sc), (er, ec)
            if self.chain and start != self.chain:
                print("You must keep jumping with the same piece.")
                continue
            was_man = not self.board[sr][sc].endswith("K")
            if capture_move(self.board, self.player, start, end):
                jumped = True
            elif simple_move(self.board, self.player, start, end):
                if has_capture(self.board, self.player):
                    print("You must capture.")
                    continue
                jumped = False
            else:
                print("Invalid move.")
                continue

            move_piece(self.board, start, end)
            promote(self.board)
            crowned = was_man and self.board[er][ec].endswith("K")
            again = jumped and not crowned and has_capture(self.board, self.player, end)
            msg = f"{self.player} {'captured' if jumped else 'moved'} {start} -> {end}"
            if crowned:
                msg += " and was crowned king"
            print(msg + (". Jump again!" if again else "."))
            if again:
                self.chain = end
                continue
            self.chain = None
            self.player = "B" if self.player == "R" else "R"