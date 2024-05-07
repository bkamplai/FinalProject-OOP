from typing import List, Tuple
from solverstrategy import SolverStrategy
from board import Board
from space import Space


class AdvancedSolver(SolverStrategy):
    def __init__(self, board: Board) -> None:
        """ Initialize the Advanced Solver. """
        self.board: Board = board
        self.safe_squares_to_probe: List[Tuple[int, int]] = []
        self.mines_identified: List[Tuple[int, int]] = []
        self.flags_placed: int = 0

    def flag_mines(self) -> bool:
        """
        Determine if you can flag any spaces based on neighboring spaces.
        Returns bool - True if mines were flagged, False otherwise
        """
        mines_flagged: bool = False
        flag_count: int = self.board.count_flags()
        max_flags: int = self.board.get_total_mine_count()

        for x in range(self.board.get_size()[0]):
            for y in range(self.board.get_size()[1]):
                cell: Space = self.board.get_piece((x, y))
                # skip already revealed cells
                if not cell.get_clicked() or cell.get_flagged():
                    continue
                num_around: int = cell.get_num_around()
                flags_around: int = self.count_flags_around(x, y)
                hidden_tiles: List[Tuple[int, int]] = \
                    self.find_hidden_tiles_around(x, y)

                # Flagging condition
                if num_around - flags_around == len(hidden_tiles) \
                        and flag_count < max_flags:
                    for hidden in hidden_tiles:
                        hidden_cell = self.board.get_piece(hidden)
                        if not hidden_cell.get_flagged() and \
                                flag_count < max_flags:
                            print(f"Flagging mine at: {hidden}")
                            self.board.handle_click(hidden_cell, True)
                            mines_flagged = True
                            self.flags_placed += 1
                            flag_count += 1
                            if flag_count >= max_flags:
                                return mines_flagged
                            # if self.board.get_lost():
                            #     print("MINE WAS REVEALED. GAME OVER.")
                            #     return mines_flagged
        return mines_flagged

    def evaluate_border_cells(self, border_cells: List[Tuple[int, int]]
                              ) -> bool:
        """
        Try to identify safe squares to probe.
        border_cells (list): List of border cells to evaluate
        Returns bool - True if changes were made, False otherwise
        """
        changes_made: bool = False
        print("Evaluating border cells: ", border_cells)
        for x, y in border_cells:
            cell: Space = self.board.get_piece((x, y))
            num_around: int = cell.get_num_around()
            flags_around: int = self.count_flags_around(x, y)
            hidden_tiles: List[Tuple[int, int]] = \
                self.find_hidden_tiles_around(x, y)

            print(f"Cell ({x}, {y}): num_around = {num_around}, flags_around ="
                  + f" {flags_around}, hidden_tiles = {hidden_tiles}")

            # Identify safe neighbors
            if flags_around == num_around and len(hidden_tiles) > 0:
                for hidden in hidden_tiles:
                    if not self.board.get_piece(hidden).get_clicked():
                        print(f"Adding safe square to probe: {hidden}")
                        self.safe_squares_to_probe.append(hidden)
                        changes_made = True
                        # if self.board.get_lost():
                        #     print("MINE WAS REVEALED. GAME OVER IN BORDER "
                        #           + "CELL.")
                        #     return True

        return changes_made or self.flag_mines()

    def count_flags_around(self, x: int, y: int) -> int:
        """
        Count the number of flags around a given space.
        Returns int - number of flags around the space
        """
        # print("In count_flags_around")
        count: int = 0
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

    def find_hidden_tiles_around(self, x: int, y: int
                                 ) -> List[Tuple[int, int]]:
        """ Get a list of hidden tiles around the space """
        # print("In find_hidden_tiles_around")
        hidden_tiles: List[Tuple[int, int]] = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.is_valid_coord(nx, ny):
                    neighbor = self.board.get_piece((nx, ny))
                    if not neighbor.get_clicked() \
                            and not neighbor.get_flagged():
                        hidden_tiles.append((nx, ny))
        return hidden_tiles

    def is_valid_coord(self, x: int, y: int) -> bool:
        """ Check if a given coordinate is valid."""
        # print("in is_valid_coord")
        return 0 <= x < self.board.get_size()[0] and 0 <= y <\
            self.board.get_size()[1]

    def solve(self) -> None:
        """ Solve the board using Advanced Solver strategy. """
        print("Solving with AdvancedSolver")
        while True:
            if self.board.get_lost():
                print("GAME OVER ADVANCED SOLVER")
                return
            border_cells: List[Tuple[int, int]] = self.find_border_cells()
            if not border_cells:
                print("No border cells to evaluate. Solver may be stuck or the"
                      + " puzzle is solved.")
                break
            if not self.evaluate_border_cells(border_cells):
                # No more mines were flagged, we're stuck
                if not self.flag_mines():
                    print("No more certain moves to make. The solver is either"
                          + " stuck or the puzzle is solved.")
                    break
                else:
                    # Mines were flagged, re-evaluate the border cells
                    continue

            self.act_on_findings()

    def get_flags_placed(self) -> int:
        """ Get the number of flags placed by the solver (display)"""
        return self.flags_placed

    def find_border_cells(self) -> List[Tuple[int, int]]:
        """ Find border cells on board (immediate neighbors) """
        border_cells: List[Tuple[int, int]] = []
        for x in range(self.board.get_size()[0]):
            for y in range(self.board.get_size()[1]):
                if self.is_border_cell(x, y):
                    border_cells.append((x, y))
        return border_cells

    def is_border_cell(self, x: int, y: int) -> bool:
        """ Check to see if a given space is a border space. """
        cell: Space = self.board.get_piece((x, y))
        if cell.get_clicked():
            return False
        # check adjacent cells for at least one revealed cell
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board.get_size()[0] \
                        and 0 <= ny < self.board.get_size()[1]:
                    neighbor: Space = self.board.get_piece((nx, ny))
                    if neighbor.get_clicked():
                        return True
        return False

    def act_on_findings(self) -> None:
        """ Reveal spaces or place flags after evaluating border cells. """
        print("In act_on_findings")
        # Reveal safe squares
        for mine_coords in self.mines_identified:
            mine_cell: Space = self.board.get_piece(mine_coords)
            if not mine_cell.get_flagged():
                print(f"Flagging tile at {mine_coords}")
                # FLAGGING FROM HERE TOO = PROBLEM!!
                self.board.handle_click(mine_cell, True)
                self.flags_placed += 1

        for square_coords in self.safe_squares_to_probe:
            safe_cell: Space = self.board.get_piece(square_coords)
            if not safe_cell.get_clicked():
                print(f"Revealing the tile at {square_coords}")
                self.board.handle_click(safe_cell, False)
        self.safe_squares_to_probe.clear()
        self.mines_identified.clear()
