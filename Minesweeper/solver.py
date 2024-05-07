from typing import List, Optional
from board import Board
from space import Space
from solverstrategy import SolverStrategy


class Solver:
    def __init__(self, board: Board) -> None:
        """
        Initialize the solver.
        board (Board): The gameboard
        strategy (Strategy): The desired strategy to use
        """
        self.board: Board = board
        self.strategy: Optional[SolverStrategy] = None

    def set_strategy(self, strategy: SolverStrategy) -> None:
        """ Set the desired strategy for the solver. """
        self.strategy = strategy

    def solve(self) -> None:
        """
        Solve the game.
        Make sure there is a strategy selected.
        Use the desired strategy to solve the game.
        """
        if not self.strategy:
            raise ValueError("Strategy not set!")
        self.strategy.solve()

    def move(self) -> None:
        """
        Do a move on the game board based on the current strategy. Iterate
        over all pieces on the board, checks neighbors, decides if should open
        unflagged tile or flag tiles based on state of neighbords.
        """
        for row in self.board.get_board():
            for piece in row:
                if not piece.get_clicked():
                    continue
                around: int = piece.get_num_around()
                unknown: int = 0
                flagged: int = 0
                neighbors: List[Space] = piece.get_neighbors()
                for p in neighbors:
                    if not p.get_clicked():
                        unknown += 1
                    if p.get_flagged():
                        flagged += 1
                if around == flagged:
                    self.open_unflagged(neighbors)
                elif around == unknown:  # Changed from if to elif
                    self.flag_all(neighbors)

    def open_unflagged(self, neighbors: List[Space]) -> None:
        """ Open unflagged tiles in the given spaces.
        neighbors (list): List of neighboring spaces """
        for piece in neighbors:
            if not piece.get_flagged():
                self.board.handle_click(piece, False)

    # MAKE SURE THIS LOGIC CHANGES FLAG COUNT!
    def flag_all(self, neighbors: List[Space]) -> None:
        """ Flag all unflagged tiles in given neighbors. """
        for piece in neighbors:
            if not piece.get_flagged():
                self.board.handle_click(piece, True)
