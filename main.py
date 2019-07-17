from sys import argv # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design
from os import remove
import csv
import back
import xlrd


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):


    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.btnBrowse.clicked.connect(self.browse_folder)
        self.btnDescribe.clicked.connect(self.describe_csv)
        self.statusBar.showMessage('Choose .csv or Excel file')


    def set_combo(self):
        global csv_path
        if self.linePath.text() != '':
            self.comboBox.clear()
            if self.linePath.text()[-4:] == '.csv':
                self.statusBar.showMessage('Ready to describe')
                self.btnDescribe.setEnabled(True)
                with open(self.linePath.text(), 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    columns = next(reader)
                    self.comboBox.addItems(columns)
                csv_path = self.linePath.text()
            elif self.linePath.text()[-4:] == '.xls' or self.linePath.text()[-5:] == '.xlsx':
                csv_from_excel(self.linePath.text())
                self.statusBar.showMessage('Ready to describe')
                self.btnDescribe.setEnabled(True)
                with open('csv_file.csv', 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    columns = next(reader)
                    self.comboBox.addItems(columns)
                csv_path = 'csv_file.csv'
            else:
                self.statusBar.showMessage('Not .csv file!')
                self.btnDescribe.setEnabled(False)

    def browse_folder(self):
        self.linePath.clear()  # На случай, если в списке уже есть элементы
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к файлу

        if path:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.linePath.setText(str(path[0]))  # добавить путь к файлу в строку
        self.set_combo()



    def describe_csv(self):
        global csv_path
        self.statusBar.showMessage('Processing...')
        path = self.linePath.text()
        column = self.comboBox.currentText()
        if path[-5:] == '.xlsx':
            csv_output = path[0:-5] + '_described.csv'
        else:
            csv_output = path[0:-4] + '_described.csv'
        back.get_token()
        back.describe_list(csv_path, column, csv_output, self)
        if path != csv_path:
            remove(csv_path)
        self.statusBar.showMessage('Done! Description in ' + csv_output)


def main():
    app = QtWidgets.QApplication(argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

def csv_from_excel(input):
    wb = xlrd.open_workbook(input)
    sh = wb.sheet_by_index(0)
    your_csv_file = open('csv_file.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL, delimiter=';')

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
