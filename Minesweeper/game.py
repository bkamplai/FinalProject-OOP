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
        """
        Initialize the game.
        grid_size (tuple): Size of the game grid (rows, columns)
        mine_count (int): Number of mines in the game
        """
        self.board = Board(grid_size, mine_count)
        piece_size = (800 // grid_size[1], 800 // grid_size[0])
        self.renderer = Renderer(grid_size=grid_size, piece_size=piece_size)
        self.mine_positions = [] # Store positions of mines from user input
        self.expected_mine_count = mine_count # expected num of mines to place
        self.show_message = True
        self.state = InitializingState(self)
        self.initial_draw()
        self.solver_interface = SolverInterface(self.board)
        self.solver_interface.set_solver('trivial')


    def run_solver(self):
        """
        Run the solver to automatically play the game.
        """
        if isinstance(self.state, PlayingState):
            #self.solver_interface.set_solver('trivial')
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
                print("Switched to Advanced Solver")
                self.solver_interface.solve()
                self.solver_triggered = False
            pygame.time.wait(3000)
        else:
            pass
            
    def shouldSwitchSolver(self):
        """
        Do we need a new strategy?
        Call the function in board to see if condition for advancedSolver is met
        """
        return self.board.isBoardOpened()

    def initial_draw(self):
        """
        Draw the initial state of the game.
        """
        self.state.update()
        self.renderer.update_display()

    def change_state(self, new_state):
        """
        Change the current state of the game.
        new_state (State): New state of the game
        """
        print(f"Changing state from {type(self.state).__name__} to {type(new_state).__name__}")
        self.state.exit()
        self.state = new_state
        self.state.enter()

    def run(self):
        """ 
        Run the game loop.
        """
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
            #print("ABOUT TO CALL RUN_SOLVER()")
            self.run_solver()
            #flags_placed = self.solver_interface.get_flags_placed()
            self.state.update()
            #self.renderer.draw_board(self.board, flags_placed=flags_placed)
            self.renderer.update_display()

            if self.board.get_lost():
                self.change_state(GameOverState(self))
                print(f"GAME LOST: {self.board.get_lost()}")
                running = False
            elif self.board.get_won():
                print(f"GAME WON: {self.board.get_won()}")
                self.win()
                running = False

            #pygame.time.wait(5000) # Causes a pause on everything until game is over

        pygame.quit()

    def convert_pixel_to_grid(self, pixel_position):
        """ 
        Convert pixel position to grid position.
        pixel_position (tuple): pixel position (x, y)
        Returns tuple - grid position (row, column)
        """
        header_height = 50
        grid_x = pixel_position[0] // self.renderer.piece_size[0]
        grid_y = (pixel_position[1] - header_height) // self.renderer.piece_size[1]
        return grid_y, grid_x # return as (row, col)

    def handleClick(self, position, flag):
        """
        Handle mouse click.
        position (tuple): Position of the click
        flag (bool): Is the click a flag?
        """
        index = tuple(int(pos // size) for pos, size in zip(position, self.renderer.piece_size))[::-1] 
        self.board.handle_click(self.board.get_piece(index), flag)

    def initialize_board(self):
        """
        Initialize the game board.
        """
        self.board.initialize_mines(self.mine_positions)
        self.board.initialized = True

    def win(self):
        """ 
        Handle the win condition.
        """
        sound = pygame.mixer.Sound('win.wav')
        sound.play()
        sleep(3)