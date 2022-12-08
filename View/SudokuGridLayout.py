import math

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from Model.SudokuRealization.cell import Cell


class SudokuGridLayout(QWidget):
    # __digitsContainer: QWidget
    __layout = QVBoxLayout()
    buttons = []

    def __init__(self,grid):
        super().__init__()
        self.generate_grid(grid)
        self.setLayout(self.__layout)

    def generate_grid(self, grid):
        font = QFont('Baron Neue', 40//math.sqrt(len(grid)))
        size = QtCore.QSize(300//len(grid), 300//len(grid))
        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0,0,0,0)
        self.buttons = []
        _type = type(Cell(0))
        for row in range(int(len(grid))):
            h_container = QWidget()
            h_layout = QHBoxLayout()
            h_container.setLayout(h_layout)
            self.__layout.addWidget(h_container)
            for cell in range(int(len(grid))):
                button = QPushButton()
                button.setFixedSize(size)
                if (type(grid[row][cell]) == _type):
                    button.setStyleSheet(self.__get_style(row,cell,grid,grid[row][cell].isActive))
                    text = str(grid[row][cell].num)
                else:
                    button.setStyleSheet(self.__get_style(row,cell,grid, grid[row][cell] == 0))
                    text = str(grid[row][cell])
                if text == "0":
                    text = ""
                button.setText(text)
                button.setFont(font)
                h_layout.addWidget(button)
                self.buttons.append(button)

    def __get_style(self, row, cell, grid, isActive: bool):
        len_of_block = math.sqrt(len(grid))
        sum: int = int(row//len_of_block) + int(cell//len_of_block)

        style = ""
        if sum%2 == 0:
            style += """
                        QPushButton { background-color: white; border: 1px solid gray}
                     """

        if isActive:
            style += """
                        QPushButton:hover { border: 2px solid blue; }
                     """
        else:
            style += """
                        QPushButton {color: blue}
                        QPushButton:pressed { background-color: red; }
                     """

        return style