import unittest
from unittest.mock import MagicMock, patch, call, ANY
from game import Game
from playingstate import PlayingState
from gameoverstate import GameOverState
from initializingstate import InitializingState
from pygame import QUIT, MOUSEBUTTONDOWN, KEYDOWN

class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game((5, 5), 5)
        self.mock_state = MagicMock(spec=PlayingState)
        self.game.state = self.mock_state
        self.game.solver = MagicMock()
        self.game.renderer = MagicMock()
        self.game.renderer.piece_size = (160, 160)
        self.game.renderer.screen_size = (800, 100)
        self.game.board = MagicMock()
        self.game.board.get_lost.return_value = False
    
    def test_run_solver_playing_state(self):
        self.game.state = PlayingState(self.game)
        self.game.expected_mine_count = 5
        self.game.board.count_flags = MagicMock(return_value=4)
        self.game.solver_interface.solve = MagicMock()
        self.game.run_solver()
        self.game.solver_interface.solve.assert_called()
    
    def test_run_solver_not_playing_state(self):
        self.game.state = InitializingState(self.game)
        self.game.solver_interface.solve = MagicMock()
        self.game.run_solver()
        self.game.solver_interface.solve.assert_not_called()
    
    def test_solver_triggered_after_run(self):
        self.game.run_solver()
        self.assertFalse(self.game.solver_triggered)
    
    def test_change_state(self):
        old_state = MagicMock()
        new_state = MagicMock()
        self.game.state = old_state
        self.game.change_state(new_state)
        old_state.exit.assert_called_once()
        new_state.enter.assert_called_once()
        self.assertEqual(self.game.state, new_state)

    def test_convert_pixel_to_grid(self):
        pixel_position = (450, 300)
        expected_grid_position = (1, 2)
        self.assertEqual(self.game.convert_pixel_to_grid(pixel_position), expected_grid_position)
    
    def test_handle_click(self):
        position = (450, 300)
        flag = True
        self.game.handleClick(position, flag)
        self.game.board.handle_click.assert_called_once()
    
    def test_run(self):
        self.game.pygame = MagicMock()
        self.game.run()
        self.assertTrue(self.game.renderer.update_display.called)
    
    def test_run_quit_event(self):
        with patch("pygame.event.get", return_value=[MagicMock(type=QUIT)]):
            self.game.run()
            self.game.renderer.update_display.assert_called()
    
    def test_handle_mouse_button_down(self):
        with patch("pygame.event.get", return_value=[MagicMock(type=MOUSEBUTTONDOWN)]):
            with patch("pygame.mouse.get_pos", return_value=(100, 100)):
                self.game.run()
                self.mock_state.handle_click.assert_called_with((100, 100))
    
    def test_handle_key_down(self):
        self.game.board.initialized = True
        self.game.board.get_lost.return_value = False
        event = MagicMock(type=KEYDOWN)
        with patch("pygame.event.get", return_value=[event]):
            self.game.run()
            self.game.solver.move.assert_called()

    def test_initialize_board(self):
        self.game.initialize_board()
        self.game.board.initialize_mines.assert_called_with(self.game.mine_positions)
        self.assertTrue(self.game.board.initialized)

    def test_win(self):
        with patch('pygame.mixer.Sound') as mock_sound:
            with patch('time.sleep', return_value=None):
                self.game.win()
                mock_sound.assert_called_with('win.wav')
                mock_sound.return_value.play.assert_called()
    
    def test_run_solver_playing_state_trivial_solver(self):
        self.game.state = PlayingState(self.game)
        self.game.solver_interface.set_solver = MagicMock()
        self.game.solver_interface.solve = MagicMock()
        self.game.run_solver()
        self.game.solver_interface.set_solver.assert_any_call('trivial')
    
    def test_run_solver_playing_state_flag_count_matches(self):
        self.game.state = PlayingState(self.game)
        self.game.expected_mine_count = 3
        self.game.board.count_flags = MagicMock(return_value=3)
        self.game.board.reveal_all_non_flagged_squares = MagicMock()
        self.game.board.check_won = MagicMock(return_value=True)
        self.game.change_state = MagicMock()
        self.game.run_solver()
        self.game.board.reveal_all_non_flagged_squares.assert_called_once()
        self.game.board.check_won.assert_called_once()
        self.game.change_state.assert_called_with(ANY)

        call_args = self.game.change_state.call_args
        if call_args:
            args, kwargs = call_args
            game_over_state_instance = args[0]
            assert isinstance(game_over_state_instance, GameOverState), "Must be an instance of GameOverState"
            assert game_over_state_instance.win == True, "Win must be True"
    
    def test_run_solver_playing_state_advanced_solver_triggered(self):
        self.game.state = PlayingState(self.game)
        self.game.solver_interface.set_solver = MagicMock()
        self.game.solver_interface.solve = MagicMock()
        self.game.shouldSwitchSolver = MagicMock(return_value=True)
        self.game.run_solver()
        calls = [call('trivial'), call('advanced')]
        self.game.solver_interface.set_solver.assert_has_calls(calls)
        self.assertEqual(self.game.solver_interface.solve.call_count, 2)
        self.assertFalse(self.game.solver_triggered)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()