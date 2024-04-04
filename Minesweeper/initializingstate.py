import pygame
from state import State
from playingstate import PlayingState

class InitializingState(State):
    def handle_click(self, position):
        grid_pos = self.game.convert_pixel_to_grid(position)
        if grid_pos not in self.game.mine_positions: # prevent duplicate mines
            self.game.mine_positions.append(grid_pos)
            print(f"Mine placed at: {grid_pos}")
            if len(self.game.mine_positions) < self.game.expected_mine_count:
                pass
            else:
                self.game.renderer.draw_board(self.game.board, self.game.mine_positions)
                self.game.renderer.update_display()
                pygame.time.delay(3000)
                self.game.change_state(PlayingState(self.game))
    
    def update(self):
        self.game.renderer.draw_board(self.game.board, self.game.mine_positions)

    def enter(self):
        # any setup needed when entering the initializing state
        self.game.update_mine_placement_message()

    def exit(self):
        # cleanup before leaving the initializing state
        pass
