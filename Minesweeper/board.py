from space import Space

class Board:
    def __init__(self, size, mine_count):
        """
        Initialize the game board.
        size (tuple): Size of the board (rows, columns)
        mine_count (int): Number of mines on the board
        """
        self.size = size
        self.board = []
        self.won = False 
        self.lost = False
        self.initialized = False
        self.mine_count = mine_count
        for row in range(size[0]):
            row = []
            for col in range(size[1]):
                piece = Space(False) # Initialzie with no mines
                row.append(piece)
            self.board.append(row)

    def initialize_mines(self, positions):
        """
        Initialize mines on the board.
        positions (list): List of mine positions
        """
        # Reset mine settings
        for row in self.board:
            for space in row:
                space.has_bomb = False
                space.clicked = False
                space.flagged = False
                space.around = 0
        # Set mines at given positions
        for position in positions:
            self.get_piece(position).has_bomb = True
            print(f"Has Mine = {self.get_piece(position).has_bomb}")
        # Call set up methods
        self.set_neighbors()
        self.set_num_around()
        self.initialized = True
        print("Mines placed and initialized")

    def reveal_all_non_flagged_squares(self):
        """ Reveal unrevealed and unflagged spaces on the board. """
        for row in self.board:
            for space in row:
                if not space.get_flagged() and not space.get_clicked():
                    self.handle_click(space, False)

    def get_total_mine_count(self):
        """ Get total number of mines on board. """
        return self.mine_count

    def count_flags(self):
        """ Count number of flags on the board. """
        flag_count = 0
        for row in self.board:
            for space in row:
                if space.get_flagged():
                    flag_count += 1
        return flag_count

    def print_board(self):
        """ Print the current state of the board. """
        for row in self.board:
            for piece in row:
                print(piece, end=" ")
            print()

    def get_board(self):
        """ Get the game board. """
        return self.board

    def get_size(self):
        """ Get the size of the game board. """
        return self.size
    
    def get_piece(self, index):
        """
        Get a piece at a given index.
        index (tuple): Index of the piece (space)
        Returns the Space at the given index
        """
        return self.board[index[0]][index[1]]

    def handle_click(self, piece, flag):
        """
        Handle a click on a piece (Space).
        piece (Space): The piece that was clicked
        flag (bool): Was the click a flag?
        """
        if piece.get_clicked() or (piece.get_flagged() and not flag):
            return
        if flag:
            piece.toggle_flag()
            return
        piece.handle_click()
        if piece.get_num_around() == 0:
            for neighbor in piece.get_neighbors():
                self.handle_click(neighbor, False)
        if piece.get_has_bomb():
            self.lost = True
        else:
            self.won = self.check_won()
    
    def check_won(self):
        """ Check if the game has been won. """
        for row in self.board:
            for piece in row:
                if not piece.get_has_bomb() and not piece.get_clicked():
                    return False
        return True

    def get_won(self):
        """ Has the game been won? """
        return self.won

    def get_lost(self):
        """ Has the game been lost? """
        return self.lost

    def set_neighbors(self):
        """ Set the neighbors for each piece (space) on the board. """
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.board[row][col]
                neighbors = []
                self.add_to_neighbors_list(neighbors, row, col)
                piece.set_neighbors(neighbors)
                # debugging
                #mines_around = sum(n.has_bomb for n in neighbors)
                #print(f"Space at ({row},{col}) has {len(neighbors)} neighbors with {mines_around} mines.")

    
    def add_to_neighbors_list(self, neighbors, row, col):
        """
        Add neighbord to a list for a given piece (Space).
        neighbors (list): List to store neighbors
        row (int): Row index of the piece
        col (int): Column index of the piece
        """
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self.size[0] or c < 0 or c >= self.size[1]:
                    continue
                neighbors.append(self.board[r][c])
        #print(f"Neighbors for ({row},{col}): {len(neighbors)}")

    def set_num_around(self):
        """ Set the number of mines around each piece on the board. """
        for rowIndex, row in enumerate(self.board):
            for colIndex, piece in enumerate(row):
                piece.set_num_around()

    def isBoardOpened(self):
        """ 
        Check to see if the space that was selected opened up the board.
        Returns bool - True is board is fully opnened, False otherwise """
        for row in self.board:
            for space in row:
                if space.get_clicked() and space.get_num_around() == 0:
                    return True
        return False
        