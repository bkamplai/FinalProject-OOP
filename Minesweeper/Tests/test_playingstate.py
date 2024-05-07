import unittest
from unittest.mock import MagicMock, patch
from playingstate import PlayingState
from hypothesis import given, strategies as st  # type: ignore


class TestPlayingState(unittest.TestCase):
    def setUp(self) -> None:
        self.game = MagicMock()
        self.state = PlayingState(self.game)

    @given(position=st.tuples(st.integers(min_value=0, max_value=800),
                              st.integers(min_value=0, max_value=600)
                              ))  # type: ignore
    def test_handle_click(self, position) -> None:
        with patch("pygame.mouse.get_pressed", return_value=(1, 0, 0)):
            self.state.handle_click(position)
            self.game.handleClick.assert_called_with(position, False)

        with patch("pygame.mouse.get_pressed", return_value=(0, 0, 1)):
            self.state.handle_click(position)
            self.game.handleClick.assert_called_with(position, True)

    def test_update(self) -> None:
        with patch.object(self.game.renderer, "draw_board") as mock_draw:
            self.state.\
                solver_interface.get_flags_placed = MagicMock(  # type: ignore
                    return_value=10)
            self.state.update()
            mock_draw.assert_called_once_with(self.game.board, flags_placed=10)

    def test_enter(self) -> None:
        with patch("builtins.print") as mock_print:
            self.state.enter()
            mock_print.assert_called_with("Entering PlayingState")
            self.assertTrue(self.game.some_initialization_flag)

    def test_enter_initializes_board_when_not_initialized(self) -> None:
        self.game.board.initialized = False

        with patch.object(self.game,
                          "initialize_board") as mock_initialize_board:
            self.state.enter()
            mock_initialize_board.assert_called_once()

        with patch('builtins.print') as mock_print:
            self.state.enter()
            mock_print.assert_called_with("Entering PlayingState")

    def test_enter_does_not_initialize_board_when_already_initialized(
            self) -> None:
        self.game.board.initialized = True

        with patch.object(self.game,
                          "initialize_board") as mock_initialize_board:
            self.state.enter()
            mock_initialize_board.assert_not_called()

    def test_exit(self) -> None:
        with patch("builtins.print") as mock_print:
            self.state.exit()
            mock_print.assert_called_with("Exiting PlayingState")
            self.assertTrue(self.game.cleanup_flag)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
