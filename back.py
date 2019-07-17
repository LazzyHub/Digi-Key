import urllib.parse
import urllib.request
import csv
import json
from accesstoken import get_access_token
from accesstoken import refresh_access_token
import requests


def get_token():
    global access_token, refresh_token
    try:
        with open('tokens.txt', 'r') as f:
            refresh_token = f.readline().strip()
        tokens = refresh_access_token(refresh_token)
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
    except KeyError:
        tokens = get_access_token()
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
    except FileNotFoundError:
        tokens = get_access_token()
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
    with open('tokens.txt', 'w') as f:
        f.writelines([refresh_token+'\n', access_token])


def product_description(key):
    url = 'https://api.digikey.com/services/partsearch/v2/keywordsearch'
    payload = {
              'Keywords' : key,
              'RecordCount' : '10'
              }

    headers = {
        'x-ibm-client-id': "df46fbf1-cbda-42a9-b7c9-2193b450b168",
        'authorization': access_token,
        'content-type': "application/json",
        'accept': "application/json"
        }

    res = requests.post(url, data=json.dumps(payload), headers=headers)
    # print(res.status_code)
    # print(res.headers)

    # with open('response.json', 'wb') as f:
    #     f.write(res.content)
    response = json.loads(res.content)
    n = 0
    while key in response['Parts'][n]['ProductDescription'] and n < 10:
        n += 1
    return response['Parts'][n]#['ProductDescription']


def describe_list(path, column, csv_output, encoding='utf-8', delimiter=';'):
    csv_file = open(path, "r", encoding=encoding)
    csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
    line_items = []
    queries = []
    for line_item in csv_reader:
        # print(line_item)
        # Skip line items without part numbers and manufacturers
        if not line_item[column]:
            continue
        line_items.append(line_item)
        # queries.append(line_item[column])
        try:
            queries.append({'Part Number': line_item[column], 'Description' : product_description(line_item[column])['ProductDescription'],
                            'URL' : 'https://www.digikey.com' + product_description(line_item[column])['PartUrl'],
                            'Datasheet' : product_description(line_item[column])['PrimaryDatasheet'],
                            'Manufacturer' : product_description(line_item[column])['ManufacturerName']['Text']
                            })
        except IndexError:
            queries.append({'Part Number': line_item[column], 'Description' : 'Not found'})

    with open(csv_output, 'w', newline='', encoding=encoding) as csv_output:
        csv_writer = csv.DictWriter(csv_output, fieldnames=['Part Number', 'Manufacturer', 'Description', 'URL', 'Datasheet'], delimiter=delimiter)
        csv_writer.writeheader()
        for i in range(len(queries)):
            row = {}
            for field in queries[i]:
                row[field] = queries[i][field]
            csv_writer.writerow(row)
            #print(queries[i])


    #print(queries)

# path = 'csv_file.csv'
# column = 'Номенклатура'
# output = path[0:-4] + '_described.csv'
# get_token()
# describe_list(path, column, output)
# print(product_description('HMC520A'))

# csv_file = open(r"C:\Users\vmezin\Documents\Копия Вектор СВЧ ч.1.csv", "r")
# csv_reader = csv.DictReader(csv_file, delimiter=';')
# line_items = []
# queries = []
#
# for line_item in csv_reader:
#     #print(line_item)
#     # Skip line items without part numbers and manufacturers
#     if not line_item['Номенклатура']:
#         continue
#     line_items.append(line_item)
#     queries.append({'mpn': line_item['Номенклатура'],
#                     'reference': len(line_items) - 1})
#print(queries)
# results = []
# for i in range(0, len(queries), 20):
#     # Batch queries in groups of 20, query limit of
#     # parts match endpoint
#     batched_queries = queries[i: i + 20]
#
#     url = 'http://octopart.com/api/v3/parts/match?queries=%s' \
#         % urllib.parse.quote(json.dumps(batched_queries))
#     url += '&apikey=ca98523b97ecfd2dc98b'
#     data = urllib.request.urlopen(url).read()
#     response = json.loads(data)
#
#     # Record results for analysis
#     results.extend(response['results'])