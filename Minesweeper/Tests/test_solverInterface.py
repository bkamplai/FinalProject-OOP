import unittest
from unittest.mock import MagicMock
from hypothesis import given, strategies as st
from SolverInterface import SolverInterface


class TestSolverInterface(unittest.TestCase):
    def setUp(self):
        self.mock_board = MagicMock()
        self.solver_interface = SolverInterface(self.mock_board)

    def test_set_solver_valid_key(self):
        self.solver_interface.set_solver('trivial')
        self.assertIsNotNone(self.solver_interface.current_solver,
                             "Current solver should be set.")

    def test_set_solver_invalid_key(self):
        with self.assertRaises(ValueError):
            self.solver_interface.set_solver('invalid_key')

    @given(st.sampled_from(['trivial', 'advanced']))
    def test_set_solver_hypothesis(self, solver_key):
        self.solver_interface.set_solver(solver_key)
        self.assertIsNotNone(self.solver_interface.current_solver,
                             f"Solver should switch to {solver_key}.")

    def test_get_flags_placed_no_solver(self):
        flags = self.solver_interface.get_flags_placed()
        self.assertEqual(flags, 0, "Should return 0 when no solver is set.")

    def test_get_flags_placed_with_solver(self):
        self.solver_interface.set_solver('trivial')
        self.solver_interface.current_solver.flags_placed = 5
        flags = self.solver_interface.get_flags_placed()
        self.assertEqual(flags, 5, "Should return the number of flags placed \
                         by the current solver.")

    def test_solve_no_solver_set(self):
        with self.assertRaises(ValueError):
            self.solver_interface.solve()

    def test_solve_with_solver_set(self):
        self.solver_interface.set_solver('advanced')
        self.solver_interface.current_solver.solve = MagicMock()
        self.solver_interface.solve()
        self.solver_interface.current_solver.solve.assert_called_once()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
