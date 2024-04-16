import pygame
from state import State

class PlayingState(State):
    def handle_click(self, position):
        rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
        self.game.handleClick(position, rightClick)

    #def handle_keydown(self, event):
        #if event.key == pygame.K_SOMEKEY:
            #self.game.solver.move()
    
    def update(self):
        self.game.run_solver()
        self.game.renderer.draw_board(self.game.board)
        if self.game.board.get_won() or self.game.board.get_lost():
            print("Game is over")
    
    def enter(self):
        print("Entering PlayingState")
        # finalize board setup or other tasks to start playing
        if not self.game.board.initialized:
            self.game.initialize_board()

    def exit(self):
        print("Exiting PlayingState")
        # cleanup before leaving the playing state
        pass
