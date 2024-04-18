import pygame
from board import Board 
from solver import Solver
from time import sleep
from renderer import Renderer
from initializingstate import InitializingState
from playingstate import PlayingState
#from trivialsolver import TrivialSolver
from gameoverstate import GameOverState
#from advancedsolver import AdvancedSolver
from SolverInterface import SolverInterface

class Game:
    def __init__(self, grid_size, mine_count):
        self.board = Board(grid_size, mine_count)
        piece_size = (800 // grid_size[1], 800 // grid_size[0])
        self.renderer = Renderer(grid_size=grid_size, piece_size=piece_size)
        self.mine_positions = [] # Store positions of mines from user input
        self.expected_mine_count = mine_count # expected num of mines to place
        self.show_message = True
        self.state = InitializingState(self)
        self.initial_draw()
        self.solver_interface = SolverInterface(self.board)

    def run_solver(self):
        #print("In run solver")
        if isinstance(self.state, PlayingState):
            #self.currentSolver.solve()
            self.solver_interface.set_solver('trivial')
            self.solver_interface.solve()

            current_flag_count = self.board.count_flags()
            if current_flag_count == self.expected_mine_count:
                # If the numbers match, attempt to reveal all non-flagged squares
                self.board.reveal_all_non_flagged_squares()
                if self.board.check_won():
                    self.change_state(GameOverState(self, win=True))
                return

            if self.shouldSwitchSolver():
                self.solver_interface.set_solver('advanced')
                self.solver_interface.solve()
                self.solver_triggered = False
            pygame.time.wait(3000)
            #if self.shouldSwitchToAdvancedSolver() and not isinstance(self.currentSolver, AdvancedSolver):
                #self.switchToAdvancedSolver() #GET RID OF (GO GET A SOLVER FROM THE SOLVERSTRATEGY)
                #self.solver_triggered = False # Reset trigger to allow advanced solver to run
            #pygame.time.wait(3000)
        else:
            pass
            
    def shouldSwitchSolver(self):
        # Call function in board to see if conditition for advancedSolver is met
        return self.board.isBoardOpened()

    def initial_draw(self):
        # draw the initial state of the game
        self.state.update()
        self.renderer.update_display()

    def change_state(self, new_state):
        print(f"Changing state from {type(self.state).__name__} to {type(new_state).__name__}")
        self.state.exit()
        self.state = new_state
        self.state.enter()

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

            self.run_solver()
            #flags_placed = self.solver_interface.get_flags_placed()
            self.state.update()
            #self.renderer.draw_board(self.board, flags_placed=flags_placed)
            self.renderer.update_display()

            if self.board.get_lost():
                self.change_state(GameOverState(self))
                running = False
            elif self.board.get_won():
                self.win()
                running = False

        pygame.quit()

    def convert_pixel_to_grid(self, pixel_position):
        header_height = 50
        grid_x = pixel_position[0] // self.renderer.piece_size[0]
        grid_y = (pixel_position[1] - header_height) // self.renderer.piece_size[1]
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