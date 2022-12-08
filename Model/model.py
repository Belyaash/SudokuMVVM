from Model.SudokuRealization.SudokuAppModel.sudokuAppModel import SudokuAppModel
from Model.Time import Time, time_class


class Model:
    time: Time
    sudoku_model: SudokuAppModel

    def __init__(self, len_of_side):
        self.sudoku_model = SudokuAppModel(len_of_side)
        self.time = time_class

