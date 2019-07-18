import csv
import json
from accesstoken import get_access_token
from accesstoken import refresh_access_token
import requests
from time import sleep
NTDNCVS

def get_token():  # получаем токен доступа
    global access_token, refresh_token
    try:
        with open('tokens.txt', 'r') as f:   # пытаемся считать refresh token из файла с токенами
            refresh_token = f.readline().strip()
        tokens = refresh_access_token(refresh_token)  # получаем новый токен доступа с помощью refresh token
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
    except KeyError:  # если что-то пошло не так, получаем новый токен доступа с нуля
        tokens = get_access_token()
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
    except FileNotFoundError:  # если файла с токенами нет
        tokens = get_access_token()  # получаем новые токены
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
    with open('tokens.txt', 'w') as f:   # создаем файл и сохраняем токены там
        f.writelines([refresh_token+'\n', access_token])


def product_description(key):  # получаем описание компонента по названию
    url = 'https://api.digikey.com/services/partsearch/v2/keywordsearch'
    payload = {
              'Keywords': key,
              'RecordCount': '10'
              }

    headers = {
        'x-ibm-client-id': "df46fbf1-cbda-42a9-b7c9-2193b450b168",
        'authorization': access_token,
        'content-type': "application/json",
        'accept': "application/json"
        }

    res = requests.post(url, data=json.dumps(payload), headers=headers)  # запрос к API по переданному ключевому слову
    response = json.loads(res.content)   # получаем ответ в формате json
    n = 0
    while key in response['Parts'][n]['ProductDescription'] and n < 10:
        # если в описании компонента содержится название микросхемы - скорее всего это eval board для нее
        # поэтому ищем первый компонент без ключевого слова в описании
        n += 1
    return response['Parts'][n]  # возвращаем полное поисание этого компонента


def describe_list(path, column, csv_output, app, encoding='utf-8', delimiter=';'):  # описание списка компонентов из csv
    csv_file = open(path, "r", encoding=encoding)  # открываем выбранный ранее csv файл
    row_count = sum(1 for row in csv_file) - 1   # считаем количество компонентов(не считаем хэдер)
    csv_file = open(path, "r", encoding=encoding)  # снова открываем этот файл
    csv_reader = csv.DictReader(csv_file, delimiter=delimiter)  # объект ридера
    line_items = []
    queries = []
    progress = 0  # пременная состояния для прогрессбара
    progress_delta = 100/row_count  # сколько процентов всей работы составляет один компонент
    for line_item in csv_reader:  # прробегаемся по всем строкам
        if not line_item[column]:  # если выбранный столбец пустой - пропускаем
            continue
        line_items.append(line_item)  # объединяем строки в один список
        try:
            product = product_description(line_item[column])  # получаем описание элемента
            queries.append({'Part Number': line_item[column],  # парт намбер берем из таблицы
                            'Description': product['ProductDescription'],  # берем из описания нужные поля
                            'URL': 'https://www.digikey.com' + product['PartUrl'],
                            'Datasheet': product['PrimaryDatasheet'],
                            'Manufacturer': product['ManufacturerName']['Text']
                            })
        except IndexError:   # если в описании нет нужного поля - значит компонент не найден на сайте
            queries.append({'Part Number': line_item[column], 'Description': 'Not found'})
        progress += progress_delta   # считаем прогресс
        sleep(0.1)
        app.progressBar.setProperty("value", progress)  # обновляем прогрессбар
    app.progressBar.setProperty("value", 100)  # после обработки всего файла пробресс = 100%

    with open(csv_output, 'w', newline='', encoding=encoding) as csv_output:  # создаем файл для записи результата
        csv_writer = csv.DictWriter(csv_output, fieldnames=['Part Number', 'Manufacturer',  # названия столбцов
                                                            'Description', 'URL', 'Datasheet'], delimiter=delimiter)
        csv_writer.writeheader()  # записываем строку с названиями столбцов
        for i in range(len(queries)):   # для всех элементов
            row = {}  # строка которая будет записана
            for field in queries[i]:   # для всех сохраненных полей из описания
                row[field] = queries[i][field]  # значение поля записывается в соответствующий столбец
            csv_writer.writerow(row)  # запись строки в файл
