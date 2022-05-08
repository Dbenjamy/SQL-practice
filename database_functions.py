import sqlite3 as sql
import pandas as pd

def _get_column_names(cursor,table_name):
    return ([x[0] for x in cursor
        .execute(f"""SELECT * FROM {table_name}""")
        .description])

def _get_table_length(cursor,table_name):
    return len(cursor.execute(f'SELECT * from {table_name}').fetchall())

def _fill_values(names):
    new_entry = []
    print('Provide the following.\n/skip to skip a value, /back to cancel:')
    for name in names:
        item = input(f'{name}: ')
        if item == '/back':
            return None
        elif item == '/skip':
            new_entry.append(None)
        else:
            new_entry.append(item)
    return new_entry

def connect_to_database(path):
    return sql.connect(path)

def get_table_names(cursor,message='Which table?'):
    tables = [x[0] for x in cursor
    .execute("""SELECT name FROM sqlite_master  
        WHERE type='table'""")
    .fetchall()]
    if message is not None:
        print(message)
        for name in tables:
            print(f'> {name}')
        while True:
            choice = input('> ')
            # 'tables' is list of tuples, so access first element
            # for name of column
            if choice == '/back':
                return None
            elif choice not in tables:
                print('Enter valid name or cancel with /back.')
            else:
                return choice
    else:
        return tables

def import_data(connection,csv_name,entries=None):
    cursor = connection.cursor()
    choice = ''
    while True:
        choice = input('1 New table\n2 Append to existing table\n> ')
        if choice in ['1','2','/back']:
            break
        else:
            print('Choose 1, 2, or /back')
    table_name = ''
    if choice == '1':
        names = get_table_names(cursor,message=None)
        while True:
            table_name = input('Input new table name:\n> ')
            if table_name == '/back':
                return None
            elif table_name not in names:
                break
            print(f'Table "{table_name}" already exists.')
    elif choice == '2':
        table_name = get_table_names(cursor,'Which table would you like to append to?')
        if table_name == None:
            return None
    elif choice == '/back':
        return None
    
    if entries is not None:
        (pd.read_csv(csv_name,nrows=entries)
        .to_sql(table_name,connection, if_exists='append', index=False))
    else:
        (pd.read_csv(csv_name)
        .to_sql(table_name,connection, if_exists='append', index=False))

def add_entry(cursor):
    table_name = get_table_names(cursor)
    names = _get_column_names(cursor,table_name)
    new_entry = _fill_values(names)
    if new_entry == None:
        return None
    cursor.execute(f"""INSERT INTO {table_name}{tuple(names)}
        VALUES{tuple(new_entry)}""")

def remove_entry(cursor):
    table_name = get_table_names(cursor)
    if table_name is None:
        return None
    rowid = input('Entry Number: ')
    while True:
        if rowid.isnumeric():
            cursor.execute(f'DELETE FROM {table_name} WHERE rowid = {rowid}')
        elif rowid == '/back':
            return None
        else:
            print('Choose a valid number.')

def edit_entry(cursor):
    table_name = get_table_names(cursor)
    if table_name == None:
        return None
    names = _get_column_names(cursor,table_name)
    table_length = _get_table_length(cursor,table_name)
    rowid = ''
    while True:
        rowid = input(f'Input entry number (1-{table_length}): ')
        if rowid == '/back':
            return None
        # elif not rowid.isnumeric() or int(rowid) not in range(1,table_length+1):
        #     print(f'Entry key must be number between 1 and {table_length}.')   
        else:
            break
    print('Current Values:')
    entry = (cursor
        .execute(f'SELECT * FROM {table_name} WHERE rowid = {rowid}')
        .fetchall())
    print(pd.DataFrame.from_dict(zip(names,entry)))
    updates = _fill_values(names)
    if updates == None:
        return None
    item_pairs = zip(names,updates)
    updated_entry = [item for item in item_pairs if None not in item]
    updated_entry = ', '.join(
    [f"{name} = '{update}'" for name,update in updated_entry]
    )
    rowid = input('rowid> ')
    if rowid == '/back':
        return None
    cursor.execute(f'UPDATE {table_name} SET {updated_entry} WHERE rowid = {rowid}')

def query(cursor):
    # table_name = get_table_names(cursor,'Which table would you like to query?')
    # if table_name is not None:

    pass


def show_data(cursor,table_name,id_range=None,rows=5):
    if id_range is None:
        cursor.execute(f'SELECT rowid, * FROM {table_name}')
    else:
        cursor.execute(f"""SELECT rowid, * FROM {table_name}
        WHERE rowid BETWEEN {id_range[0]} and {id_range[1]}
        """)
    entries = cursor.fetchall()
    if id_range is None:
        for item in range(len(entries)):
            if item > rows:
                break
            print(entries[item])
    else:
        for item in entries:
            print(item)
