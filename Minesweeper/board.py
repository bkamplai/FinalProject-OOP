import random
from space import Space

class Board:
    def __init__(self, size, mine_count):
        self.size = size
        self.board = []
        self.won = False 
        self.lost = False
        self.initialized = False
        self.mine_count = mine_count
        for row in range(size[0]):
            row = []
            for col in range(size[1]):
                #bomb = random.random() < mine_count #going away to replace with IO
                #piece = Space(bomb)
                piece = Space(False) # Initialzie with no mines
                row.append(piece)
            self.board.append(row)
        #self.set_neighbors() # Don't call this until user places mines
        #self.set_num_around() # Don't call this until user places mines

    def initialize_mines(self, positions):
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
        for row in self.board:
            for space in row:
                if not space.get_flagged() and not space.get_clicked():
                    self.handle_click(space, False)

    def get_total_mine_count(self):
        return self.mine_count

    def count_flags(self):
        flag_count = 0
        for row in self.board:
            for space in row:
                if space.get_flagged():
                    flag_count += 1
        return flag_count

    def print_board(self):
        for row in self.board:
            for piece in row:
                print(piece, end=" ")
            print()

    def get_board(self):
        return self.board

    def get_size(self):
        return self.size
    
    def get_piece(self, index):
        return self.board[index[0]][index[1]]

    def handle_click(self, piece, flag):
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
        for row in self.board:
            for piece in row:
                if not piece.get_has_bomb() and not piece.get_clicked():
                    return False
        return True

    def get_won(self):
        return self.won

    def get_lost(self):
        return self.lost

    def set_neighbors(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.board[row][col]
                neighbors = []
                self.add_to_neighbors_list(neighbors, row, col)
                piece.set_neighbors(neighbors)
                # debugging
                mines_around = sum(n.has_bomb for n in neighbors)
                #print(f"Space at ({row},{col}) has {len(neighbors)} neighbors with {mines_around} mines.")

    
    def add_to_neighbors_list(self, neighbors, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self.size[0] or c < 0 or c >= self.size[1]:
                    continue
                neighbors.append(self.board[r][c])
        #print(f"Neighbors for ({row},{col}): {len(neighbors)}")

    def set_num_around(self):
        for rowIndex, row in enumerate(self.board):
            for colIndex, piece in enumerate(row):
                piece.set_num_around()
                # debugging
                #if rowIndex == 0 and colIndex == 0:  # Example for the first cell
                    #for neighbor in piece.neighbors:
                        #print(f"Neighbor mine status: {neighbor.has_bomb}")
                #print(f"Space at position ({rowIndex}, {colIndex}) has {piece.get_num_around()} mines around")
                #print(f"Space at position ({rowIndex}, {colIndex}) has {piece.get_num_around()} mines around")

    def someConditionMetForSwitch(self):
        for row in self.board:
            for space in row:
                if space.get_clicked() and space.get_num_around() == 0:
                    return True
        return False
        