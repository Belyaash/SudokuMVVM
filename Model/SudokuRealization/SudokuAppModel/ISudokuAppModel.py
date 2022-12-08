import numpy

from Model.SudokuRealization.SudokuGameGridFactory.ISudokuGameGridFactory import ISudokuGameGridFactory
from Model.SudokuRealization.SudokuGridFactory.ISudokuGridFactory import ISudokuGridFactory


class ISudokuAppModel:
    solved_grid: numpy.array
    game_grid: numpy.array
    solved_grid_factory: ISudokuGridFactory
    game_grid_factory: ISudokuGameGridFactory

    def __init__(self, length_of_block=3) -> None:
        pass

    def new_game(self) -> None:
        pass

    def is_player_win(self) -> bool:
        pass

    def get_game_grid_cell_num(self, row, col) -> int:
        pass

    def get_game_grid_cell_is_const(self, row, col) -> bool:
        pass

    def get_solved_grid_cell(self, row, col) -> int:
        pass

    def set_cell_num(self, row, col, num) -> None:
        pass

    def is_game_grid_filled(self) -> bool:
        pass

    def set_difficulty(self, difficulty) -> None:
        pass

    def set_length_of_block(self, length):
        pass
