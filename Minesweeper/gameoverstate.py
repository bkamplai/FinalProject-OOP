from state import State
import pygame

class GameOverState(State):
    def handle_click(self, position):
        # Handle logic to restart the game or quit
        pass

    def update(self):
        # Draw game over screen
        self.game.renderer.clear_screen()
        #self.game.renderer.display_message("Game Over! Click to exit.", self.game.renderer.screen_size[0] // 2, 50)
        self.game.renderer.update_display()

    def enter(self):
        print("Entering GameOverState")
        self.update()

    def exit(self):
        print("Exiting GameOverState")