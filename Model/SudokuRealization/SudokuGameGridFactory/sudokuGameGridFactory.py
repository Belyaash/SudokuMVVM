import copy
import random

import numpy

from Model.SudokuRealization.SudokuGameGridFactory.ISudokuGameGridFactory import ISudokuGameGridFactory
from Model.SudokuRealization.SudokuSolver.ISudokuSolver import ISudokuSolver
from Model.SudokuRealization.SudokuSolver.sudokuSolver import SudokuSolver
from Model.SudokuRealization.cell import Cell


class SudokuGameGridFactory(ISudokuGameGridFactory):
    difficulty: int
    game_grid: numpy.array
    __solved_grid: numpy.array
    __difficulty_of_game_grid: int
    __order_of_deletion: numpy.array
    length_of_block: int

    def __init__(self, difficulty: int = 50, length_of_block=3) -> None:
        self.length_of_block = length_of_block
        self.difficulty = difficulty

    def create_game_grid(self, grid) -> numpy.array:
        self.__solved_grid = grid
        self.__difficulty_of_game_grid = 0

        while self.__difficulty_of_game_grid < self.difficulty:
            self.__difficulty_of_game_grid = 0
            self.__create_order_of_deletion()
            self.__create_game_matrix()

        return self.__convert_num_matrix_to_cell_matrix(self.game_grid)

    def set_length_of_block(self, length):
        self.length_of_block = length

    def __create_order_of_deletion(self) -> None:
        order = list(range(self.length_of_block**4))
        random.shuffle(order)
        self.__order_of_deletion = numpy.array(order, dtype=int)

    def __create_game_matrix(self) -> None:
        self.game_grid = copy.deepcopy(self.__solved_grid)
        sudoku_solver: ISudokuSolver = SudokuSolver(self.game_grid, self.length_of_block)
        for pos_of_deletion in self.__order_of_deletion:
            if self.__difficulty_of_game_grid >= self.difficulty + 1:
                break
            row = pos_of_deletion // self.length_of_block ** 2
            col = pos_of_deletion % self.length_of_block ** 2
            temp = self.game_grid[row][col]
            self.game_grid[row][col] = 0
            self.__difficulty_of_game_grid += 1
            if sudoku_solver.is_grid_have_only_one_solution(row, col, temp) is False:
                self.game_grid[row][col] = temp
                self.__difficulty_of_game_grid -= 1

    def __convert_num_matrix_to_cell_matrix(self, grid) -> numpy.array:
        """
        convert matrix of ints to matrix of cells
        :param grid:
        :return: list[list[Cell]]
        """
        side = self.length_of_block**2
        new_grid = numpy.zeros((side, side), dtype=Cell)
        for i in range(side):
            for j in range(side):
                new_grid[i][j] = Cell(grid[i][j])

        return new_grid


# grid = GridFactory(4).create_new_grid()
# ss = SudokuGameGridFactory(140, 4)
# ss.create_game_grid(grid)