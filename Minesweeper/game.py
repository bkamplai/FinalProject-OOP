import pygame
from board import Board 
from solver import Solver
from time import sleep
from renderer import Renderer
from initializingstate import InitializingState

class Game:
    def __init__(self, grid_size, mine_count):
        self.board = Board(grid_size, mine_count)
        piece_size = (800 // grid_size[1], 800 // grid_size[0])
        self.renderer = Renderer(grid_size=grid_size, piece_size=piece_size)
        self.solver = Solver(self.board)
        self.mine_positions = [] # Store positions of mines from user input
        self.expected_mine_count = mine_count # expected num of mines to place
        self.show_message = True
        self.state = InitializingState(self)

    def change_state(self, new_state):
        self.state.exit()
        self.state = new_state
        self.state.enter()

    def update_mine_placement_message(self):
        mines_left = self.expected_mine_count - len(self.mine_positions)
        message = f"Place your mines. Mines left: {mines_left}"
        self.renderer.display_message(message, (self.renderer.screen_size[0] // 2, 50))

    def run(self):
        running = True
        while running:
            self.renderer.clear_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.state.handle_click(pygame.mouse.get_pos())
                    #if not self.board.initialized:
                        # User is still placing mines
                        #position = self.convert_pixel_to_grid(pygame.mouse.get_pos())
                        #if position not in self.mine_positions: # prevent duplicate mines
                            #self.mine_positions.append(position)
                            #if len(self.mine_positions) < self.expected_mine_count:
                                # Update message with new remaining mine value
                                #mines_left = self.expected_mine_count - len(self.mine_positions)
                                #self.renderer.display_message(f"Place your mines. Mines left: {mines_left}", (100, 100))
                                #pass
                            #else:
                                # All mines placed, initialize the board and start the game
                                #self.board.initialize_mines(self.mine_positions)
                                #self.board.initialized = True
                                #self.renderer.display_message("All mines placed. Starting game...", (100, 100))
                                #pygame.time.wait(2000) # Wait 2 sec before starting
                            #self.show_message = False
                    #elif not (self.board.get_won() or self.board.get_lost()):
                        #rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                        #self.handleClick(pygame.mouse.get_pos(), rightClick)
                #if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.get_won() or self.board.get_lost()):
                    #rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    #self.handleClick(pygame.mouse.get_pos(), rightClick)
                
                elif event.type == pygame.KEYDOWN:
                    if self.board.initialized and not self.board.get_lost():
                        self.solver.move()
            
            if self.board.initialized:
                self.renderer.draw_board(self.board)

            if self.show_message:
                mines_left = self.expected_mine_count - len(self.mine_positions)
                message = "Place your mines. Click to place" if mines_left > 0 else "All mines placed. Starting game..."
                self.renderer.display_message(message, (self.renderer.screen_size[0] // 2, 50))
            
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

    def convert_pixel_to_grid(self, pixel_position):
        grid_x = pixel_position[0] // self.renderer.piece_size[0]
        grid_y = pixel_position[1] // self.renderer.piece_size[1]
        return grid_y, grid_x # return as (row, col)

    def handleClick(self, position, flag):
        index = tuple(int(pos // size) for pos, size in zip(position, self.renderer.piece_size))[::-1] 
        self.board.handle_click(self.board.get_piece(index), flag)

    def initialize_board(self):
        self.board.initialize_mines(self.mine_positions)
        self.board.initialized = True

    def win(self):
        sound = pygame.mixer.Sound('win.wav')
        sound.play()
        sleep(3)