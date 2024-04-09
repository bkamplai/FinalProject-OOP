from solverstrategy import SolverStrategy
import random

class AdvancedSolver(SolverStrategy):
    def __init__(self, board):
        self.board = board
        self.safe_squares_to_probe = []
        self.mines_identified = []

    def solve(self):
        self.safe_squares_to_probe.clear()
        self.mines_identified.clear()

        border_cells = self.find_border_cells()
        if not border_cells:
            # If no border cells are found, pick a random unrevealed cell
            self.pick_random_unrevealed_cell()
        else:
            self.evaluate_border_cells(border_cells)
            self.act_on_findings()
    
    def find_border_cells(self):
        border_cells = []
        for x in range(self.board.get_size()[0]):
            for y in range(self.board.get_size()[1]):
                if self.is_border_cell(x, y):
                    border_cells.append((x, y))
        return border_cells
    
    def is_border_cell(self, x, y):
        cell = self.board.get_piece((x, y))
        if cell.get_clicked():
            return False
        # check adjacent cells for at least one revealed cell
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board.get_size()[0] and 0 <= ny < self.board.get_size()[1]:
                    neighbor = self.board.get_piece((nx, ny))
                    if neighbor.get_clicked():
                        return True
        return False
    
    def evaluate_border_cells(self, border_cells):
        # logic that evaluates each border cell and updates
        pass

    def act_on_findings(self):
        # Reveal safe squares
        for square in self.safe_squares_to_probe:
            x, y = square
            self.board.handle_click(self.board.get_piece((x, y)), False)
    
        # Flag identified mines
        for mine in self.mines_identified:
            x, y = mine
            self.board.handle_click(self.board.get_piece((x, y)), True)
    
    def pick_random_unrevealed_cell(self):
        unrevealed = [(x, y) for x in range(self.board.get_size()[0])
                      for y in range(self.board.get_size()[1])
                      if not self.board.get_piece((x, y)).get_clicked() and not self.board.get_piece((x, y)).get_flagged()]
        if unrevealed:
            choice = random.choice(unrevealed)
            self.board.handle_click(choice, False)
