import unittest
from unittest.mock import MagicMock
from hypothesis import given, strategies as st  # type: ignore
from solverstrategy import SolverStrategy


class ConcreteSolver(SolverStrategy):
    def solve(self) -> None:
        return "Solving the puzzle!"  # type: ignore


class TestSolverStrategy(unittest.TestCase):
    def test_concrete_solver_instantiation(self) -> None:
        solver = ConcreteSolver()
        self.assertIsInstance(solver, SolverStrategy)

    def test_concrete_solver_solve_method(self) -> None:
        solver = ConcreteSolver()
        result = solver.solve()  # type: ignore
        self.assertEqual(result, "Solving the puzzle!",
                         "The solve method should return the correct string.")

    @given(st.integers())  # type: ignore
    def test_solve_with_random_input(self, input: str) -> None:
        solver = ConcreteSolver()
        solver.solve = MagicMock(  # type: ignore
            return_value=f"Solving with input {input}")
        result = solver.solve()
        self.assertEqual(result, f"Solving with input {input}")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
