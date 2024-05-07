import unittest
from unittest.mock import MagicMock, patch, call
from hypothesis import given, strategies as st  # type: ignore
from gameoverstate import GameOverState


class TestGameOverState(unittest.TestCase):

    def setUp(self) -> None:
        self.game = MagicMock()
        self.game.renderer = MagicMock()
        self.game_over_state = GameOverState(self.game, win=False)

    def test_handle_click(self) -> None:
        @given(st.tuples(st.integers(), st.integers()))  # type: ignore
        def test(position):  # pragma: no cover
            try:
                self.game_over_state.handle_click(position)
                assert True
            except Exception:
                assert False
        test()

    def test_update(self) -> None:
        with patch('pygame.time.wait'), \
             patch.object(self.game.renderer, 'clear_screen'), \
             patch.object(self.game.renderer, 'update_display'):
            self.game_over_state.update()
            self.game.renderer.clear_screen.assert_called_once()
            self.game.renderer.update_display.assert_called_once()

    def test_enter(self) -> None:
        with patch('builtins.print') as mocked_print:
            win_state = GameOverState(self.game, win=True)
            win_state.enter()
            mocked_print.assert_has_calls([call("Entering GameOverState"),
                                           call("Congratulations!")])

        # Test entering a losing state.
        with patch('builtins.print') as mocked_print:
            lose_state = GameOverState(self.game, win=False)
            lose_state.enter()
            mocked_print.assert_has_calls([call("Entering GameOverState"),
                                           call("Ouch!")])

    def test_exit(self) -> None:
        # Test that exiting prints correctly.
        with patch('builtins.print') as mocked_print:
            self.game_over_state.exit()
            mocked_print.assert_called_once_with("Exiting GameOverState")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
