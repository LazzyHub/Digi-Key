import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design
import os
import csv
import back

print(test)
class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.btnBrowse.clicked.connect(self.browse_folder)
        self.btnDescribe.clicked.connect(self.describe_csv)
        self.statusBar.showMessage('Choose .csv file')

    def set_combo(self):
        if self.linePath.text() != '':
            self.comboBox.clear()
            if self.linePath.text()[-4:] == '.csv':
                self.statusBar.showMessage('Ready to describe')
                self.btnDescribe.setEnabled(True)
                with open(self.linePath.text(), 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    columns = next(reader)
                    self.comboBox.addItems(columns)
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
        path = self.linePath.text()
        column = self.comboBox.currentText()
        csv_output = path[0:-4] + '_described.csv'
        back.get_token()
        back.describe_list(path, column, csv_output)
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
