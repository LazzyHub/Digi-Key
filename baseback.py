import csv
import back
import json


def add_to_base(element, value, units):
    if element == 'Резистор':
        path = 'Chip_Resistor_-_Surface_Mount.csv' #r'C:\Users\Public\Documents\Altium\Pcblibraries\Altium\Chip_Resistor_-_Surface_Mount.csv'
        resistance = value
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            dict_headers = {}
            for header in headers:
                dict_headers[header] = ''

        if units == 'Ohm':
            resistance_str = resistance.split('.')
            try:
                res_code = str(resistance_str[0]) + 'R' + str(resistance_str[1])
            except IndexError:
                res_code = str(resistance_str[0]) + 'R'
            part_number = 'RC0805FR-07%sL' % res_code
            try:
                response = back.product_description(part_number)
            except IndexError:
                raise ValueError('Такого номинала не существует')
            dict_headers['Comment'] = resistance
        elif units == 'kOhm':
            resistance_str = str(resistance).split('.')
            try:
                res_code = str(resistance_str[0]) + 'K' + str(resistance_str[1])
            except IndexError:
                res_code = str(resistance_str[0]) + 'K'
            part_number = 'RC0805FR-07%sL' % res_code
            try:
                response = back.product_description(part_number)
            except IndexError:
                raise ValueError('Такого номинала не существует')
            dict_headers['Comment'] = res_code.lower()

        dict_headers['Part Number'] = part_number
        dict_headers['Manufacturer'] = response['ManufacturerName']['Text']
        dict_headers['Identifier'] = dict_headers['Manufacturer'] + '_' + dict_headers['Part Number']
        dict_headers['Description'] = response['ProductDescription']
        dict_headers['Library Ref'] = 'Resistor'
        dict_headers['Library Path'] = 'Resistors/Chip_Resistor_-_Surface_Mount/Resistor.SchLib'
        dict_headers['Footprint Ref'] = 'RESC200X125X60L35N'
        dict_headers['Footprint Path'] = 'Resistors/Chip_Resistor_-_Surface_Mount/RESC200X125X60L35N.PcbLib'
        dict_headers['Supplier 1'] = 'Digi-Key'
        dict_headers['Supplier Part Number 1'] = response['DigiKeyPartNumber']
        dict_headers['ComponentLink1Description'] = 'Datasheet'
        dict_headers['ComponentLink1URL'] = response['PrimaryDatasheet']
        dict_headers['HelpURL'] = response['PrimaryDatasheet']
        dict_headers['Resistance'] = dict_headers['Comment']
        dict_headers['Tolerance'] = '1,00%'
        dict_headers['Power'] = '0.125W'
        dict_headers['Package'] = '0805'
        dict_headers['Supplier 2'] = 'ChipDip'
        dict_headers['Supplier 3'] = 'Terraelectronica'
        dict_headers['Supplier 4'] = 'Platan'
        dict_headers['Supplier 5'] = 'Mouser'
        dict_headers['Supplier 6'] = 'Farnell'
        dict_headers['Supplier 7'] = 'Brownbear'
        dict_headers['Supplier 8'] = 'Aliexpress'

        with open(path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=dict_headers.keys())
            writer.writerow(dict_headers)

    elif element == 'Конденсатор':
        path = 'Ceramic_Capacitors.csv' #r'C:\Users\Public\Documents\Altium\Pcblibraries\Altium\Ceramic_Capacitors.csv'
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            dict_headers = {}
            for header in headers:
                dict_headers[header] = ''

        if units == 'pF':
            extra_zeros = 0
        elif units == 'nF':
            extra_zeros = 3
        value_zeros = 0
        i = 10
        value = int(value)
        while i <= value:
            if value % i == 0:
                value_zeros += 1
            i *= 10
        if value_zeros != 0:
            value_code = str(value/value_zeros*10) + str(value_zeros + extra_zeros)
        else:
            value_code = str(value) + str(value_zeros + extra_zeros)
        part_number = 'CC0805JRX7R9BB%s' % value_code
        try:
            response = back.product_description(part_number)
        except IndexError:
            raise ValueError('Такого номинала не существует')
        dict_headers['Comment'] = str(value) + units[:-1] + ' 50V'
        dict_headers['Part Number'] = part_number
        dict_headers['Manufacturer'] = response['ManufacturerName']['Text']
        dict_headers['Identifier'] = dict_headers['Manufacturer'] + '_' + dict_headers['Part Number']
        dict_headers['Description'] = response['ProductDescription']
        dict_headers['Library Ref'] = 'Ceramic capacitor'
        dict_headers['Library Path'] = 'Capacitors/Ceramic_Capacitors/Ceramic_Capacitor.SchLib'
        dict_headers['Footprint Ref'] = 'CAPC200X125X60L35N'
        dict_headers['Footprint Path'] = 'Capacitors/Ceramic_Capacitors/CAPC200X125X60L35N.PcbLib'
        dict_headers['Supplier 1'] = 'Digi-Key'
        dict_headers['Supplier Part Number 1'] = response['DigiKeyPartNumber']
        dict_headers['ComponentLink1Description'] = 'Datasheet'
        dict_headers['ComponentLink1URL'] = response['PrimaryDatasheet']
        dict_headers['HelpURL'] = response['PrimaryDatasheet']
        dict_headers['Capacitance'] = str(value) + units[:-1]
        dict_headers['Tolerance'] = response['Parameters'][3]['Value']
        dict_headers['Voltage'] = '50V'
        dict_headers['Temperature Coefficient'] = 'X7R'
        dict_headers['Package'] = '0805'
        dict_headers['Supplier 2'] = 'ChipDip'
        dict_headers['Supplier 3'] = 'Terraelectronica'
        dict_headers['Supplier 4'] = 'Platan'
        dict_headers['Supplier 5'] = 'Mouser'
        dict_headers['Supplier 6'] = 'Farnell'
        dict_headers['Supplier 7'] = 'Brownbear'
        dict_headers['Supplier 8'] = 'Aliexpress'

        with open(path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=dict_headers.keys())
            writer.writerow(dict_headers)

# element = 'Конденсатор'
# resistance = '1'
# units = 'pF'
# add_to_base(element, resistance, units)