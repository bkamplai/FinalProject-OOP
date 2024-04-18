import pygame
from state import State

class PlayingState(State):
    def __init__(self, game):
        """
        Initialize Playing State.
        game (Game): The game instance """
        super().__init__(game)
        self.solver_interface = self.game.solver_interface

    def handle_click(self, position):
        """ Tell the game to handle the click at given position. """
        rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
        self.game.handleClick(position, rightClick)
    
    def update(self):
        """ Update the Playing State. """
        self.game.run_solver() # Tell the game to run the solver
        flags_placed = self.solver_interface.get_flags_placed() # Get num of flags placed by solver
        print(f"FLAGS PLACED = {flags_placed}")
        self.game.renderer.draw_board(self.game.board, flags_placed=flags_placed) # Draw game board & update header
        if self.game.board.get_won() or self.game.board.get_lost(): # Check if game is over
            print("Game is over")
    
    def enter(self):
        """ Enter the Playing State."""
        print("Entering PlayingState")
        # Finalize board setup or other tasks to start playing
        if not self.game.board.initialized:
            self.game.initialize_board()

    def exit(self):
        """ Exit the Playing State. """
        print("Exiting PlayingState")
        # Cleanup before leaving the playing state
        pass
