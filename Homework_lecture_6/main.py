# Homework for lecture 6
# Task 1: Assistance to the secretary

import sqlite3 as sq

documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


with sq.connect("database.db") as db:
    conn = db.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS directories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shelf VARCHAR(8),
        number VARCHAR(15) NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type VARCHAR(15),
        number VARCHAR(15) NOT NULL UNIQUE,
        name VARCHAR(30),
        FOREIGN KEY (number) REFERENCES directories (number)
    )
    """

    conn.executescript(query)

# Adding data by condition, use it at the FIRST START of the program
    # for doc in documents:
    #     conn.execute('INSERT INTO documents (type, number, name) VALUES (?,?,?)',
    #                  (doc['type'], doc['number'], doc['name']))

    # for shelf, docs in directories.items():
    #     if directories[shelf] != []:
    #         for doc in docs:
    #             conn.execute(
    #                 'INSERT INTO directories (shelf, number) VALUES (?,?)', (shelf, doc))
    #     else:
    #         conn.execute('INSERT INTO directories (shelf) VALUES (?)', shelf)


def conn_db(sql_query, *values):
    db = sq.connect('database.db')
    conn = db.cursor()
    try:
        conn.execute(sql_query, values)
    except sq.Error as e:
        print("Error:", e)
    finally:
        output = conn.fetchall()
        db.commit()
        db.close()
        return output


def check_doc(str_input):
    while True:
        value = str(input(str_input))
        if value == 'q':
            return value
        else:
            query = conn_db(
                'SELECT number FROM directories WHERE number = ?', value)
            if query == []:
                print('Указанного докумнета нет в базе')
            else:
                str_input = 'В базе уже есть такой документ, введите другой: '
                return value


def check_shelf(str_input):
    ''' The function checks the availability of shelves in directories.
    '''
    while True:
        value = str(input(str_input))
        if value == 'q':
            return value
        else:
            query = conn_db(
                'SELECT shelf FROM directories WHERE shelf = ?', value)
            if query == []:
                print('Указанной полки нет в базе')
            else:
                return value


def people_docs():
    '''The function outputs people or a shelf by document number.
    '''
    while True:
        usr_input = check_doc('Введите номер документа: ')
        if usr_input == 'q':
            return
        person = conn_db(
            'SELECT name FROM documents WHERE number = ?', usr_input)
        print(''.join(*person))


def shelf_docs():
    while True:
        usr_input = check_doc('Введите номер документа: ')
        if usr_input == 'q':
            return
        shelf = conn_db(
            'SELECT shelf FROM directories WHERE number = ?', usr_input)
        print('Документ лежит на полке № ' + ''.join(*shelf))


def list_docs():
    docs_documents = conn_db('SELECT type, number, name FROM documents')
    print('\n'.join(f'{" ".join(value)}' for value in docs_documents))
    doc_without_owner = conn_db(
        'select number from directories WHERE number is not null EXCEPT SELECT number from documents')
    print('Документы без реквезитов: ' + ''.join(*doc_without_owner))


def add_doc():
    ''' Adds a new document to the documents and to the directories,
    asking for its number, type, name of the owner and the number of the shelf
    on which it will be stored.
    '''
    while True:
        doc_type = input('Введите тип документа: ').lower()
        if doc_type == 'q':
            return
        doc_num = input('Введите номер документа: ')
        if doc_num == 'q':
            return
        owner_doc = input('Введите имя владельца: ').title()
        if owner_doc == 'Q':
            return
        num_shelf = check_shelf(
            'Введите номер полки на которой будет храниться документ: ')
        if num_shelf == 'q':
            return
        query = conn_db('SELECT number FROM documents WHERE number = ?', doc_num)
        if query == []:
            conn_db('INSERT INTO documents(type, number, name) VALUES(?, ?, ?)', doc_type, doc_num, owner_doc)
            conn_db('INSERT INTO directories(shelf, number) VALUES(?, ?)', num_shelf, doc_num)
            print('Документ добавлен.')
        else:
            query = conn_db('SELECT shelf FROM directories WHERE number = ?', doc_num)
            print('Такой документ уже лежит на полке: ' + ''.join(*query))


def delete_doc():
    while True:
        doc_num = check_doc(
            'Введите номер документа который хотите удалить: ')
        if doc_num == 'q':
            return
        conn_db('DELETE FROM directories WHERE number = ?', doc_num)
        conn_db('DELETE FROM documents WHERE number = ?', doc_num)
        print('Документ удален.')


def move_doc():
    doc_num = check_doc('Введите номер документа который хотите переместить: ')
    shelf = check_shelf('Введите конечную полку: ')
    conn_db('DELETE FROM directories WHERE number= ?', doc_num)
    conn_db('INSERT INTO directories (shelf, number) VALUES(?, ?)', shelf, doc_num)
    print(f'Документ перемещен на полку № {shelf}')
    return


def add_shelf():
    while True:
        new_shelf = input('Введите номер новой полки: ')
        if new_shelf == 'q':
            return
        query = conn_db('SELECT shelf FROM directories WHERE shelf = ?', new_shelf)
        if query == []:
            conn_db('INSERT INTO directories (shelf) VALUES (?)', new_shelf)
            print(f'Папка № {new_shelf} добавлена.')
            return
        else:
            print(f'Папка {new_shelf} уже сужествует')


def main():
    with open('commands.txt', 'r', encoding='utf-8') as file:
        print(file.read())
    while True:
        usr_cmd = input('Введите команду:')
        if usr_cmd == 'p':
            people_docs()
        elif usr_cmd == 's':
            shelf_docs()
        elif usr_cmd == 'l':
            list_docs()
        elif usr_cmd == 'ls':
            query = conn_db('SELECT shelf, number FROM directories WHERE number IS NOT NULL')
            print('\n'.join(f'{" ".join(value)}' for value in query))
        elif usr_cmd == 'a':
            add_doc()
        elif usr_cmd == 'd':
            delete_doc()
        elif usr_cmd == 'm':
            move_doc()
        elif usr_cmd == 'as':
            add_shelf()
        elif usr_cmd == 'q':
            break
        else:
            print('Введена неверная команда')


main()
