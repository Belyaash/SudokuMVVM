from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton

from ViewModel.MainViewModel import view_model


class MenuLayout(QWidget):
    def __init__(self):
        super(MenuLayout, self).__init__()
        main_layout = QGridLayout()

        difficulty_label = QLabel()
        difficulty_label.setGeometry(QtCore.QRect(0, 0, 120, 30))
        difficulty_label.setText("Select difficulty")
        main_layout.addWidget(difficulty_label)

        self.difficulty_combo_box = QtWidgets.QComboBox()
        self.difficulty_combo_box.setGeometry(QtCore.QRect(0, 30, 120, 30))
        self.difficulty_combo_box.addItems(["Easy", "Medium", "Hard"])
        self.__get_difficulty(view_model.difficulty)
        self.difficulty_combo_box.currentTextChanged.connect(self.__difficulty_changed)
        main_layout.addWidget(self.difficulty_combo_box)

        size_label = QLabel()
        size_label.setGeometry(QtCore.QRect(0, 70, 120, 30))
        size_label.setText("Select block")
        main_layout.addWidget(size_label)

        self.size_cb = QtWidgets.QComboBox()
        self.size_cb.setGeometry(QtCore.QRect(0, 100, 120, 30))
        self.size_cb.addItems(["2", "3"])
        self.size_cb.setCurrentText(view_model.len_of_side)
        self.size_cb.currentTextChanged.connect(self.__length_changed)
        main_layout.addWidget(self.size_cb)

        best_time_label = QLabel()
        best_time_label.setGeometry(QtCore.QRect(0, 140, 120, 30))
        best_time_label.setText("Best time")
        main_layout.addWidget(best_time_label)

        self.best_game_time = QLabel()
        self.best_game_time.setGeometry(QtCore.QRect(0, 170, 120, 30))
        self.best_game_time.setText(view_model.possible_best_time)
        main_layout.addWidget(self.best_game_time)

        self.setLayout(main_layout)

    def __difficulty_changed(self):
        res = 0
        if self.difficulty_combo_box.currentText() == "Medium":
            res = 1
        elif self.difficulty_combo_box.currentText() == "Hard":
            res = 2
        view_model.difficulty = res

    def __get_difficulty(self, difficulty):
        if view_model.difficulty == 0:
            self.difficulty_combo_box.setCurrentText("Easy")
        elif view_model.difficulty == 1:
            self.difficulty_combo_box.setCurrentText('Medium')
        else:
            self.difficulty_combo_box.setCurrentText('Hard')

    def __length_changed(self):
        view_model.len_of_side = self.size_cb.currentText()