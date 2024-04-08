import pygame
from board import Board 
from solver import Solver
from time import sleep
from renderer import Renderer
from initializingstate import InitializingState
from playingstate import PlayingState
from trivialsolver import TrivialSolver
from gameoverstate import GameOverState

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
        self.initial_draw()
        self.solver = TrivialSolver(self.board)

    def run_solver(self):
        print("In run solver")
        if isinstance(self.state, PlayingState):
            self.solver.solve()
            pygame.time.wait(3000)
        else:
            print("Solver called in non-playing state. Ignored.")
        #self.solver.solve()

    def initial_draw(self):
        # draw the initial state of the game
        self.state.update()
        self.renderer.update_display()

    def change_state(self, new_state):
        print(f"Changing state from {type(self.state).__name__} to {type(new_state).__name__}")
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
                elif event.type == pygame.KEYDOWN:
                    if self.board.initialized and not self.board.get_lost():
                        self.solver.move()

            if self.show_message:
                mines_left = self.expected_mine_count - len(self.mine_positions)
                message = "Place your mines. Click to place" if mines_left > 0 else "All mines placed. Starting game..."
                self.renderer.display_message(message, (self.renderer.screen_size[0] // 2, 50))
            
            self.run_solver()
            #self.renderer.update_display()
            self.state.update()
            self.renderer.update_display()

            #if self.board.get_won():
                #self.win()
                #running = False
            if self.board.get_lost():
                self.change_state(GameOverState(self))
                running = False
            elif self.board.get_won():
                #self.change_state(WinState(self))
                self.win()
                running = False

        pygame.quit()

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