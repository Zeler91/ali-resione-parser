import sqlite3
from logconfig import logger

DB_PATH = './data/resin.db'

def open_connection():
    global con, cur
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

def close_connection():
    con.close() 

def db_connection(func):
    def func_with_connection(*args):
        open_connection()
        data = func(*args)
        close_connection()
        return data
    return func_with_connection

def create_table(name:str, collums:tuple):
    try:
        cur.execute(f"CREATE TABLE {name}{collums}")
        logger.info(f"Table: '{name}' create successfull!")
    except(sqlite3.OperationalError):
        logger.info(f"Table: '{name}' already exist!")

def insert_data(name:str, data:list):
    values = ''
    data_index = 0
    while data_index < (len(data[0]) - 1):
        values += '?, '
        data_index += 1
    values += '?'
    if data:
        cur.executemany(f"INSERT INTO {name} VALUES({values})", data)
        logger.info(f'Data successfully insert into "{name}" table!')
    else:
        logger.warning(f'Empty data')

    con.commit()

@db_connection
def select_data(sql_request:str, verbose=True):
    recs = cur.execute(sql_request)
    row_list = []
    for row in recs:
        if verbose:
            print(row)
        row_list.append(row)
    if len(row_list) == 1:
        return row_list[0]
    else:
        return row_list


# open_connection()
# create_table('test_table', 'score', 'record', 'time')
# test_data = [(100, 150, 23), (77, 150, 44), (52, 150, 10)]
# insert_data('test_table', test_data)
# select_all_data('test_table')

# def close_connection():