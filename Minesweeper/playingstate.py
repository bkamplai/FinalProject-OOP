import pygame  # type: ignore
from typing import Tuple, Any
from state import State


class PlayingState(State):
    def __init__(self, game: Any) -> None:
        super().__init__(game)
        self.solver_interface = self.game.solver_interface

    def handle_click(self, position: Tuple[int, int]) -> None:
        rightClick: bool = pygame.mouse.get_pressed(num_buttons=3)[2]
        self.game.handleClick(position, rightClick)

    def update(self) -> None:
        self.game.run_solver()
        flags_placed: int = self.solver_interface.get_flags_placed()
        print(f"FLAGS PLACED = {flags_placed}")
        self.game.renderer.draw_board(self.game.board,
                                      flags_placed=flags_placed)
        if self.game.board.get_won() or self.game.board.get_lost():
            print("Game is over")

    def enter(self) -> None:
        print("Entering PlayingState")
        # finalize board setup or other tasks to start playing
        if not self.game.board.initialized:
            self.game.initialize_board()

    def exit(self) -> None:
        print("Exiting PlayingState")
        # cleanup before leaving the playing state
        pass
