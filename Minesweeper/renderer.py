import pygame
import os
from typing import Dict

class Renderer:
    def __init__(self, grid_size, piece_size, extra_height=100) -> None: #reference code
        pygame.init()
        pygame.font.init() # initalize the font module
        self.piece_size = piece_size
        self.screen_size = (grid_size[0] * piece_size[0], grid_size[1] * piece_size[1] + extra_height)
        self.extra_height = extra_height
        self.screen = pygame.display.set_mode(self.screen_size)

        #load images here!
        #self.sizeScreen = 800, 800
        #self.screen = pygame.display.set_mode(self.sizeScreen)
        #self.pieceSize = (self.sizeScreen[0] / size[1], self.sizeScreen[1] / size[0]) 
        
        self.assets = self.load_assets()
        self.font = pygame.font.Font(None, 36)
        #self.loadPictures()

    def load_assets(self) -> Dict[str,pygame.Surface]: # reference code
        #self.images = {}
        assets = {}
        images_dir = "images"
        for fileName in os.listdir(images_dir):
            if not fileName.endswith(".png"):
                continue
            path = images_dir + r"/" + fileName 
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(img, (int(self.piece_size[0]), int(self.piece_size[1])))
            assets[fileName.split(".")[0]] = img
        return assets
    
    def draw_board(self, board, mine_positions=[]) -> None:
        self.screen.fill((0, 0, 0))
        top_left = (0, 0)
        for y, row in enumerate(board.get_board()):
            for x, piece in enumerate(row): # call piece space?
                position = (top_left[0] + x * self.piece_size[0], top_left[1] + y * self.piece_size[1])
                if (y, x) in mine_positions:
                    # draw bomb image for selected mine positions
                    self.screen.blit(self.assets['unclicked-bomb'], position)
                else:
                    self.draw_piece(piece, position)
                    #self.draw_piece(piece, top_left)
                #top_left = top_left[0] + self.piece_size[0], top_left[1]
            #top_left = (0, top_left[1] + self.piece_size[1])
    
    def draw_piece(self, piece, position) -> None:
        image_key = self.get_image_key(piece)
        image = self.assets[image_key]
        self.screen.blit(image, position)
    
    def get_image_key(self, piece) -> str:
        if piece.get_clicked():
            return str(piece.get_num_around()) if not piece.get_has_bomb() else 'bomb-at-clicked-block'
        if piece.get_flagged():
            return 'flag'
        return 'empty-block'

    def update_display(self) -> None:
        #self.screen.fill((0, 0, 0))
        pygame.display.flip()
    
    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def display_message(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, 10)) # get rectangle of text surface and center
        self.screen.blit(text_surface, text_rect) # Draw text on screen
        pygame.display.update(text_rect)
