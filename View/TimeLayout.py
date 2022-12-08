from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from ViewModel.MainViewModel import view_model


class TimeLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.current_time = QLabel()
        self.best_time = QLabel()

        first_container = QWidget()
        first = QHBoxLayout()
        first_container.setLayout(first)
        current_time_label = QLabel("Current time : ")
        self.current_time.setText(view_model.current_time)
        first.addWidget(current_time_label)
        first.addWidget(self.current_time)

        second_container = QWidget()
        second = QHBoxLayout()
        second_container.setLayout(second)
        best_time_label = QLabel("Best time : ")
        self.best_time.setText(view_model.best_time)
        second.addWidget(best_time_label)
        second.addWidget(self.best_time)

        self.layout.addWidget(first_container)
        self.layout.addWidget(second_container)

        self.setLayout(self.layout)
