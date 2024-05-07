from typing import Dict, Optional
from advancedsolver import AdvancedSolver
from trivialsolver import TrivialSolver
from board import Board


class SolverInterface:
    def __init__(self, board: Board) -> None:
        """
        Initialize the Solver Interface.
        Dictionary to hold different solver instances
        """
        self.board: Board = board
        self.solvers: Dict[str, AdvancedSolver | TrivialSolver] = {
            # Initialize TrivialSolver instance
            'trivial': TrivialSolver(board),
            # Initialize AdvancedSolver instance
            'advanced': AdvancedSolver(board)
        }
        # Currently selected solver (starts empty)
        self.current_solver: Optional[AdvancedSolver | TrivialSolver] = None

    def get_flags_placed(self) -> int:
        """ Get the number of flags placed by the current solver. """
        if self.current_solver is not None:
            print("INTERFACE FLAGS_PLACED = "
                  + f"{self.current_solver.flags_placed}")
            return self.current_solver.flags_placed
        else:
            return 0

    def set_solver(self, solver_key: str) -> None:
        """
        Set the current solver based on the provided key.
        solver_key (str): Key to select the solver (if it's in the dict)
        """
        # Change the solver based on the key provided
        if solver_key in self.solvers:
            self.current_solver = self.solvers[solver_key]
            print(f"Switched to {solver_key} solver.")
        else:
            raise ValueError(f"No solver found for key: {solver_key}")

    def solve(self) -> None:
        """ Delegate the solve method to the current solver. """
        if self.current_solver is not None:
            # Call solve method of appropriate strategy
            self.current_solver.solve()
        else:
            raise ValueError("No solver is set.")
