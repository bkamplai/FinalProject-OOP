import pygame  # type: ignore
from typing import Tuple, Any
from state import State


class GameOverState(State):
    def __init__(self, game: Any, win: bool = False) -> None:
        super().__init__(game)
        self.win: bool = win

    def handle_click(self, position: Tuple[int, int]) -> None:
        """ Handle logic to restart the game or quit. """
        pass

    def update(self) -> None:
        """ Draw game over screen. """
        pygame.time.wait(5000)
        self.game.renderer.clear_screen()
        # self.game.renderer.display_message(
        #     "Game Over! Click to exit.",
        #     self.game.renderer.screen_size[0] // 2, 50)
        self.game.renderer.update_display()

    def enter(self) -> None:
        """ Enter the Game Over State. """
        print("Entering GameOverState")
        if self.win:
            print("Congratulations!")
        else:
            print("Ouch!")
        self.update()

    def exit(self) -> None:
        """ Exit the Game Over State. """
        print("Exiting GameOverState")
