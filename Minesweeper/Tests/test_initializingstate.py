import unittest
from unittest.mock import MagicMock, patch, ANY
from initializingstate import InitializingState


class TestInitializingState(unittest.TestCase):
    def setUp(self) -> None:
        self.game = MagicMock()
        self.state = InitializingState(self.game)
        self.game.expected_mine_count = 5
        self.game.mine_positions = []

    def test_handle_click_adds_new_mine(self) -> None:
        position = (100, 100)
        self.game.convert_pixel_to_grid.return_value = (10, 10)
        self.state.handle_click(position)
        self.assertIn((10, 10), self.game.mine_positions)

    def test_handle_click_prevents_duplicate_mines(self) -> None:
        position = (100, 100)
        self.game.convert_pixel_to_grid.return_value = (10, 10)
        self.game.mine_positions.append((10, 10))
        self.state.handle_click(position)
        self.assertEqual(len(self.game.mine_positions), 1)

    def test_state_transition_to_playing(self) -> None:
        self.game.expected_mine_count = 1
        position = (100, 100)
        self.game.convert_pixel_to_grid.return_value = (10, 10)
        with patch.object(self.game, "change_state") as mock_change_state:
            self.state.handle_click(position)
            mock_change_state.assert_called_with(ANY)

    def test_update_calls_draw(self) -> None:
        with patch.object(self.game.renderer, 'draw_board') as mock_draw_board:
            self.state.update()
            mock_draw_board.assert_called_once()

    def test_enter_prints_message(self) -> None:
        with patch('builtins.print') as mock_print:
            self.state.enter()
            mock_print.assert_called_with("Entering InitializingState")

    def test_exit_prints_message(self) -> None:
        with patch('builtins.print') as mock_print:
            self.state.exit()
            mock_print.assert_called_with("Exiting InitializingState")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
