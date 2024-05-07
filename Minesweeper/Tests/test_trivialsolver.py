import unittest
from unittest.mock import MagicMock, patch
from hypothesis import given, strategies as st  # type: ignore
from typing import Tuple
from trivialsolver import TrivialSolver


class TestTrivialSolver(unittest.TestCase):
    def setUp(self) -> None:
        self.board = MagicMock()
        self.solver = TrivialSolver(self.board)
        self.board.get_size.return_value = (10, 10)

    def test_find_potentially_safe_tile_no_safe_tiles(self) -> None:
        self.board.get_piece.return_value = MagicMock(get_clicked=lambda: True,
                                                      get_flagged=lambda: True)
        result = self.solver.find_potentially_safe_tile(5, 5)
        self.assertIsNone(result)

    @given(st.integers(min_value=0, max_value=9),
           st.integers(min_value=0, max_value=9))  # type: ignore
    def test_find_potentially_safe_tile_with_hypothesis(self, x: int, y: int
                                                        ) -> None:
        self.board.get_piece.return_value = MagicMock(get_clicked=lambda: True,
                                                      get_flagged=lambda:
                                                      False)
        result = self.solver.find_potentially_safe_tile(x, y)
        self.assertIsNone(result)

    def test_get_flags_placed(self) -> None:
        self.assertEqual(self.solver.get_flags_placed(), 0)

    def test_select_random_tile(self) -> None:
        self.board.get_piece.return_value = MagicMock(get_clicked=lambda:
                                                      False,
                                                      get_flagged=lambda:
                                                      False)
        result = self.solver.select_random_tile()
        self.assertIsNotNone(result)

    def test_solve_method(self) -> None:
        self.solver.select_random_tile = MagicMock(  # type: ignore
            side_effect=[(0, 0), (1, 1), None])
        piece_mock_0_0 = MagicMock(get_clicked=lambda: False,
                                   get_num_around=lambda: 0)
        piece_mock_1_1 = MagicMock(get_clicked=lambda: False,
                                   get_num_around=lambda: 1)

        def get_piece_mock(coord: Tuple[int, int]
                           ) -> MagicMock:  # pragma: no cover
            x, y = coord
            if (x, y) == (0, 0):
                return piece_mock_0_0
            elif (x, y) == (1, 1):
                return piece_mock_1_1
            raise ValueError("Invalid coordinates")

        self.board.get_piece.side_effect = get_piece_mock

        with patch.object(self.board, 'handle_click') as mock_handle_click, \
             patch.object(self.board, 'get_lost', side_effect=[False, False,
                                                               True]):
            self.solver.solve()

            print("handle_click call count:", mock_handle_click.call_count)
            self.assertEqual(mock_handle_click.call_count, 1)

    def test_select_random_tile_no_unrevealed_tiles(self) -> None:
        self.board.get_size.return_value = (5, 5)
        self.board.get_piece.return_value.get_clicked.return_value = True
        self.board.get_piece.return_value.get_flagged.return_value = False
        self.assertIsNone(self.solver.select_random_tile())

    def test_select_random_tile_with_unrevealed_tiles(self) -> None:
        self.board.get_size.return_value = (5, 5)
        self.board.get_piece.side_effect = lambda coord: MagicMock(
            get_clicked=lambda: (coord[0] + coord[1]) % 2 == 0,
            get_flagged=lambda: False)
        tile = self.solver.select_random_tile()
        self.assertIn(tile, [(x, y) for x in range(5) for y in range(5) if (
            x + y) % 2 == 1])

    def test_find_potentially_safe_tile_no_safe_tiles2(self) -> None:
        self.board.get_size.return_value = (10, 10)
        self.board.get_piece.return_value.get_clicked.return_value = False
        self.board.get_piece.return_value.get_flagged.return_value = True
        self.assertIsNone(self.solver.find_potentially_safe_tile(5, 5))

    def test_solve_game_over_on_first_tile(self) -> None:
        self.board.get_lost.return_value = True
        with self.assertLogs('trivialsolver', level='INFO') as cm:
            self.solver.solve()
        self.assertTrue(any(
            "TRIVIAL SOLVER GAME OVER" in message for message in cm.output))

    def test_find_potentially_safe_tile_with_safe_tiles(self) -> None:
        detailed_logger = MagicMock()

        def get_piece_mock(coord: Tuple[int, int]
                           ) -> MagicMock:  # pragma: no cover
            x, y = coord
            mock_tile = MagicMock()
            if (x, y) == (3, 3):
                mock_tile.get_clicked.return_value = False
                mock_tile.get_flagged.return_value = False
                detailed_logger(
                    f"Tile at ({x}, {y}): Clicked=False, Flagged=False")
            else:
                mock_tile.get_clicked.return_value = True
                mock_tile.get_flagged.return_value = True
                detailed_logger(
                    f"Tile at ({x}, {y}): Clicked=True, Flagged=True")
            return mock_tile

        self.board.get_piece.side_effect = get_piece_mock

        result = self.solver.find_potentially_safe_tile(5, 5)

        print("Logging calls:")
        for log_call in detailed_logger.mock_calls:
            print(log_call)

        self.assertEqual(result, (3, 3), f"Expected (3, 3), but got {result}")

    def test_solve_game_already_lost(self) -> None:
        self.board.get_lost.return_value = True
        with self.assertLogs('trivialsolver', level='INFO') as log:
            self.solver.solve()
            self.assertIn("TRIVIAL SOLVER GAME OVER", log.output[1])

    def test_solve_no_additional_safe_moves_found(self) -> None:
        self.solver.select_random_tile = MagicMock(  # type: ignore
            return_value=(3, 3))
        self.solver.find_potentially_safe_tile = MagicMock(  # type: ignore
            return_value=None)
        self.board.get_lost.return_value = False
        mock_piece = MagicMock(get_num_around=lambda: 1,
                               get_clicked=lambda: False,
                               get_flagged=lambda: False)
        self.board.get_piece.return_value = mock_piece

        with self.assertLogs('trivialsolver', level='INFO') as log:
            self.solver.solve()
            expected_log_message = "INFO:trivialsolver:No additional safe "\
                "move was found, stopping solver."
            found = any(expected_log_message in log_message for log_message in
                        log.output)
            self.assertTrue(found, "Expected log message not found in output.")

    def test_solve_reveal_empty_tile(self) -> None:
        self.solver.select_random_tile = MagicMock(  # type: ignore
            return_value=(3, 3))
        self.board.get_lost.return_value = False
        self.board.get_piece.side_effect = lambda coord: MagicMock(
            get_num_around=lambda: 0, get_clicked=lambda: False,
            get_flagged=lambda: False)
        self.board.handle_click = MagicMock()

        with self.assertLogs('trivialsolver', level='INFO') as log:
            self.solver.solve()
            expected_log_message = "Revealed an empty space, board should "\
                "auto-reveal tiles"
            found = any(expected_log_message in log_message for log_message in
                        log.output)
            self.assertTrue(found, "Expected log message not found in output.")

    def test_solve_continuous_safe_tile_revelation(self) -> None:
        self.solver.select_random_tile = MagicMock()  # type: ignore
        self.solver.find_potentially_safe_tile = MagicMock()  # type: ignore
        self.board.get_lost.return_value = False

        tile_sequence = [(5, 5), (6, 6), (7, 7)]
        safe_tile_sequence = [(6, 6), (7, 7), None]

        self.solver.select_random_tile.side_effect = tile_sequence
        self.solver.find_potentially_safe_tile.side_effect = safe_tile_sequence

        mock_piece = MagicMock(get_num_around=lambda: 1,
                               get_clicked=lambda: False,
                               get_flagged=lambda: False)
        self.board.get_piece.return_value = mock_piece
        self.board.handle_click = MagicMock()

        with self.assertLogs('trivialsolver', level='INFO') as log:
            self.solver.solve()

            expected_logs = [
                "INFO:trivialsolver:In TrivialSolver solve()",
                "INFO:trivialsolver:Attempting to reveal tile at (5, 5)",
                "INFO:trivialsolver:Found potentially safe tile at (6, 6), " +
                "attempting to reveal",
                "INFO:trivialsolver:Attempting to reveal tile at (6, 6)",
                "INFO:trivialsolver:Found potentially safe tile at (7, 7), " +
                "attempting to reveal",
                "INFO:trivialsolver:Attempting to reveal tile at (7, 7)",
                "INFO:trivialsolver:No additional safe move was found, " +
                "stopping solver."
            ]

            for expected_log in expected_logs:
                self.assertIn(expected_log, log.output)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
