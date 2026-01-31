class GameState:
    __slots__ = (
        "turn",
        "moves",
        "king_moved",
        "last_move",
        "board",
    )

    def __init__(
        self,
        *,
        turn=1,
        moves=0,
        king_moved=None,
        last_move=None,
        board=None,
    ):
        self.turn = turn
        self.moves = moves
        self.king_moved = (["None", "0", "0"] if king_moved is None else list(king_moved))
        self.last_move = None if last_move in (None, "None") else list(last_move)
        self.board = {} if board is None else dict(board)

    def copy(self):
        return GameState(
            turn=self.turn,
            moves=self.moves,
            king_moved=self.king_moved.copy(),
            last_move=None if self.last_move is None else self.last_move.copy(),
            board=self.board.copy(),
        )

    def to_dict(self):
        return {
            "turn": self.turn,
            "moves": self.moves,
            "king_moved": self.king_moved.copy(),
            "last_move": None if self.last_move is None else self.last_move.copy(),
            "board": self.board.copy(),
        }

    @staticmethod
    def from_dict(d):
        return GameState(
            turn=d.get("turn", 1),
            moves=d.get("moves", 0),
            king_moved=d.get("king_moved", ["None", "False", "False"]),
            last_move=d.get("last_move", None),
            board=d.get("board", {}),
        )