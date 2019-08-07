from sys import argv # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design
from os import remove
import csv
import back
import xlrd
from baseback import add_to_base
import sys
import traceback


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow, ):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.btnBrowse.clicked.connect(self.browse_folder)  # отработка нажатия кнопки Browse
        self.btnDescribe.clicked.connect(self.describe_csv)  # отработка нажатия кнопки Describe
        self.statusBar.showMessage('Choose .csv or Excel file')  # инициализация статусбара
        self.itemSelect.currentTextChanged.connect(self.set_units)
        self.itemSelect.addItems(['Резистор', 'Конденсатор'])
        self.tabWidget.currentChanged.connect(self.set_statusbar)
        self.toBaseBtn.clicked.connect(self.add_to_base)

    def add_to_base(self):
        self.statusBar.showMessage('Wait...')
        element = self.itemSelect.currentText()
        value = self.lineEdit.text()
        units = self.unitsBox.currentText()
        try:
            add_to_base(element, value, units)
            self.statusBar.showMessage('Element added')
        except ValueError:
            self.statusBar.showMessage('Set different value')



    def set_statusbar(self):
        if self.tabWidget.currentWidget() == self.describeTab:
            self.statusBar.showMessage('Choose .csv or Excel file')
        else:
            self.statusBar.showMessage('')

    def set_units(self):
        self.unitsBox.clear()
        if self.itemSelect.currentText() == 'Резистор':
            self.unitsBox.addItems(['Ohm', 'kOhm'])
        elif self.itemSelect.currentText() == 'Конденсатор':
            self.unitsBox.addItems(['pF', 'nF'])

    def set_combo(self):  # создание элементов комбобокса
        global csv_path  # переменная пути к csv файлу (исходному или созданному из xls)
        if self.linePath.text() != '':  # работаем только если строка пути не пустая
            self.comboBox.clear()
            if self.linePath.text()[-4:] == '.csv':  # если выбран csv файл
                self.statusBar.showMessage('Ready to describe')
                self.btnDescribe.setEnabled(True)  # активируем кнопку
                with open(self.linePath.text(), 'r', encoding='utf-8') as file:  # открываем выбранный файл
                    reader = csv.reader(file, delimiter=';')  # объект ридера
                    columns = next(reader)  # читаем первую строку файла
                    self.comboBox.addItems(columns)  # создаем элементы комбобокса из первой строки
                csv_path = self.linePath.text()  # переменная пути равна пути к выбранному файлу
            elif self.linePath.text()[-4:] == '.xls' or self.linePath.text()[-5:] == '.xlsx':  # если выбран Excel файл
                csv_from_excel(self.linePath.text())  # конвертируем excel-файл во временный csv
                self.statusBar.showMessage('Ready to describe')
                self.btnDescribe.setEnabled(True)  # активируем кнопку
                with open('csv_file.csv', 'r', encoding='utf-8') as file:  # открываем временный csv файл
                    reader = csv.reader(file, delimiter=';')
                    columns = next(reader)
                    self.comboBox.addItems(columns)
                csv_path = 'csv_file.csv'  # переменная пути ведет к временному файлу
            else:
                self.statusBar.showMessage('Not .csv or Excel file!')   # если выбран любой другой формат
                self.btnDescribe.setEnabled(False)                      # деактивируем кнопку

    def browse_folder(self):  # функция выбора файла
        self.linePath.clear()  # На случай, если в списке уже есть элементы
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к файлу

        if path:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.linePath.setText(str(path[0]))  # добавить путь к файлу в строку
        self.set_combo()  # создание элементов комбобоква

    def describe_csv(self):  # описываемкомпоненты из csv
        global csv_path
        self.statusBar.showMessage('Processing...')
        path = self.linePath.text()  # путь берем из строки пути
        column = self.comboBox.currentText()  # нужную колонку - выбранную в комбобоксе
        if path[-5:] == '.xlsx':          # описываем имя результирующего файла
            csv_output = path[0:-5] + '_described.csv'
        else:
            csv_output = path[0:-4] + '_described.csv'
        back.describe_list(csv_path, column, csv_output, self)  # делаем запросы по каждому пункту из выбранной колонки
        if path != csv_path:  # если csv файл был временный - удаляем его
            remove(csv_path)
        self.statusBar.showMessage(' '.join(['Done! Description in', csv_output]))  # показываем путь к результату


def main():
    app = QtWidgets.QApplication(argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


def csv_from_excel(input):   # конвертируем xls в csv
    wb = xlrd.open_workbook(input)  # открываем xls
    sh = wb.sheet_by_index(0)  # выбираем лист
    your_csv_file = open('csv_file.csv', 'w', encoding='utf-8', newline='')  # создаем временный файл
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL, delimiter=';')  # объект райтера для временного файла

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))  # построчно переписываем из xls в csv

    your_csv_file.close()   # закрываем временный файл


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)

    text += ''.join(traceback.format_tb(tb))

    print(text)
    QtWidgets.QMessageBox.critical(None, 'Error', text)

    sys.exit()


sys.excepthook = log_uncaught_exceptions

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
