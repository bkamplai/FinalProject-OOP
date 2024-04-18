from solverstrategy import SolverStrategy
import random

class TrivialSolver(SolverStrategy):
    def __init__(self, board):
        """
        Initialize the Trivial Solver.
        board (Board): The game board
        """
        self.board = board
        self.flags_placed = 0

    def get_flags_placed(self):
        """ Return the number of flags placed by the solver (display)"""
        return self.flags_placed
    

    def select_random_tile(self):
        """
        Select a random unrevealed tile from the board.
        Returns tuple or None - Coordinates of the selected tile, or None if no unrevealed tiles
        """
        #print("SELECT RANDOM TILE")
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

    def find_potentially_safe_tile(self, revealed_x, revealed_y):
        """
        Find a potentiall safe tile in the safe neighbors (+1/-1).
        revealed_x (int): x-coordinate of revealed tile
        revealed_y (int): y-coordinate of revealed tile
        Returns tuple or None - Coordinates of potentially safe tile or None if no unrevealed tile
        """
        size_x, size_y = self.board.get_size()
        potentially_safe_tiles = []

        # Define search area considering edge cases
        search_offsets = range(-2, 3) # -2 -> 2 to cover secondary layer

        for dx in search_offsets:
            for dy in search_offsets:
                new_x, new_y = revealed_x + dx, revealed_y + dy

                #skip center equare and out-of-bounds spaces
                if (dx == 0 and dy == 0) or not (0 <= new_x < size_x and 0 <=new_y < size_y):
                    continue

                #check if the space is directly adjacent
                if abs(dx) <= 1 and abs(dy) <= 1:
                    continue

                #now focusing on secondary layer
                tile = self.board.get_piece((new_x, new_y))
                if not tile.get_clicked() and not tile.get_flagged():
                    potentially_safe_tiles.append((new_x, new_y))

                # Prioritize selection
                if potentially_safe_tiles:
                    # could add additional logic -> just return first one for now
                    return potentially_safe_tiles[0]
                
                return None # no safe tile found

    def solve(self):
        """ Solve the game using the trivial solver strategy. """
        print("In TrivialSolver solve()")
        tile = self.select_random_tile()
        while tile:
            print(f"Attempting to reveal tile at {tile}")
            piece = self.board.get_piece(tile)
            self.board.handle_click(piece, False)

            if piece.get_num_around() == 0:
                print("Revealed an empty space, board should auto-reveal tiles")
                break

            # If the tile is a number:
            safe_tile = self.find_potentially_safe_tile(*tile)
            if safe_tile:
                print(f"Found potentially safe tile at {safe_tile}, attempting to reveal")
                tile = safe_tile
            else:
                print("No additional safe move was found, stopping solver.")
                break