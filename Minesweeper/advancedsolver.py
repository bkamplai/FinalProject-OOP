from solverstrategy import SolverStrategy
import pygame

class AdvancedSolver(SolverStrategy):
    def __init__(self, board):
        """
        Initialize the AdvancedSolver.
        board (Board): The game board
        """
        self.board = board
        self.safe_squares_to_probe = [] # List of safe squares to investigate
        self.mines_identified = [] # List of identified mines
        self.flags_placed = 0 # Counter for flags placed (display)

    def flag_mines(self):
        """
        Flag mines based on evaluation of neighboring spaces.
        Returns bool - True is mines were flagged, False otherwise
        """
        mines_flagged = False
        for x in range(self.board.get_size()[0]):
            for y in range(self.board.get_size()[1]):
                cell = self.board.get_piece((x, y))
                if not cell.get_clicked(): # skip already revealed cells
                    continue
                num_around = cell.get_num_around()
                flags_around = self.count_flags_around(x, y)
                hidden_tiles = self.find_hidden_tiles_around(x, y)

                # Flagging condition
                if num_around - flags_around == len(hidden_tiles):
                    for hidden in hidden_tiles:
                        hidden_cell = self.board.get_piece(hidden)
                        if not hidden_cell.get_flagged():
                            print(f"Flagging mine at: {hidden}")
                            self.board.handle_click(hidden_cell, True)
                            mines_flagged = True
                            self.flags_placed += 1
        return mines_flagged

    def evaluate_border_cells(self, border_cells):
        """
        Evaluate the border cells to identify safe squares to probe
        border_cells (list): List of border cells to evaluate
        Returns bool - True is changes were made, False otherwise
        """
        changes_made = False
        print("Evaluating border cells: ", border_cells)
        for x, y in border_cells:
            cell = self.board.get_piece((x, y))
            num_around = cell.get_num_around()
            flags_around = self.count_flags_around(x, y)
            hidden_tiles = self.find_hidden_tiles_around(x, y)

            print(f"Cell ({x}, {y}): num_around = {num_around}, flags_around = {flags_around}, hidden_tiles = {hidden_tiles}")

            # Identify safe neighbors
            if flags_around == num_around and len(hidden_tiles) > 0:
                for hidden in hidden_tiles:
                    if not self.board.get_piece(hidden).get_clicked():
                        print(f"Adding safe square to probe: {hidden}")
                        self.safe_squares_to_probe.append(hidden)
                        changes_made = True
        
        return changes_made or self.flag_mines()

    def count_flags_around(self, x, y):
        """
        Count the number of flags around a given cell.
        x (int): x-coordinate of the cell
        y (int): y-coordinate of the cell
        Returns int - Number of flags around the space
        """
        #print("In count_flags_around")
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
        """
        Find hidden tiles around a given space.
        x (int): x-coordinate of the space
        y (int): y-coordinate of the space
        Returns list - List of hidden tiles around the space
        """
        #print("In find_hidden_tiles_around")
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
        """
        Check if a given coordinate is valid.
        x (int): x-coordinate
        y (int): y-coordiante
        Returns bool - True if coordinate is valid, False otherwise
        """
        return 0 <= x < self.board.get_size()[0] and 0 <= y < self.board.get_size()[1]

    def solve(self):
        """
        Solve the game using the advanced solver strategy.
        """
        print("Solving with AdvancedSolver")
        while True:
            border_cells = self.find_border_cells()
            if not border_cells:
                print("No border cells to evaluate. Solver may be stuck or the puzzle is solved.")
                break
            if not self.evaluate_border_cells(border_cells):
                if not self.flag_mines(): # No more mines were flagged, we're stuck
                    print("No more certain moves to make. The solver is either stuck or the puzzle is solved.")
                    break
                else:
                    # Mines were flagged, re-evaluate the border cells
                    continue
            
            self.act_on_findings()
    
    def get_flags_placed(self):
        """
        Get the number of flags placed by the solver (display).
        Returns int - Number of flags placed
        """
        return self.flags_placed

    def find_border_cells(self):
        """
        Find border cells on the game board.
        Returns list - List of border cells (immediate neighbors)
        """
        border_cells = []
        for x in range(self.board.get_size()[0]):
            for y in range(self.board.get_size()[1]):
                if self.is_border_cell(x, y):
                    border_cells.append((x, y))
        return border_cells
    
    def is_border_cell(self, x, y):
        """
        Check if a given cell is a border cell.
        x (int): x-coordinate of the cell
        y (int): y-coordinate of the cell
        Returns bool - True if the cell is a border cell, False otherwise
        """
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

    def act_on_findings(self):
        """
        Flag or reveal mines based on the findings of the solver.
        """
        print("In act_on_findings")
        # Reveal safe squares
        for mine_coords in self.mines_identified:
            mine_cell = self.board.get_piece(mine_coords)
            if not mine_cell.get_flagged():
                print(f"Flagging tile at {mine_coords}")
                self.board.handle_click(mine_cell, True)
                self.flags_placed += 1

        for square_coords in self.safe_squares_to_probe:
            safe_cell = self.board.get_piece(square_coords)
            if not safe_cell.get_clicked():
                print(f"Revealing the tile at {square_coords}")
                #pygame.time.wait(5000)
                self.board.handle_click(safe_cell, False)
        self.safe_squares_to_probe.clear()
        self.mines_identified.clear()