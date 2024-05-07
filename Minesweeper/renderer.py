import pygame  # type: ignore
import os
from typing import Dict, Tuple, List
from space import Space
from board import Board


class Renderer:
    def __init__(self, grid_size: Tuple[int, int], piece_size: Tuple[int, int],
                 extra_height: int = 100) -> None:
        """
        Initialize the renderer
        grid_size (tuple): Size of the grid
        piece_size (tuple): Size of each grid piece (space)
        extra_height (int): Optional extra height for game window
        """
        pygame.init()
        pygame.font.init()  # initalize the font module
        self.piece_size: Tuple[int, int] = piece_size
        self.screen_size: Tuple[int, int] = (
            grid_size[0] * piece_size[0],
            grid_size[1] * piece_size[1] + extra_height)
        self.extra_height: int = extra_height
        self.screen: pygame.Surface = pygame.display.set_mode(self.screen_size)
        # Load game assets
        self.assets: Dict[str, pygame.Surface] = self.load_assets()
        # Initialize font
        self.font: pygame.font.Font = pygame.font.Font(None, 36)

    def load_assets(self) -> Dict[str, pygame.Surface]:
        """
        Load game assets.
        Returns a dictionary that contains the game assets
        """
        assets: Dict[str, pygame.Surface] = {}
        images_dir: str = "images"
        for fileName in os.listdir(images_dir):
            if not fileName.endswith(".png"):
                continue
            path: str = images_dir + r"/" + fileName
            img: pygame.Surface = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(img, (int(self.piece_size[0]),
                                               int(self.piece_size[1])))
            assets[fileName.split(".")[0]] = img
        return assets

    def draw_header(self, mine_count: int, flags_placed: int) -> None:
        """
        Draw the game header (mine count & smiley face).
        mine_count (int): Total number of mines
        flags_placed (int): Total number of flags placed
        """
        header_height: int = 50
        header_rect: pygame.Rect = pygame.Rect(0, 0, self.screen_size[0],
                                               header_height)
        pygame.draw.rect(self.screen, (200, 200, 200), header_rect)

        # Draw the smiley face
        smiley_img: pygame.Surface = pygame.image.load('images/smiley.png')
        smiley_img = pygame.transform.scale(smiley_img, (30, 30))
        smiley_x: int = self.screen_size[0] // 2 - smiley_img.get_width() // 2
        smiley_y: int = header_height // 2 - smiley_img.get_height() // 2
        self.screen.blit(smiley_img, (smiley_x, smiley_y))

        # Print the mine count
        text: str = str(mine_count - flags_placed)
        # print(f"Text: ",{text})
        text_surface: pygame.Surface = self.font.render(text, True, (0, 0, 0))
        text_x: int = 10
        text_y: int = header_height // 2 - text_surface.get_height() // 2
        self.screen.blit(text_surface, (text_x, text_y))

    def draw_board(self, board: Board,
                   mine_positions: List[Tuple[int, int]] = [],
                   flags_placed: int = 0) -> None:
        """
        Draw the game board.
        board (Board): The game board
        mine_positions (list): List of mine positions. Defaults to []
        flags_placed (int): Number of flags placed. Defaults to 0
        """
        header_height: int = 50
        total_header_height: int = header_height
        top_left: Tuple[int, int] = (0, total_header_height)

        # self.screen.fill((0, 0, 0))
        # top_left = (0, 0)

        # Draw the board grid
        for y, row in enumerate(board.get_board()):
            for x, piece in enumerate(row):
                position = (top_left[0] + x * self.piece_size[0], top_left[1]
                            + y * self.piece_size[1])
                if (y, x) in mine_positions:
                    # draw bomb image for selected mine positions
                    self.screen.blit(self.assets['unclicked-bomb'], position)
                else:
                    self.draw_piece(piece, position)
        # Draw the header
        self.draw_header(board.get_total_mine_count(), flags_placed)

    def draw_piece(self, piece: Space, position: Tuple[int, int]) -> None:
        """
        Draw a single piece (space) on the board.
        piece (Piece): Space to draw
        position (tuple): Where to draw the piece
        """
        image_key: str = self.get_image_key(piece)
        image: pygame.Surface = self.assets[image_key]
        self.screen.blit(image, position)

    def get_image_key(self, piece: Space) -> str:
        """
        Get the image key for a game piece.
        piece (Piece): The game piece
        Returns the image key (str)
        """
        if piece.get_clicked():
            return str(piece.get_num_around()) if not piece.get_has_bomb() \
                else 'bomb-at-clicked-block'
        if piece.get_flagged():
            return 'flag'
        return 'empty-block'

    def update_display(self) -> None:
        """ Update the display. """
        pygame.display.flip()

    def clear_screen(self) -> None:
        """ Clear the screen. """
        self.screen.fill((0, 0, 0))
