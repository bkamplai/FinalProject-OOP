import pyautogui

class Solver:
    def __init__(self, board) -> None:
        """
        Initialize the solver.
        board (Board): The gameboard
        strategy (Strategy): The desired strategy to use
        """
        self.board = board
        self.strategy = None

    def set_strategy(self, strategy):
        """ Set the desired strategy for the solver. """
        self.strategy = strategy

    def solve(self):
        """ 
        Solve the game.
        Make sure there is a strategy selected.
        Use the desired strategy to solve the game.
        """
        if not self.strategy:
            raise ValueError("Strategy not set!")
        self.strategy.solve(self.board)

    def move(self) -> None:
        """ 
        Do a move on the game board based on the current strategy.
        Iterate over all pieces on the board, checks neighbors, decides if should open unflagged tile
        or flag tiles based on state of neighbords.
        """
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
                elif around == unknown: # Changed from if to elif
                    self.flag_all(neighbors)

    def open_unflagged(self, neighbors) -> None:
        """ Open unflagged tiles in the given spaces.
        neighbors (list): List of neighboring spaces """
        for piece in neighbors:
            if not piece.get_flagged():
                self.board.handle_click(piece, False)

    def flag_all(self, neighbors) -> None: #MAKE SURE THIS LOGIC CHANGES FLAG COUNT!
        """ Flag all unflagged tiles in given neighbors. """
        for piece in neighbors:
            if not piece.get_flagged():
                self.board.handle_click(piece, True)