import numpy
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton
from PyQt5 import QtCore


class Digits(QDialog):

    def __init__(self, length_of_block=3):
        super().__init__()
        self.num = None
        self.setWindowTitle('Select a num')
        self.init_list_of_nums(length_of_block)
        self.init_ui(length_of_block)

    def init_list_of_nums(self, length_of_block):
        self.__digits = []
        for i in range(length_of_block ** 2):
            self.__digits.append(str(i + 1))

    def init_ui(self, length_of_block=3):
        main_layout = QGridLayout()
        font = QFont('Century', 14)

        positions = [(i, j) for i in range(length_of_block) for j in range(length_of_block)]

        for position, letter in zip(positions, self.__digits):
            btn = QPushButton(letter)
            btn.setFont(font)
            btn.clicked.connect(self.on_click)
            btn.setMaximumSize(QtCore.QSize(40, 40))
            main_layout.addWidget(btn, *position)

        empty_button = QPushButton()
        empty_button.setText("Empty")
        empty_button.setFont(font)
        empty_button.clicked.connect(self.on_click_empty)

        main_layout.addWidget(empty_button, length_of_block, 0, length_of_block, 0)

        self.setLayout(main_layout)

    def on_click(self):
        btn = self.sender()
        self.num = btn.text()
        self.close()

    def on_click_empty(self):
        self.num = '0'
        self.close()


