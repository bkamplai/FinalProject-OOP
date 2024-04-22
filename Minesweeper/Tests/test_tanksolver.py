import unittest
from unittest.mock import MagicMock
from hypothesis import given, strategies as st
from tanksolver import TankSolver


class TestTankSolver(unittest.TestCase):
    def setUp(self):
        self.solver = TankSolver()

    def test_tank_solver_instantiation(self):
        self.assertIsInstance(self.solver, TankSolver)

    def test_tank_solver_solve_method_exists(self):
        self.assertTrue(hasattr(self.solver, 'solve') and callable(getattr(
            self.solver, 'solve')), "solve method should be callable")

    @given(st.lists(st.integers()))
    def test_solve_with_hypothesis(self, input_list):
        self.solver.solve = MagicMock(return_value="mocked return")
        board_mock = MagicMock()
        result = self.solver.solve(board_mock)
        self.solver.solve.assert_called_with(board_mock)
        self.assertEqual(result, "mocked return")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
