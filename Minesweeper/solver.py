import pyautogui

class Solver:
    def __init__(self, board) -> None:
        self.board = board

    def move(self) -> None:
        for row in self.board.get_board():
            for piece in row:
                if not piece.get_clicked():
                    continue
                around = piece.get_num_around()
                unknown = 0
                flagged = 0
                neighbors = piece.get_neighbors()
                for p in neighbors:
                    if not p.get_clicked():
                        unknown += 1
                    if p.get_flagged():
                        flagged += 1
                if around == flagged:
                    self.open_unflagged(neighbors)
                if around == unknown:
                    self.flag_all(neighbors)

    def open_unflagged(self, neighbors) -> None:
        for piece in neighbors:
            if not piece.get_flagged():
                self.board.handle_click(piece, False)


    def flag_all(self, neighbors) -> None:
        for piece in neighbors:
            if not piece.get_flagged():
                self.board.handle_click(piece, True)