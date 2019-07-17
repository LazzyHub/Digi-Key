import xlrd
import csv

def csv_from_excel(input):
    wb = xlrd.open_workbook(input)
    sh = wb.sheet_by_index(0)
    your_csv_file = open('csv_file.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL, delimiter=';')

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

csv_from_excel('C:/Users/vmezin/Documents/Копия Вектор СВЧ ч.1.xlsx')