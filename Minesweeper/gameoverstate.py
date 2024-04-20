from state import State
import pygame

class GameOverState(State):
    def __init__(self, game, win=False):
        super().__init__(game)
        self.win = win

    def handle_click(self, position):
        """ Handle logic to restart the game or quit. """
        pass

    def update(self):
        """ Draw game over screen. """
        pygame.time.wait(5000)
        self.game.renderer.clear_screen()
        #self.game.renderer.display_message("Game Over! Click to exit.", self.game.renderer.screen_size[0] // 2, 50)
        self.game.renderer.update_display()

    def enter(self):
        """ Enter the Game Over State. """
        print("Entering GameOverState")
        if self.win:
            print("Congratulations!")
        else:
            print("Ouch!")
        self.update()

    def exit(self):
        """ Exit the Game Over State. """
        print("Exiting GameOverState")