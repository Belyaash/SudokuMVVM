from PyQt5.QtWidgets import QApplication
import sys

from View.MainView import MainWindow

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
app.exec()
