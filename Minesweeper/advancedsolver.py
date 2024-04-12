from solverstrategy import SolverStrategy
import random

class AdvancedSolver(SolverStrategy):
    def __init__(self, board):
        self.board = board
        self.safe_squares_to_probe = []
        self.mines_identified = []

    def flag_mines(self):
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
                        #if not self.board.get_piece(hidden).get_flagged():
                            #self.mines_identified.append(hidden)
                            #mines_flagged = True
        return mines_flagged

    def evaluate_border_cells(self, border_cells):
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
    
            # Subtraction rule for flagging mines
            #if num_around - flags_around == len(hidden_tiles) and len(hidden_tiles) > 0:
                #for hidden in hidden_tiles:
                    #if not self.board.get_piece(hidden).get_flagged():
                        #print(f"Flagging mine at: {hidden}")
                        #self.mines_identified.append(hidden)
                        #changes_made = True
        #return changes_made

        #print("IN evaluate_boarder_cells")
        #for x, y in border_cells:
            #cell = self.board.get_piece((x, y))
            #num_around = cell.get_num_around()
            #flags_around = self.count_flags_around(x, y)
            #hidden_tiles = self.find_hidden_tiles_around(x, y)

            #if num_around == flags_around:
                # All hidden tiles are safe
                #for hidden in hidden_tiles:
                    #print(f"Adding safe square to probe: {hidden}")
                    #self.safe_squares_to_probe.append(hidden)
            #elif num_around - flags_around == len(hidden_tiles):
                # All hidden tiles are safe
                #for hidden in hidden_tiles:
                    #print(f"Flagging mine at: {hidden}")
                    #self.mines_identified.append(hidden)


       

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
        
        #print("Solving with AdvancedSolver")
        #border_cells = self.find_border_cells()
        #if border_cells:
            #self.evaluate_border_cells(border_cells)
            #if not self.safe_squares_to_probe and not self.mines_identified:
                #print("No more cetain moves to make. The solver is either stuck or the puzzle is solved.")
            #self.act_on_findings()
        #else:
            #print("No border cells to evaluate. Solver may be stuck or the puzzle is solved.")

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

    def act_on_findings(self):
        print("In act_on_findings")
        # Reveal safe squares
        for mine_coords in self.mines_identified:
            mine_cell = self.board.get_piece(mine_coords)
            if not mine_cell.get_flagged():
                print(f"Flagging tile at {mine_coords}")
                self.board.handle_click(mine_cell, True)

        #for mine in self.mines_identified:
            #self.board.handle_click(mine, True)
            #x, y = mine
            #tile = self.board.get_piece((x, y))
            #if not tile.get_flagged():
                #print(f"Flagging tile at ({x}, {y})")
                #self.board.handle_click(tile, True) # toggle the flag status of the tile
        for square_coords in self.safe_squares_to_probe:
            safe_cell = self.board.get_piece(square_coords)
            if not safe_cell.get_clicked():
                print(f"Revealing the tile at {square_coords}")
                self.board.handle_click(safe_cell, False)
        self.safe_squares_to_probe.clear()
        self.mines_identified.clear()
        
        #for square in self.safe_squares_to_probe:
            #x, y = square
            #tile = self.board.get_piece((x, y))
            #if not tile.get_clicked():
                #print(f"Revealing tile at({x}, {y})")
                #self.board.handle_click(tile, False)

        #self.safe_squares_to_probe.clear()
        #self.mines_identified.clear()