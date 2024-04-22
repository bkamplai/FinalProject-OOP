import unittest
from unittest.mock import MagicMock, patch, call
from hypothesis import given, strategies as st
from typing import List, Tuple
from advancedsolver import AdvancedSolver
from board import Board


class TestAdvancedSolver(unittest.TestCase):
    def setUp(self) -> None:
        size: Tuple[int, int] = (10, 10)
        mine_count: int = 15
        self.board: Board = Board(size, mine_count)
        self.solver: AdvancedSolver = AdvancedSolver(self.board)

    def test_flag_mines_initial(self) -> None:
        self.board.initialize_mines([])
        result: bool = self.solver.flag_mines()
        self.assertFalse(result)

    @given(st.lists(st.tuples(st.integers(0, 9), st.integers(0, 9)),
                    unique=True))
    def test_flag_mines_effectiveness(self, mine_positions: List[Tuple[
            int, int]]) -> None:
        self.board.initialize_mines(mine_positions)
        result: bool = self.solver.flag_mines()
        self.assertIsInstance(result, bool)

    def test_flag_mines_limits(self) -> None:
        mines: List[Tuple[int, int]] = [
            (i, j) for i in range(5) for j in range(5)]
        self.board.initialize_mines(mines)
        while not self.board.get_lost():
            if not self.solver.flag_mines():
                break
        self.assertTrue(self.board.get_lost() or not self.solver.flag_mines())

    def test_evaluate_border_cells_changes(self) -> None:
        border_cells: List[Tuple[int, int]] = [(0, 0), (0, 1)]
        self.board.initialize_mines([(0, 1)])
        result: bool = self.solver.evaluate_border_cells(border_cells)
        self.assertTrue(result)

    def test_evaluate_border_cells_no_change(self):
        self.board.initialize_mines([])
        for x in range(10):
            for y in range(10):
                self.board.get_piece((x, y)).handle_click()
        border_cells = [(0, 0)]
        result = self.solver.evaluate_border_cells(border_cells)
        self.assertFalse(result,
                         "No changes should occur as all cells are clicked")

    def test_evaluate_border_cells_efficiency(self) -> None:
        border_cells: List[Tuple[int, int]] = [(0, 0), (0, 1)]
        self.board.initialize_mines([(0, 1), (1, 1)])
        self.board.get_piece((0, 1)).toggle_flag()
        self.board.get_piece((1, 1)).toggle_flag()
        self.solver.evaluate_border_cells(border_cells)
        self.assertIn((1, 0), self.solver.safe_squares_to_probe)

    def test_count_flags_around_no_flags(self) -> None:
        self.board.initialize_mines([(0, 1)])
        count: int = self.solver.count_flags_around(0, 0)
        self.assertEqual(count, 0)

    @given(st.integers(0, 9), st.integers(0, 9))
    def test_count_flags_around_with_flags(self, x: int, y: int) -> None:
        self.board.initialize_mines([(x, y)])
        self.board.get_piece((x, y)).toggle_flag()
        count: int = self.solver.count_flags_around(x, y - 1)
        if y > 0:
            self.assertEqual(count, 1)

    def test_count_flags_around_boundary(self) -> None:
        self.board.initialize_mines([(9, 9)])
        self.board.get_piece((9, 9)).toggle_flag()
        count: int = self.solver.count_flags_around(8, 8)
        self.assertEqual(count, 1)

    @given(st.integers(0, 9), st.integers(0, 9))
    def test_find_hidden_tiles_around(self, x: int, y: int) -> None:
        self.board.initialize_mines([])
        hidden_tiles: List[Tuple[int, int]
                           ] = self.solver.find_hidden_tiles_around(x, y)
        self.assertIsInstance(hidden_tiles, list)
        if x > 0 and x < 9 and y > 0 and y < 9:
            self.assertEqual(len(hidden_tiles), 8)

    def test_find_hidden_tiles_around_no_hidden(self) -> None:
        self.board.initialize_mines([])
        self.board.get_piece((0, 0)).handle_click()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= dx < 10 and 0 <= dy < 10:
                    self.board.get_piece((dx, dy)).handle_click()
        hidden_tiles: List[Tuple[int, int]
                           ] = self.solver.find_hidden_tiles_around(0, 0)
        self.assertEqual(len(hidden_tiles), 0)

    def test_find_hidden_tiles_around_edge(self) -> None:
        self.board.initialize_mines([(0, 0)])
        hidden_tiles: List[Tuple[int, int]
                           ] = self.solver.find_hidden_tiles_around(0, 0)
        self.assertGreater(len(hidden_tiles), 0)

    @given(st.integers(min_value=-10, max_value=20), st.integers(min_value=-10,
                                                                 max_value=20))
    def test_is_valid_coord(self, x: int, y: int) -> None:
        result: bool = self.solver.is_valid_coord(x, y)
        self.assertEqual(result, 0 <= x < 10 and 0 <= y < 10)

    def test_stuck_scenario(self):
        mine_positions = [(0, 0), (0, 1), (9, 9)]
        self.board.initialize_mines(mine_positions)
        self.solver.solve()

        self.assertFalse(self.board.get_piece((5, 5)).get_clicked(),
                         "Solver should be stuck without clicking random \
                            squares")
        self.assertFalse(self.board.get_lost(),
                         "Game should not be lost due to guessing")

    def test_game_over_handling(self):
        mine_positions = [(0, 0)]
        self.board.initialize_mines(mine_positions)
        self.board.handle_click(self.board.get_piece((0, 0)), False)
        self.solver.solve()

        self.assertTrue(self.board.get_lost(),
                        "Game should be recognized as lost")
        self.assertFalse(self.board.get_won(), "Game should not be won")

    def test_flag_mines_no_flags(self):
        with patch.object(self.board, 'get_piece',
                          return_value=MagicMock(get_clicked=lambda: False,
                                                 get_flagged=lambda: False)):
            self.assertFalse(self.solver.flag_mines())

    def test_flag_mines_flags_placed(self):
        cell = MagicMock(get_clicked=lambda: True, get_flagged=lambda: False,
                         get_num_around=lambda: 2)

        hidden_tile1 = MagicMock(get_clicked=lambda: False,
                                 get_flagged=lambda: False)
        hidden_tile2 = MagicMock(get_clicked=lambda: False,
                                 get_flagged=lambda: False)

        def get_piece_side_effect(coord):
            if coord == (0, 0):
                return cell
            elif coord in [(0, 1), (0, 2)]:
                return hidden_tile1 if coord == (0, 1) else hidden_tile2
            else:
                return MagicMock(get_clicked=lambda: False,
                                 get_flagged=lambda: True)

        self.board.get_piece = MagicMock(side_effect=get_piece_side_effect)

        with patch.object(self.board, 'count_flags', return_value=0
                          ) as mock_count_flags, \
            patch.object(self.board, 'get_total_mine_count', return_value=10
                         ) as mock_total_mines, \
            patch.object(self.solver, 'count_flags_around', return_value=0
                         ) as mock_flags_around, \
            patch.object(self.solver, 'find_hidden_tiles_around',
                         return_value=[(0, 1), (0, 2)]) as mock_hidden_tiles, \
                patch.object(self.board, 'handle_click') as mock_handle_click:

            result = self.solver.flag_mines()

            self.assertTrue(result, "The flag_mines method should have \
                            returned True, indicating that flags were placed.")
            self.assertEqual(mock_handle_click.call_count, 2, "handle_click \
                             should have been called twice to flag two mines.")
            mock_handle_click.assert_has_calls([call(hidden_tile1, True), call(
                hidden_tile2, True)], any_order=True)

            print(f"Result of flag_mines: {result}")
            print(f"Call count of handle_click: {mock_handle_click.call_count}"
                  )
            print(f"Flags around count: {mock_flags_around.return_value}")
            print(f"Hidden tiles around: {mock_hidden_tiles.return_value}")
            print(f"Flag count: {mock_count_flags.return_value}")
            print(f"Max flags: {mock_total_mines.return_value}")

    def test_solve_early_termination_lost(self):
        with patch.object(self.board, 'get_lost', return_value=True):
            self.solver.solve()
            self.assertTrue(self.board.get_lost.called)

    def test_get_flags_placed(self):
        self.solver.flags_placed = 5
        self.assertEqual(self.solver.get_flags_placed(), 5)

    def test_act_on_findings(self):
        self.solver.mines_identified = [(1, 1)]
        self.solver.safe_squares_to_probe = [(1, 2)]
        mine_cell = MagicMock(get_flagged=lambda: False)
        safe_cell = MagicMock(get_clicked=lambda: False)
        self.board.get_piece = MagicMock(
            side_effect=lambda x: mine_cell if x == (1, 1) else safe_cell)

        with patch.object(self.board, 'handle_click') as mock_handle_click:
            self.solver.act_on_findings()
            expected_calls = [((mine_cell, True),), ((safe_cell, False),)]
            mock_handle_click.assert_has_calls(expected_calls, any_order=True)

    def test_flag_mines_places_flags_correctly(self):
        cell = MagicMock(get_clicked=lambda: True, get_flagged=lambda: False,
                         get_num_around=lambda: 2)
        hidden_tile1 = MagicMock(get_clicked=lambda: False,
                                 get_flagged=lambda: False)
        hidden_tile2 = MagicMock(get_clicked=lambda: False,
                                 get_flagged=lambda: False)

        def get_piece_side_effect(coord):
            if coord == (0, 0):
                return cell
            elif coord == (0, 1):
                return hidden_tile1
            elif coord == (0, 2):
                return hidden_tile2
            return MagicMock(get_clicked=lambda: True,
                             get_flagged=lambda: True)

        self.board.get_piece = MagicMock(side_effect=get_piece_side_effect)
        self.board.count_flags = MagicMock(return_value=0)
        self.board.get_total_mine_count = MagicMock(return_value=10)
        self.solver.count_flags_around = MagicMock(return_value=0)
        self.solver.find_hidden_tiles_around = MagicMock(return_value=[(0, 1),
                                                                       (0, 2)])

        with patch.object(self.board, 'handle_click',
                          autospec=True) as mock_handle_click:
            result = self.solver.flag_mines()

            self.assertTrue(result, "flag_mines should return True indicating \
                            that flags were placed.")
            expected_calls = [call(hidden_tile1, True), call(hidden_tile2,
                                                             True)]
            mock_handle_click.assert_has_calls(expected_calls, any_order=True)

    def test_solve_terminates_when_lost(self):
        self.board.get_lost = MagicMock(return_value=True)
        with patch('builtins.print') as mock_print:
            self.solver.solve()
            mock_print.assert_called_with("GAME OVER ADVANCED SOLVER")

    def test_solve_continues_when_flags_placed(self):
        self.board.get_lost = MagicMock(return_value=False)
        self.solver.find_border_cells = MagicMock(return_value=[(0, 0)])
        self.solver.evaluate_border_cells = MagicMock(return_value=False)
        self.solver.flag_mines = MagicMock(side_effect=[True, False])

        expected_message = "No more certain moves to make. The solver is \
            either stuck or the puzzle is solved."
        with patch('builtins.print') as mock_print:
            self.solver.solve()
            mock_print.assert_called_with(expected_message)

    def test_no_flagging_when_at_max_flags(self):
        self.board.get_piece = MagicMock(return_value=MagicMock(
            get_clicked=lambda: True,
            get_flagged=lambda: False,
            get_num_around=lambda: 2
        ))
        self.board.count_flags = MagicMock(return_value=10)
        self.board.get_total_mine_count = MagicMock(return_value=10)
        self.solver.count_flags_around = MagicMock(return_value=0)
        self.solver.find_hidden_tiles_around = MagicMock(return_value=[(0, 1),
                                                                       (0, 2)])

        with patch.object(self.board, 'handle_click') as mock_handle_click:
            result = self.solver.flag_mines()
            self.assertFalse(result)
            mock_handle_click.assert_not_called()

    def test_no_action_possible(self):
        self.board.get_piece = MagicMock(return_value=MagicMock(
            get_clicked=lambda: False,
            get_flagged=lambda: True,
            get_num_around=lambda: 0
        ))
        self.board.count_flags = MagicMock(return_value=10)
        self.board.get_total_mine_count = MagicMock(return_value=10)

        result = self.solver.flag_mines()
        self.assertFalse(result)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
