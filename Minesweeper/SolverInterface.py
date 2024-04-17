from advancedsolver import AdvancedSolver
from trivialsolver import TrivialSolver

class SolverInterface:
    def __init__(self, board):
        self.board = board
        self.solvers = {
            'trivial' : TrivialSolver(board),
            'advanced' : AdvancedSolver(board)
        }
        self.current_solver = None
    
    def get_flags_placed(self):
        if self.current_solver is not None:
            return self.current_solver.flags_placed
        else:
            return 0

    def set_solver(self, solver_key):
        # Change the solver based on the key provided
        if solver_key in self.solvers:
            self.current_solver = self.solvers[solver_key]
            print(f"Switched to {solver_key} solver.")
        else:
            raise ValueError(f"No solver found for key: {solver_key}")
    
    def solve(self):
        # Delegate the solve method to the current solver
        if self.current_solver is not None:
            self.current_solver.solve()
        else:
            raise ValueError(f"No solver is set.")