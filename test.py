import csv
from back import product_description

csv_file = open(r"C:\Users\vmezin\Documents\Копия Вектор СВЧ ч.1.csv", "r", encoding='utf-8')
csv_reader = csv.DictReader(csv_file, delimiter=';')
line_items = []
queries = []

for line_item in csv_reader:
    #print(line_item)
    # Skip line items without part numbers and manufacturers
    if not line_item['Номенклатура']:
        continue
    line_items.append(line_item)
    #queries.append(line_item['Номенклатура'])
    try:
        queries.append({line_item['Номенклатура']: product_description(line_item['Номенклатура'])})
    except IndexError:
        queries.append({line_item['Номенклатура']: 'Not found'})
print(queries)

