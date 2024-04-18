import pygame
from state import State
from playingstate import PlayingState

class InitializingState(State):
    def handle_click(self, position):
        """
        Handle click event in Initializing State.
        position (tuple): The position of the click
        """
        grid_pos = self.game.convert_pixel_to_grid(position) # Convert pixel position to grid coordinates
        if grid_pos not in self.game.mine_positions: # Prevent duplicate mines
            self.game.mine_positions.append(grid_pos) # Add mine position to list
            print(f"Mine placed at: {grid_pos}")
            if len(self.game.mine_positions) < self.game.expected_mine_count:
                pass # More mines to place? Continue
            else:
                self.game.renderer.draw_board(self.game.board, self.game.mine_positions) # Draw board w/ mine positions
                self.game.renderer.update_display() # Update the display
                #pygame.time.delay(3000) # Delay before transitioning to playing state
                self.game.change_state(PlayingState(self.game)) # Change game state to Playing State

    def update(self):
        """ Update the board with the selected mine positions. """
        self.game.renderer.draw_board(self.game.board, self.game.mine_positions)

    def enter(self):
        """ Enter the Initializing State. """
        print("Entering InitializingState")
        # any setup needed when entering the initializing state
        self.game.update_mine_placement_message()

    def exit(self):
        """ Exit the Initializing State. """
        print("Exiting InitializingState")
        # cleanup before leaving the initializing state
        pass
