import pygame  # type: ignore
from typing import Tuple, Any
from state import State
from SolverInterface import SolverInterface


class PlayingState(State):
    def __init__(self, game: Any) -> None:
        """
        Initialize Playing State.
        game (Game): The game instance """
        super().__init__(game)
        self.solver_interface: SolverInterface = self.game.solver_interface

    def handle_click(self, position: Tuple[int, int]) -> None:
        """ Tell the game to handle the click at given position. """
        rightClick: bool = pygame.mouse.get_pressed(num_buttons=3)[2]
        self.game.handleClick(position, rightClick)

    def update(self) -> None:
        """ Update the Playing State. """
        print("CALLING RUN_SOLVER()")
        self.game.run_solver()  # Tell the game to run the solver
        # Get num of flags placed by solver
        flags_placed: int = self.solver_interface.get_flags_placed()
        print(f"FLAGS PLACED = {flags_placed}")
        # Draw game board & update header
        self.game.renderer.draw_board(self.game.board,
                                      flags_placed=flags_placed)
        # Check if game is over
        if self.game.board.get_won() or self.game.board.get_lost():
            print("Game is over")

    def enter(self) -> None:
        """ Enter the Playing State."""
        print("Entering PlayingState")
        # Finalize board setup or other tasks to start playing
        if not self.game.board.initialized:
            self.game.initialize_board()

    def exit(self) -> None:
        """ Exit the Playing State. """
        print("Exiting PlayingState")
        # Cleanup before leaving the playing state
        pass
