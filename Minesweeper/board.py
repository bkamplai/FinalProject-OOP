import random
from piece import Piece

class Board:
    def __init__(self, size, mine_count):
        self.size = size
        self.board = []
        self.won = False 
        self.lost = False
        for row in range(size[0]):
            row = []
            for col in range(size[1]):
                bomb = random.random() < mine_count #going away to replace with IO
                piece = Piece(bomb)
                row.append(piece)
            self.board.append(row)
        self.set_neighbors()
        self.set_num_around()

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
    
    def add_to_neighbors_list(self, neighbors, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self.size[0] or c < 0 or c >= self.size[1]:
                    continue
                neighbors.append(self.board[r][c])
    
    def set_num_around(self):
        for row in self.board:
            for piece in row:
                piece.set_num_around()
        
        