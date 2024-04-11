from solverstrategy import SolverStrategy
import random

class AdvancedSolver(SolverStrategy):
    def __init__(self, board):
        self.board = board
        self.safe_squares_to_probe = []
        self.mines_identified = []

    def evaluate_border_cells(self, border_cells):
        print("IN evaluate_border_cells")
        for x, y in border_cells:
            cell = self.board.get_piece((x, y))
            num_around = cell.get_num_around()
            flags_around = self.count_flags_around(x, y)
            hidden_tiles = self.find_hidden_tiles_around(x, y)

            # Apply heuristic rules
            if num_around == flags_around + len(hidden_tiles):
                # All hidden tiles must be mines
                for hidden in hidden_tiles:
                    print(f"Flagging mine at: {hidden}")
                    self.mines_identified.append(hidden)
            elif flags_around == num_around:
                # All hidden tiles are safe
                for hidden in hidden_tiles:
                    print(f"Adding safe square to probe: {hidden}")
                    self.safe_squares_to_probe.append(hidden)

    def count_flags_around(self, x, y):
        print("In count_flags_around")
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.is_valid_coord(nx, ny):
                    neighbor = self.board.get_piece((nx, ny))
                    if neighbor.get_flagged():
                        count += 1
        return count
    
    def find_hidden_tiles_around(self, x, y):
        print("In find_hidden_tiles_around")
        hidden_tiles = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.is_valid_coord(nx, ny):
                    neighbor = self.board.get_piece((nx, ny))
                    if not neighbor.get_clicked() and not neighbor.get_flagged():
                        hidden_tiles.append((nx, ny))
        return hidden_tiles

    def is_valid_coord(self, x, y):
        print("in is_valid_coord")
        return 0 <= x < self.board.get_size()[0] and 0 <= y < self.board.get_size()[1]

    def solve(self):
        print("Solving with AdvancedSolver")
        border_cells = self.find_border_cells()
        if border_cells:
            self.evaluate_border_cells(border_cells)
            self.act_on_findings()

    #def solve(self):
        #self.safe_squares_to_probe.clear()
        #self.mines_identified.clear()

        #border_cells = self.find_border_cells()
        #if not border_cells:
            # If no border cells are found, pick a random unrevealed cell
            #self.pick_random_unrevealed_cell()
        #else:
            #self.evaluate_border_cells(border_cells)
            #self.act_on_findings()
    
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
    
    #def evaluate_border_cells(self, border_cells):
        # logic that evaluates each border cell and updates
        #pass

    def act_on_findings(self):
        print("In act_on_findings")
        # Reveal safe squares
        for mine in self.mines_identified:
            x, y = mine
            tile = self.board.get_piece((x, y))
            if not tile.get_flagged():
                print(f"Flagging tile at ({x}, {y})")
                self.board.handle_click(tile, True) # toggle the flag status of the tile
        for square in self.safe_squares_to_probe:
            x, y = square
            tile = self.board.get_piece((x, y))
            if not tile.get_clicked():
                print(f"Revealing tile at({x}, {y})")
                self.board.handle_click(tile, False)

        self.safe_squares_to_probe.clear()
        self.mines_identified.clear()


    #def pick_random_unrevealed_cell(self):
        #unrevealed = [(x, y) for x in range(self.board.get_size()[0])
                      #for y in range(self.board.get_size()[1])
                      #if not self.board.get_piece((x, y)).get_clicked() and not self.board.get_piece((x, y)).get_flagged()]
        #if unrevealed:
            #choice = random.choice(unrevealed)
            #self.board.handle_click(choice, False)
