import database_functions as dbf

db_path = r'database.db'

if db_path is None:
    db_path = input('Path to database:\n>')
connection = dbf.connect_to_database(db_path)
cursor = connection.cursor()


while True:
    print('Select from the following (1-8):\n\
    1. Add Entry\n\
    2. Edit Entry\n\
    3. Import Data\n\
    4. Remove Entry\n\
    5. Explore Data\n\
    6. Query\n\
    7. Change Database\n\
    8. Commit Current Changes\n\
    9. Quit')
    option = 0
    while True:
        try:
            option = int(input('> '))
            if option in range(1,10):
                break
            print('Please input a valid number.')
        except ValueError:
            print('Please input a valid number.')

    # Add Entry
    if option == 1:
        table_name = dbf.get_table_names(cursor)
        dbf.add_entry(cursor,table_name)

    # Edit Entry
    elif option == 2:
        dbf.edit_entry(cursor)

    # Import Data
    elif option == 3:
        csv_name = input('Path to data file: ')
        entries = ''
        while True:
            entries = input('How many rows would you like to import?\n\
00 will import the whole file.\n>')
            if entries == '/back':
                break
            elif entries == '00':
                dbf.import_data(connection,csv_name)
                break
            elif not entries.isnumeric():
                print('Please enter a valid number.')
            else:
                entries = int(entries)
                dbf.import_data(connection,csv_name,entries=int(entries))
                break

    # Remove Data
    elif option == 4:
        choice = None
        while True:
            choice = input('Table entry or table? (1-3)\n1 Table Entry\n2 Table\n/back (cancel)\n>  ').lower()
            if choice in ['1','2','/back']:
                break
            print('Choose valid option.')
        if choice == '1':
            dbf.remove_entry(cursor)
        elif choice == '2':
            table_name = dbf.get_table_names(cursor)
            cursor.execute(f'DROP TABLE {table_name}')
        elif choice == '/back':
            pass
        else:
            print('Something went wrong.')

    # Explore Data
    elif option == 5:
        table_name = dbf.get_table_names(cursor,'Which would you like to explore?')
        if table_name is not None:
            dbf.show_data(cursor,table_name)

    # Query
    elif option == 6:
        
        pass

    # Change Database
    elif option == 7:
        pass
    # Commit Current Changes
    elif option == 8:
        connection.commit()
    # Quit
    elif option == 9:
        connection.commit()
        connection.close()
        exit()