import unittest
from unittest import mock
from hypothesis import given, strategies as st, settings
import pygame
from pygame import Surface
from renderer import Renderer

class TestRenderer(unittest.TestCase):
    def setUp(self):
        self.renderer = Renderer((10, 10), (32, 32))

    @settings(deadline=None)
    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10), st.integers(min_value=0, max_value=200))
    def test_init(self, gx, gy, eh):
        renderer = Renderer((gx, gy), (32, 32), eh)
        self.assertEqual(renderer.piece_size, (32, 32))
        self.assertEqual(renderer.screen_size, (gx * 32, gy * 32 + eh))
        self.assertIsInstance(renderer.screen, pygame.Surface)

    def test_load_assets(self):
        renderer = Renderer((10, 10), (32, 32))
        assets = renderer.load_assets()
        self.assertIsInstance(assets, dict)
        self.assertTrue(all(isinstance(val, Surface) for val in assets.values()))

    @settings(deadline=None)
    @given(st.lists(st.tuples(st.integers(), st.integers()), unique=True))
    def test_draw_board(self, mine_positions):
        class MockBoard:
            def get_board(self):
                return [[MockPiece() for _ in range(10)] for _ in range(10)]
            def get_total_mine_count(self):
                return len(mine_positions)

        class MockPiece:  # pragma: no cover
            def get_clicked(self):
                return False
            def get_has_bomb(self):
                return False
            def get_flagged(self):
                return False
            def get_num_around(self):
                return 0

        renderer = Renderer((10, 10), (32, 32))
        board = MockBoard()
        renderer.draw_board(board, mine_positions)
    
    def test_get_image_key_clicked_with_bomb(self):
        piece = mock.Mock()
        piece.get_clicked.return_value = True
        piece.get_has_bomb.return_value = True
        self.assertEqual(self.renderer.get_image_key(piece), 'bomb-at-clicked-block')

    def test_get_image_key_clicked_without_bomb(self):
        piece = mock.Mock()
        piece.get_clicked.return_value = True
        piece.get_has_bomb.return_value = False
        piece.get_num_around.return_value = 3
        self.assertEqual(self.renderer.get_image_key(piece), '3')

    def test_get_image_key_flagged(self):
        piece = mock.Mock()
        piece.get_clicked.return_value = False
        piece.get_flagged.return_value = True
        self.assertEqual(self.renderer.get_image_key(piece), 'flag')

    def test_get_image_key_empty(self):
        piece = mock.Mock()
        piece.get_clicked.return_value = False
        piece.get_flagged.return_value = False
        self.assertEqual(self.renderer.get_image_key(piece), 'empty-block')

    @mock.patch('pygame.display.flip')
    def test_update_display(self, mock_flip):
        self.renderer.update_display()
        mock_flip.assert_called_once()

    @mock.patch('pygame.display.set_mode')
    def test_clear_screen(self, mock_set_mode):
        mock_screen = mock.Mock()
        mock_set_mode.return_value = mock_screen
        self.renderer = Renderer((10, 10), (32, 32))
        self.renderer.clear_screen()
        mock_screen.fill.assert_called_once_with((0, 0, 0))

if __name__ == "__main__":  # pragma: no cover
    unittest.main()