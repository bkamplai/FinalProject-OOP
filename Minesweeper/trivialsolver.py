from solverstrategy import SolverStrategy
import random

class TrivialSolver(SolverStrategy):
    def __init__(self, board):
        self.board = board

    def select_random_tile(self):
        print("SELECT RANDOM TILE")
        unrevealed_tiles = []

        for x in range(self.board.get_size()[0]):
            for y in range(self.board.get_size()[1]):
                if not self.board.get_piece((x, y)).get_clicked() and not self.board.get_piece((x, y)).get_flagged():
                    unrevealed_tiles.append((x, y))

        if unrevealed_tiles:
            print(f"UNREVEALED TILES: {len(unrevealed_tiles)}")  # Debugging
            selected_tile = random.choice(unrevealed_tiles)
            print(f"SELECTED TILE: {selected_tile}")  # Debugging
            return selected_tile
        else:
            print("No unrevealed tiles found.")
        return None

    def solve(self):
        print("In TrivialSolver solve()")
        tile = self.select_random_tile()
        if tile:
            print(f"Attempting to reveal tile at {tile}")  # Debugging
            # Simulate clicking on the tile
            self.board.handle_click(self.board.get_piece(tile), False)
            #pass