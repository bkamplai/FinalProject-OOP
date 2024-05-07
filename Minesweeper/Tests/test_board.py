import unittest
from unittest.mock import patch, Mock
import io
from hypothesis import given, strategies as st  # type: ignore
from typing import Tuple, List
from board import Board


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board: Board = Board((5, 5), 5)

    def test_initialize_mines_valid(self) -> None:
        positions: List[Tuple[int, int]] = [(0, 0), (1, 1), (2, 2), (3, 3),
                                            (4, 4)]
        self.board.initialize_mines(positions)
        for position in positions:
            self.assertTrue(self.board.get_piece(position).has_bomb)

    def test_initialize_mines_invalid(self) -> None:
        positions: List[Tuple[int, int]] = [(0, 0), (6, 6), (-1, -1), (5, 5),
                                            (100, 100)]
        with self.assertRaises(IndexError):
            self.board.initialize_mines(positions)

    @given(st.integers(min_value=0, max_value=4),
           st.integers(min_value=0, max_value=4))  # type: ignore
    def test_get_piece(self, row: int, col: int) -> None:
        piece = self.board.get_piece((row, col))
        self.assertFalse(piece.has_bomb)

    def test_handle_click_on_mine(self) -> None:
        positions: List[Tuple[int, int]] = [(0, 0)]
        self.board.initialize_mines(positions)
        self.board.handle_click(self.board.get_piece((0, 0)), False)
        self.assertTrue(self.board.get_lost())

    def test_handle_click_flag(self) -> None:
        self.board.handle_click(self.board.get_piece((0, 0)), True)
        self.assertTrue(self.board.get_piece((0, 0)).flagged)

    def test_handle_click_uncover_safe_area(self) -> None:
        positions: List[Tuple[int, int]] = [(0, 0)]
        self.board.initialize_mines(positions)
        self.board.handle_click(self.board.get_piece((1, 1)), False)
        self.assertFalse(self.board.get_lost())
        self.assertTrue(self.board.get_piece((1, 1)).clicked)

    def test_print_board(self) -> None:
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.board.print_board()
            output = fake_out.getvalue()
            self.assertTrue(len(output) > 0)

    def test_get_board(self) -> None:
        board = self.board.get_board()
        self.assertEqual(len(board), 5)
        self.assertEqual(len(board[0]), 5)

    def test_get_size(self) -> None:
        size = self.board.get_size()
        self.assertEqual(size, (5, 5))

    def test_handle_click_uncover_safe_full_area(self) -> None:
        self.board.handle_click(self.board.get_piece((0, 0)), False)
        self.assertTrue(self.board.get_piece((0, 0)).clicked)

    def test_check_won_false(self) -> None:
        self.assertFalse(self.board.check_won())

    def test_check_won_true(self) -> None:
        self.board.won = True
        self.assertTrue(self.board.get_won())

    def test_get_won_initial_state(self) -> None:
        self.assertFalse(self.board.get_won())

    def test_handle_click_already_clicked(self) -> None:
        piece = self.board.get_piece((0, 0))
        piece.handle_click()
        with self.subTest("Click on already clicked piece"):
            output_before = piece.clicked
            self.board.handle_click(piece, False)
            output_after = piece.clicked
            self.assertEqual(output_before, output_after)

    def test_handle_click_flagged_no_toggle(self) -> None:
        piece = self.board.get_piece((0, 0))
        piece.toggle_flag()
        with self.subTest("Click on flagged piece without toggling"):
            output_before = piece.flagged
            self.board.handle_click(piece, False)
            output_after = piece.flagged
            self.assertTrue(output_before and output_after)

    def test_check_won_not_all_clicked(self) -> None:
        for i in range(2):
            for j in range(5):
                piece = self.board.get_piece((i, j))
                if not piece.get_has_bomb():
                    piece.handle_click()

        self.assertFalse(self.board.check_won())

    def test_check_won_all_clicked(self) -> None:
        for row in range(5):
            for col in range(5):
                piece = self.board.get_piece((row, col))
                if not piece.get_has_bomb():
                    piece.handle_click()

        self.assertTrue(self.board.check_won())

    def test_reveal_all_non_flagged_squares(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        board.board = [[Mock() for _ in range(3)] for _ in range(3)]
        for row in board.board:
            for space in row:
                space.get_flagged.return_value = False  # type: ignore
                space.get_clicked.return_value = False  # type: ignore
        with patch.object(board, 'handle_click') as mocked_handle_click:
            board.reveal_all_non_flagged_squares()
            self.assertEqual(mocked_handle_click.call_count, 9)

    def test_count_flags(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        board.board = [[Mock() for _ in range(3)] for _ in range(3)]
        for row in board.board:
            for space in row:
                space.get_flagged.return_value = True  # type: ignore
        flags = board.count_flags()
        self.assertEqual(flags, 9)

    def test_handle_click_game_lost(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        board.get_lost = Mock(return_value=True)  # type: ignore
        with patch('builtins.print') as mocked_print:
            board.handle_click(Mock(), False)
            mocked_print.assert_called_with(
                "Click ignored: game already lost.")

    def test_handle_click_flag2(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        space = Mock()
        space.get_clicked.return_value = False
        space.get_flagged.return_value = False
        with patch.object(space, 'toggle_flag') as mocked_toggle_flag:
            board.handle_click(space, True)
            mocked_toggle_flag.assert_called_once()

    def test_is_board_opened(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        board.board = [[Mock() for _ in range(3)] for _ in range(3)]
        board.board[0][0].get_clicked.return_value = True  # type: ignore
        board.board[0][0].get_num_around.return_value = 0  # type: ignore
        self.assertTrue(board.is_board_opened())

    def test_click_ignored_if_game_lost(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        board.get_lost = Mock(return_value=True)  # type: ignore
        with patch('builtins.print') as mocked_print:
            board.handle_click(Mock(), False)
            mocked_print.assert_called_once_with(
                "Click ignored: game already lost.")

    def test_click_no_action_if_clicked_or_wrong_flag(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        space = Mock()
        space.get_clicked.return_value = True
        board.handle_click(space, False)

        space.get_clicked.return_value = False
        space.get_flagged.return_value = True
        board.handle_click(space, False)

    def test_toggle_flag_on_click(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        space = Mock()
        space.get_clicked.return_value = False
        space.get_flagged.return_value = False
        with patch.object(space, 'toggle_flag') as mocked_toggle_flag:
            board.handle_click(space, True)
            mocked_toggle_flag.assert_called_once()

    def test_is_board_opened_true(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        board.board = [[Mock() for _ in range(3)] for _ in range(3)]
        board.board[1][1].get_clicked.return_value = True  # type: ignore
        board.board[1][1].get_num_around.return_value = 0  # type: ignore
        self.assertTrue(board.is_board_opened())

    def test_is_board_opened_false(self) -> None:
        board = Board(size=(3, 3), mine_count=1)
        board.board = [[Mock() for _ in range(3)] for _ in range(3)]
        for row in board.board:
            for space in row:
                space.get_clicked.return_value = False  # type: ignore
                space.get_num_around.return_value = 1  # type: ignore
        self.assertFalse(board.is_board_opened())


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
