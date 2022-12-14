from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QPushButton, QLabel

from Model import model
from Model.model import Model, main_model
from View.MenuLayout import MenuLayout
from View.SetDigitsUI import Digits
from View.SudokuGridLayout import SudokuGridLayout
from View.TimeLayout import TimeLayout
from ViewModel.MainViewModel import view_model


class View(QWidget):
    is_in_menu: bool

    def __init__(self, window: QMainWindow):
        super().__init__()
        window.setCentralWidget(self)
        self.layout = QVBoxLayout()

        self.sudokuLayout = self.__create_grid()
        self.layout.addWidget(self.sudokuLayout)

        self.menuLayout = MenuLayout()
        # self.layout.addWidget(self.menuLayout)
        self.is_in_menu = False

        self.condition = QLabel()
        self.condition.setText(" ")
        self.condition.setStyleSheet("QLabel { background-color : #f0f0f0 }")
        self.layout.addWidget(self.condition)

        self.time_layout = TimeLayout()
        self.layout.addWidget(self.time_layout)

        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(main_model.new_game)
        self.layout.addWidget(new_game_button)

        self.menu_button = QPushButton("To menu")
        self.menu_button.clicked.connect(self.__open_close_menu)
        self.layout.addWidget(self.menu_button)

        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(main_model.sudoku_model.solve)
        self.layout.addWidget(self.solve_button)

        self.setLayout(self.layout)

        self.__open_close_menu()

        """current_time: str
        best_time: str
        possible_best_time: str"""

        view_model.on_change("grid", lambda x: self._refresh_grid())
        view_model.on_change("is_game_stopped", lambda x: self._refresh_condition())
        view_model.on_change("current_time", lambda x: self._refresh_current_time())
        view_model.on_change("best_time", lambda x: self._refresh_best_time())
        view_model.on_change("possible_best_time", lambda x: self._refresh_possible_best_time())


    def __create_grid(self):
        sudokuLayout = SudokuGridLayout(view_model.grid)
        for i in sudokuLayout.buttons:
            i.clicked.connect(self.__cell_clicked)
        return sudokuLayout

    def _refresh_grid(self):
        if self.is_in_menu:
            self.__open_close_menu()
        for btn in self.sudokuLayout.buttons:
            try:
                btn.destroy()
                btn.close()
            except:
                pass
        grid = self.__create_grid()
        self.layout.replaceWidget(self.sudokuLayout, grid)
        self.sudokuLayout.destroy()
        self.sudokuLayout = grid

    def _refresh_condition(self):
        if view_model.is_game_stopped:
            self.condition.setText("Sudoku is filled in correctly")
            self.condition.setStyleSheet("QLabel { background-color : green; color : blue; }")
        else:
            self.condition.setText("")
            self.condition.setStyleSheet("QLabel { background-color : #f0f0f0; color : blue; }")

    def __cell_clicked(self):
        if view_model.is_game_stopped:
            return

        button = self.sender()
        index = self.sudokuLayout.buttons.index(button)
        side = int(view_model.len_of_side) ** 2

        if not view_model.grid[index // side, index % side].isActive:
            return

        digit = self.__set_digit_dialog()
        if not digit:
            return

        main_model.sudoku_model.set_cell_num(index // side, index % side, int(digit))

    def __set_digit_dialog(self):
        window = Digits(int(view_model.len_of_side))
        window.exec()
        return window.num

    def __open_close_menu(self):
        if self.is_in_menu:
            self.layout.replaceWidget(self.menuLayout, self.sudokuLayout)
            self.sudokuLayout.show()
            self.menuLayout.close()
            self.condition.show()
            self.solve_button.show()
            self.menu_button.show()
        else:
            self.menuLayout = MenuLayout()
            self.sudokuLayout.close()
            self.condition.close()
            self.solve_button.close()
            if not view_model.is_grid_created:
                self.menu_button.close()
            self.layout.replaceWidget(self.sudokuLayout, self.menuLayout)
        self.is_in_menu = not self.is_in_menu

    def _refresh_current_time(self):
        self.time_layout.current_time.setText(view_model.current_time)

    def _refresh_best_time(self):
        self.time_layout.best_time.setText(view_model.best_time)

    def _refresh_possible_best_time(self):
        self.menuLayout.best_game_time.setText(view_model.possible_best_time)
