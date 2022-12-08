from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton

from View.SudokuGridLayout import SudokuGridLayout
from View.View import View
from ViewModel.MainViewModel import MainViewModel, view_model


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        View(self)
        self.show()
        