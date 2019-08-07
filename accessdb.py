import pyodbc


def db_index(part_number):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=\\SRV-ASK\ExchangeN\DataBase\БД.accdb'
        )
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    number = part_number
    while len(number) > 2:
        crsr.execute("select * from [All microchips] WHERE ([Название микросхемы] LIKE '%{}%' )".format(part_number))
        row = crsr.fetchone()
        if row:
            return row[5]
        else:
            number = number[:-1]
    return 'Not in Database'


def db_name(part_number):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=\\SRV-ASK\ExchangeN\DataBase\БД.accdb'
        )
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    number = part_number
    while len(number) > 2:
        crsr.execute("select * from [All microchips] WHERE ([Название микросхемы] LIKE '%{}%' )".format(part_number))
        row = crsr.fetchone()
        if row:
            return row[0]
        else:
            number = number[:-1]
    return 'Not in Database'
#
# part_number = 'ETC1-1T-2TR'
# print(db_name(part_number), db_index(part_number))
