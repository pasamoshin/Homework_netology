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
    CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type VARCHAR(15),
        number VARCHAR(15) NOT NULL,
        name VARCHAR(30)
    );
    CREATE TABLE IF NOT EXISTS directories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shelf VARCHAR(8),
        number VARCHAR(15)
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


def check_shelf(str_input):
    ''' The function checks the availability of shelves in directories.
    '''
    while True:
        value = str(input(str_input))
        if value == 'q':
            return
        else:
            try:
                db = sq.connect('database.db')
                conn = db.cursor()
                conn.execute(
                    'SELECT number FROM directories WHERE number = ?', (value,))
                print((value,))
                print(conn.fetchone())
                if conn.fetchone() == None:
                    print('есть такой')
                else:
                    print('Указанного докумнета нет в базе')
                    return
            except sq.Error as e:
                print("Error:", e)
            finally:
                conn.close()
                db.close()


i = check_shelf('Введите документ: ')

# def check_doc(str_input):
#     while True:
#         value = str(input(str_input))
#         for document in documents:
#             if value == document['number']:
#                 return value
#         if value == 'q':
#             return value
#         for docs in directories.values():
#             if value in docs:
#                 print('Указанный документ просто валяется на полке')
#                 return value
#         else:
#             print('Указанного документа нет в базе.')


# def people_docs():
#     '''The function outputs people or a shelf by document number.
#     '''
#     while True:
#         usr_input = check_doc('Введите номер документа: ')
#         if usr_input == 'q':
#             return
#         for person in documents:
#             if usr_input == person['number']:
#                 print(person['name'])


# def shelf_docs():
#     while True:
#         usr_input = check_doc('Введите номер документа: ')
#         if usr_input == 'q':
#             return
#         for shelf, docs in directories.items():
#             if usr_input in docs:
#                 print(f'Документ "{usr_input}" лежит на полке № {shelf}')


# def list_docs():
#     for person in documents:
#         print(f'{list(person.values())[0]}' +
#               ' '.join(f' "{text}"' for text in list(person.values())[1:]))


# def add_doc():
#     ''' Adds a new document to the documents and to the directories,
#     asking for its number, type, name of the owner and the number of the shelf
#     on which it will be stored.
#     '''
#     while True:
#         doc_type = input('Введите тип документа: ').lower()
#         if doc_type == 'q':
#             return
#         doc_num = input('Введите номер документа: ')
#         if doc_num == 'q':
#             return
#         owner_doc = input('Введите имя владельца: ').title()
#         if owner_doc == 'Q':
#             return
#         num_shelf = check_shelf(
#             'Введите номер полки на которой будет храниться документ: ')
#         if num_shelf == 'q':
#             return
#         new_doc = {"type": doc_type,
#                    "number": doc_num,
#                    "name": owner_doc}
#         if new_doc not in documents:
#             documents.append(new_doc)
#             directories[num_shelf].append(new_doc['number'])
#             print('Документ добавлен.')
#         else:
#             for shelf, docs in directories.items():
#                 if doc_num in docs:
#                     print(f'Такой документ уже лежит на полке {shelf}')


# def delete_doc():
#     global documents, directories
#     while True:
#         doc_num = check_doc(
#             'Введите номер документа который хотите удалить: ')
#         if doc_num == 'q':
#             return
#         documents = list(filter(lambda i: i['number'] != doc_num, documents))
#         for shelf, docs in directories.items():
#             if doc_num in docs:
#                 directories[shelf].remove(doc_num)
#                 print('Документ удален')


# def move_doc():
#     global documents, directories
#     doc_num = check_doc('Введите номер документа: ')
#     destination_shelf = check_shelf('Введите конечную полку: ')
#     for shelf, docs in directories.items():
#         if doc_num in docs:
#             directories[shelf] = list(filter(lambda i: i != doc_num, docs))
#             for shelf, docs in directories.items():
#                 if destination_shelf == shelf:
#                     directories[shelf].append(doc_num)
#                     print(f'Документ перемещен на полку № {shelf}')
#                     return


# def add_shelf():
#     while True:
#         new_shelf = input('Введите номер новой папки: ')
#         if new_shelf == 'q':
#             return
#         if new_shelf not in directories:
#             directories[new_shelf] = []
#             print(f'Папка № {new_shelf} добавлена.')
#             return
#         else:
#             print(f'Папка {new_shelf} уже сужествует')


# def main():
#     with open('commands.txt', 'r', encoding='utf-8') as file:
#         print(file.read())
#     while True:
#         usr_cmd = input('Введите команду:')
#         if usr_cmd == 'p':
#             people_docs()
#         elif usr_cmd == 's':
#             shelf_docs()
#         elif usr_cmd == 'l':
#             list_docs()
#         elif usr_cmd == 'ls':
#             print(directories)
#         elif usr_cmd == 'a':
#             add_doc()
#         elif usr_cmd == 'd':
#             delete_doc()
#         elif usr_cmd == 'm':
#             move_doc()
#         elif usr_cmd == 'as':
#             add_shelf()
#         elif usr_cmd == 'q':
#             break
#         else:
#             print('Введена неверная команда')


# main()
