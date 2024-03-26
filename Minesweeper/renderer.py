import pygame
import os
from typing import Dict

class Renderer:
    def __init__(self, screen_size, piece_size) -> None: #reference code
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        #load images here!
        #self.sizeScreen = 800, 800
        #self.screen = pygame.display.set_mode(self.sizeScreen)
        #self.pieceSize = (self.sizeScreen[0] / size[1], self.sizeScreen[1] / size[0]) 
        self.piece_size = piece_size
        self.assets = self.load_assets()
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
    
    def draw_board(self, board) -> None:
        self.screen.fill((0, 0, 0))
        top_left = (0, 0)
        for row in board.get_board():
            for piece in row: # call piece space?
                self.draw_piece(piece, top_left)
                #rect = pygame.Rect(top_left, self.pieceSize)
                #image = self.images[self.getImageString(piece)]
                #self.screen.blit(image, top_left) 
                top_left = top_left[0] + self.piece_size[0], top_left[1]
            top_left = (0, top_left[1] + self.piece_size[1])
    
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
        pygame.display.flip()