import numpy


class ISudokuSolver(object):
    def set_grid(self, grid: numpy.array) -> None:
        pass

    def get_solved_grid(self):
        pass

    def is_grid_have_only_one_solution(self, last_deleted_row, last_deleted_col, last_deleted_num) -> bool:
        pass

    def set_length_of_block(self, length):
        pass