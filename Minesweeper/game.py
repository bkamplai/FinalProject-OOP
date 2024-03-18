import pygame
from board import Board 
from solver import Solver
from time import sleep
from renderer import Renderer

class Game:
    def __init__(self, size, mine_count):
        self.board = Board(size, mine_count)
        piece_size = (800 // size[1], 800 // size[0])
        self.renderer = Renderer(screen_size=(800,800), piece_size=piece_size)
        self.solver = Solver(self.board)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.get_won() or self.board.get_lost()):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.handleClick(pygame.mouse.get_pos(), rightClick)
                if event.type == pygame.KEYDOWN:
                    self.solver.move()

            self.renderer.draw_board(self.board)
            self.renderer.update_display()

            if self.board.get_won():
                self.win()
                running = False
        pygame.quit()

    """def getImageString(self, piece):
        if piece.get_clicked():
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'
        if (self.board.get_lost()):
            if (piece.getHasBomb()):
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.getFlagged() else 'empty-block'
        return 'flag' if piece.getFlagged() else 'empty-block'"""

    def handleClick(self, position, flag):
        index = tuple(int(pos // size) for pos, size in zip(position, self.renderer.piece_size))[::-1] 
        self.board.handle_click(self.board.get_piece(index), flag)

    def win(self):
        sound = pygame.mixer.Sound('win.wav')
        sound.play()
        sleep(3)