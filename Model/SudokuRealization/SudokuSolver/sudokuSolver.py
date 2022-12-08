import copy
import numpy

from Model.SudokuRealization.SudokuSolver.ISudokuSolver import ISudokuSolver
from Model.SudokuRealization.SudokuState import SudokuState


class SudokuSolver(ISudokuSolver):
    __grid: numpy.array
    __solutions = 0
    __row_of_unfilled_cell: int
    __col_of_unfilled_cell: int
    __solved_grid: numpy.array
    __length_of_block: int

    def __init__(self, grid_to_solve: numpy.array, length_of_block=3) -> None:
        self.set_grid(grid_to_solve)
        self.__length_of_block = length_of_block

    def set_grid(self, grid: numpy.array) -> None:
        self.__grid = grid

    def get_solved_grid(self):
        return self.__sudoku_solver(self.__grid)

    def set_length_of_block(self, length):
        self.__length_of_block = length

    def __sudoku_solver(self, state: numpy.ndarray) -> numpy.ndarray:
        """
        Solves the given sudoku, if there are empty cells.
        If there are no empty cells, an error grid is returned.
        :param state: 9x9 sudoku grid to solve
        :return: 9x9 solved sudoku grid, or error grid.
        """
        # Value to return if sudoku is unsolvable
        error = numpy.full((self.__length_of_block**2, self.__length_of_block**2), fill_value=-1)

        if numpy.count_nonzero(state == 0) == 0:
            return error

        # Make SudokuState with received array
        sudoku_state = SudokuState(state, self.__length_of_block)

        # Solve sudoku, if it appears to be solvable
        result = self.__backtrack(sudoku_state) if sudoku_state.solvable else None

        # Return result if valid
        return error if result is None else result.apply_solution()

    def __backtrack(self, state: SudokuState) -> SudokuState or None:
        """
        Solve sudoku using backtracking
        :param state: State to solve
        :return: Solved state
        """
        # Pick a constraint to satisfy
        const = state.pick_constraint()

        # No more constraints to satisfy
        if const is None:
            return None

        # List of satisfying RCV (row, column, value) tuples
        satisfying_rcvs = list(state.a[const])

        for rcv in satisfying_rcvs:
            # Add RCV to solutions, and save removed conflicting RCVs
            removed = state.add_solution(rcv)

            # Return this state if it's a goal
            if state.is_goal():
                return state

            # Continue trying this RCV
            deep_state = self. __backtrack(state)

            # Was a solution found?
            if deep_state is not None:
                return deep_state

            # This RCV doesn't lead to a solved sudoku

            # Remove RCV from solution and restore the matrix, so that we can try the next RCV
            state.remove_solution(rcv, removed)

    def is_grid_have_only_one_solution(self, row, col, num) -> bool:
        self.__solutions = 0
        self.__count_solutions(row, col, num)
        return self.__solutions == 0

    def __count_solutions(self, row, col, num) -> None:
        for i in range(1, self.__length_of_block**2):
            if self.__solutions > 0:
                return
            if i != num:
                grid = copy.deepcopy(self.__grid)
                if self.__is_safe(grid, row, col, i):
                    grid[row][col] = i
                    grid = self.__sudoku_solver(grid)
                    if grid[0][0] != -1:
                        self.__solutions += 1

    def __is_safe(self, grid, row, col, num) -> bool:
        start_row = row - row % self.__length_of_block
        start_col = col - col % self.__length_of_block
        for i in range(self.__length_of_block**2):
            if (grid[row][i] == num) or (grid[i][col] == num) \
                    or (grid[i // self.__length_of_block + start_row][i % self.__length_of_block + start_col] == num):
                return False
        return True


