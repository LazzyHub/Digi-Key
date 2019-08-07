import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
#from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout,
#                            QApplication, QComboBox, QPushButton, QProgressBar, QTabWidget, QVBoxLayout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        line = QLabel('qwerty')
        grid = QVBoxLayout()
        grid.addWidget(line)


        self.setWindowTitle('Test')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
