import csv
import sys
import traceback
from os import remove

import xlrd
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

import back
from baseback import add_to_base


def csv_from_excel(input_):  # конвертируем xls в csv
    wb = xlrd.open_workbook(input_)  # открываем xls
    sh = wb.sheet_by_index(0)  # выбираем лист
    your_csv_file = open('csv_file.csv', 'w', encoding='utf-8', newline='')  # создаем временный файл
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL, delimiter=';')  # объект райтера для временного файла

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))  # построчно переписываем из xls в csv
    your_csv_file.close()  # закрываем временный файл


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.pathLabel = QLabel('Путь к таблице')
        self.columnLabel = QLabel('Название столбца с p/n')
        self.pathLine = QLineEdit()
        self.columnComboBox = QComboBox()
        self.describeBtn = QPushButton('Describe')
        self.browseBtn = QPushButton('Browse')
        self.progressBar = QProgressBar()
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.grid = QGridLayout()

        self.typeLabel = QLabel('Тип элемента')
        self.itemSelect = QComboBox()
        self.valueLabel = QLabel('Номинал')
        self.unitsLabel = QLabel('Единицы измерения')
        self.valueLine = QLineEdit()
        self.unitsComboBox = QComboBox()
        self.toBaseBtn = QPushButton('Добавить в базу')
        self.toBaseGrid = QGridLayout()

        self.initUI()
        self.browseBtn.clicked.connect(self.browse_folder)  # отработка нажатия кнопки Browse
        self.describeBtn.clicked.connect(self.describe_csv)  # отработка нажатия кнопки Describe
        self.statusBar().showMessage('Choose .csv or Excel file')  # инициализация статусбара
        self.itemSelect.currentTextChanged.connect(self.set_units)
        self.itemSelect.addItems(['Резистор', 'Конденсатор'])
        self.tabs.currentChanged.connect(self.set_statusbar)
        self.toBaseBtn.clicked.connect(self.add_to_base)

    def initUI(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("footer_company_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.describeBtn.setEnabled(False)
        self.layout.setSpacing(1)
        self.pathLine.setPlaceholderText("Путь к .csv или Excel файлу")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFormat("%p%")
        self.grid.setSpacing(10)
        self.grid.addWidget(self.pathLabel, 0, 0)
        self.grid.addWidget(self.pathLine, 1, 0)
        self.grid.addWidget(self.browseBtn, 1, 1)
        self.grid.addWidget(self.columnLabel, 2, 0)
        self.grid.addWidget(self.columnComboBox, 3, 0, 1, 2)
        self.grid.addWidget(self.describeBtn, 4, 0, 1, 2)
        self.grid.addWidget(self.progressBar, 5, 0, 1, 2)
        self.tabs.addTab(self.tab1, 'Перечень элементов')
        self.tabs.addTab(self.tab2, 'База элементов')
        self.toBaseGrid.addWidget(self.typeLabel, 0, 0)
        self.toBaseGrid.addWidget(self.itemSelect, 1, 0, 1, 2)
        self.toBaseGrid.addWidget(self.valueLabel, 3, 0)
        self.toBaseGrid.addWidget(self.unitsLabel, 3, 1)
        self.toBaseGrid.addWidget(self.valueLine, 3, 0, 2, 1)
        self.toBaseGrid.addWidget(self.unitsComboBox, 3, 1, 2, 1)
        self.toBaseGrid.addWidget(self.toBaseBtn, 5, 0, 1, 2)

        self.layout.setContentsMargins(10, 10, 10, 0)
        self.layout.addWidget(self.tabs)
        self.tab1.setLayout(self.grid)
        self.tab2.setLayout(self.toBaseGrid)
        self.grid.setContentsMargins(25, 5, 25, 20)

        self.resize(320, 300)
        # self.statusBar().showMessage('Choose .csv or Excel file')

        self.setWindowTitle('ASCParser')
        self.show()

    def add_to_base(self):
        self.statusBar().showMessage('Wait...')
        element = self.itemSelect.currentText()
        value = self.valueLine.text()
        units = self.unitsComboBox.currentText()
        try:
            add_to_base(element, value, units)
            self.statusBar().showMessage('Element added')
        except ValueError:
            self.statusBar().showMessage('Set different value')

    def browse_folder(self):  # функция выбора файла
        self.pathLine.clear()  # На случай, если в списке уже есть элементы
        path = QFileDialog.getOpenFileName(self, 'Выберите папку')
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к файлу

        if path:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.pathLine.setText(str(path[0]))  # добавить путь к файлу в строку
        self.set_combo()  # создание элементов комбобоква

    def describe_csv(self):  # описываемкомпоненты из csv
        global csv_path
        self.statusBar().showMessage('Processing...')
        path = self.pathLine.text()  # путь берем из строки пути
        column = self.columnComboBox.currentText()  # нужную колонку - выбранную в комбобоксе
        if path[-5:] == '.xlsx':  # описываем имя результирующего файла
            csv_output = path[0:-5] + '_described.csv'
        else:
            csv_output = path[0:-4] + '_described.csv'
        back.describe_list(csv_path, column, csv_output, self)  # делаем запросы по каждому пункту из выбранной колонки
        if path != csv_path:  # если csv файл был временный - удаляем его
            remove(csv_path)
        self.statusBar().showMessage(' '.join(['Done! Description in', csv_output]))  # показываем путь к результату

    def set_combo(self):  # создание элементов комбобокса
        global csv_path  # переменная пути к csv файлу (исходному или созданному из xls)
        if self.pathLine.text() != '':  # работаем только если строка пути не пустая
            self.columnComboBox.clear()
            if self.pathLine.text()[-4:] == '.csv':  # если выбран csv файл
                self.statusBar().showMessage('Ready to describe')
                self.describeBtn.setEnabled(True)  # активируем кнопку
                with open(self.pathLine.text(), 'r', encoding='utf-8') as file:  # открываем выбранный файл
                    reader = csv.reader(file, delimiter=';')  # объект ридера
                    columns = next(reader)  # читаем первую строку файла
                    self.columnComboBox.addItems(columns)  # создаем элементы комбобокса из первой строки
                csv_path = self.pathLine.text()  # переменная пути равна пути к выбранному файлу
            elif self.pathLine.text()[-4:] == '.xls' or self.pathLine.text()[-5:] == '.xlsx':  # если выбран Excel файл
                csv_from_excel(self.pathLine.text())  # конвертируем excel-файл во временный csv
                self.statusBar().showMessage('Ready to describe')
                self.describeBtn.setEnabled(True)  # активируем кнопку
                with open('csv_file.csv', 'r', encoding='utf-8') as file:  # открываем временный csv файл
                    reader = csv.reader(file, delimiter=';')
                    columns = next(reader)
                    self.columnComboBox.addItems(columns)
                csv_path = 'csv_file.csv'  # переменная пути ведет к временному файлу
            else:
                self.statusBar().showMessage('Not .csv or Excel file!')  # если выбран любой другой формат
                self.describeBtn.setEnabled(False)  # деактивируем кнопку

    def set_statusbar(self):
        if self.tabs.currentWidget() == self.tab1:
            self.statusBar().showMessage('Choose .csv or Excel file')
        else:
            self.statusBar().showMessage('')

    def set_units(self):
        self.unitsComboBox.clear()
        if self.itemSelect.currentText() == 'Резистор':
            self.unitsComboBox.addItems(['Ohm', 'kOhm'])
        elif self.itemSelect.currentText() == 'Конденсатор':
            self.unitsComboBox.addItems(['pF', 'nF'])

    def log_uncaught_exceptions(ex_cls, ex, tb):
        text = '{}: {}:\n'.format(ex_cls.__name__, ex)

        text += ''.join(traceback.format_tb(tb))

        print(text)
        QMessageBox.critical(None, 'Error', text)

        sys.exit()

    sys.excepthook = log_uncaught_exceptions


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
