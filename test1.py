import csv

path = r'C:\Users\vmezin\Documents\Копия Вектор СВЧ ч.1.csv'
column = 'Номенклатура'
output = path[0:-4] + '_described.csv'

with open(path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    columns = next(reader)
    print(columns)