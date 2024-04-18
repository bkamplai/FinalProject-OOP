from advancedsolver import AdvancedSolver
from trivialsolver import TrivialSolver

class SolverInterface:
    def __init__(self, board):
        """
        Initialize the Solver Interface.
        Dictionary to hold different solver instances
        """
        self.board = board
        self.solvers = {
            'trivial' : TrivialSolver(board), # Initialize TrivialSolver instance
            'advanced' : AdvancedSolver(board) # Initialize AdvancedSolver instance
        }
        self.current_solver = None # Currently selected solver (starts empty)
    
    def get_flags_placed(self):
        """ Get the number of flags placed by the current solver. """
        if self.current_solver is not None:
            print(f"INTERFACE FLAGS_PLACED = {self.current_solver.flags_placed}")
            return self.current_solver.flags_placed
        else:
            return 0

    def set_solver(self, solver_key):
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
    
    def solve(self):
        """ Delegate the solve method to the current solver. """
        if self.current_solver is not None:
            self.current_solver.solve() # Call solve method of appropriate strategy
        else:
            raise ValueError(f"No solver is set.")