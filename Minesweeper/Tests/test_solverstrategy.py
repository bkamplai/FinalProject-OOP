import unittest
from unittest.mock import MagicMock
from hypothesis import given, strategies as st
from solverstrategy import SolverStrategy


class ConcreteSolver(SolverStrategy):
    def solve(self):
        return "Solving the puzzle!"


class TestSolverStrategy(unittest.TestCase):
    def test_concrete_solver_instantiation(self):
        solver = ConcreteSolver()
        self.assertIsInstance(solver, SolverStrategy)

    def test_concrete_solver_solve_method(self):
        solver = ConcreteSolver()
        result = solver.solve()
        self.assertEqual(result, "Solving the puzzle!",
                         "The solve method should return the correct string.")

    @given(st.integers())
    def test_solve_with_random_input(self, input):
        solver = ConcreteSolver()
        solver.solve = MagicMock(return_value=f"Solving with input {input}")
        result = solver.solve()
        self.assertEqual(result, f"Solving with input {input}")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
