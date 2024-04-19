import unittest
from unittest.mock import MagicMock, patch, Mock
from solver import Solver

class TestSolver(unittest.TestCase):
    def setUp(self):
        self.board = MagicMock()
        self.solver = Solver(self.board)
        self.piece = MagicMock()
        self.unclicked_piece = MagicMock(get_clicked=MagicMock(return_value=False))
        self.clicked_piece = MagicMock(get_clicked=MagicMock(return_value=True))
    
    def test_set_strategy(self):
        strategy = MagicMock()
        self.solver.set_strategy(strategy)
        self.assertEqual(self.solver.strategy, strategy)
    
    def test_solve_without_strategy(self):
        with self.assertRaises(ValueError):
            self.solver.solve()
    
    def test_solve_with_strategy(self):
        strategy = MagicMock()
        self.solver.set_strategy(strategy)
        self.solver.solve()
        strategy.solve.assert_called_with(self.board)

    def test_move_logic_open_unflagged_called_correctly(self):
        self.board.get_board.return_value = [[self.piece]]
        self.piece.get_clicked.return_value = True
        self.piece.get_num_around.return_value = 1
        neighbor = MagicMock()
        neighbor.get_clicked.return_value = False
        neighbor.get_flagged.return_value = True
        self.piece.get_neighbors.return_value = [neighbor]

        with patch.object(self.solver, "open_unflagged") as mock_open, \
            patch.object(self.solver, "flag_all") as mock_flag:
            self.solver.move()
            mock_open.assert_called_once_with([neighbor])
            mock_flag.assert_not_called()

    def test_move_logic_flag_all_called(self):
        self.board.get_board.return_value = [[self.piece]]
        self.piece.get_clicked.return_value = True
        self.piece.get_num_around.return_value = 1
        self.piece.get_neighbors.return_value = [MagicMock(get_clicked=Mock(return_value=False), get_flagged=Mock(return_value=False))]
        self.piece.get_flagged.return_value = False

        with patch.object(self.solver, "open_unflagged") as mock_open, \
            patch.object(self.solver, "flag_all") as mock_flag:
            self.solver.move()
            mock_flag.assert_called_once()
            mock_open.assert_not_called()
    
    def test_open_unflagged(self):
        neighbors = [self.piece]
        self.piece.get_flagged.return_value = False
        self.solver.open_unflagged(neighbors)
        self.board.handle_click.assert_called_with(self.piece, False)
    
    def test_flag_all(self):
        neighbors = [self.piece]
        self.piece.get_flagged.return_value = False
        self.solver.flag_all(neighbors)
        self.board.handle_click.assert_called_with(self.piece, True)
    
    def test_skip_unclicked_pieces(self):
        self.board.get_board.return_value = [[self.unclicked_piece, self.clicked_piece]]
        self.clicked_piece.get_num_around.return_value = 1
        self.clicked_piece.get_neighbors.return_value = [self.unclicked_piece]
        self.solver.move()

        self.unclicked_piece.get_num_around.assert_not_called()
        self.unclicked_piece.get_neighbors.assert_not_called()
        self.clicked_piece.get_num_around.assert_called_once()
        self.clicked_piece.get_neighbors.assert_called_once()

if __name__ == "__main__":  # pragma: no cover
    unittest.main()