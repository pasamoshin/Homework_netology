# Homework for lecture 6
# Task 1: Assistance to the secretary

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


def check_shelf(str_input):
    ''' The function checks the availability of shelves in directories.
    '''
    while True:
        value = str(input(str_input))
        if value == 'q':
            return value
        elif value in directories.keys():
            return value
        else:
            print('Указанная полка не существует. Введите номер полки: ')


def check_doc(str_input):
    '''Checking the existence of a shelf.
    '''
    while True:
        value = str(input(str_input))
        for document in documents:
            if value == document['number']:
                return value
        if value == 'q':
            return value
        for docs in directories.values():
            if value in docs:
                print('Указанный документ просто валяется на полке')
                return value
        else:
            print('Указанного документа нет в базе.')


def people_docs():
    '''The function outputs people or a shelf by document number.
    '''
    while True:
        usr_input = check_doc('Введите номер документа: ')
        if usr_input == 'q':
            return
        for person in documents:
            if usr_input == person['number']:
                print(person['name'])


def shelf_docs():
    '''Search for a document on the shelves.
    '''
    while True:
        usr_input = check_doc('Введите номер документа: ')
        if usr_input == 'q':
            return
        for shelf, docs in directories.items():
            if usr_input in docs:
                print(f'Документ "{usr_input}" лежит на полке № {shelf}')


def list_docs():
    '''Showing all documents.
    '''
    for person in documents:
        print(f'{list(person.values())[0]}' +
              ' '.join(f' "{text}"' for text in list(person.values())[1:]))

    docs_dir = set(x for y in directories.values() for x in y)
    docs_doc = set()
    for person in documents:
        docs_doc.add(person['number'])
    docs_without_owner = docs_dir.difference(docs_doc)
    print("Документы без данных: ", *docs_without_owner)


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
        new_doc = {"type": doc_type,
                   "number": doc_num,
                   "name": owner_doc}
        if new_doc not in documents:
            documents.append(new_doc)
            directories[num_shelf].append(new_doc['number'])
            print('Документ добавлен.')
        else:
            for shelf, docs in directories.items():
                if doc_num in docs:
                    print(f'Такой документ уже лежит на полке {shelf}')


def delete_doc():
    global documents, directories
    while True:
        doc_num = check_doc(
            'Введите номер документа который хотите удалить: ')
        if doc_num == 'q':
            return
        documents = list(filter(lambda i: i['number'] != doc_num, documents))
        for shelf, docs in directories.items():
            if doc_num in docs:
                directories[shelf].remove(doc_num)
                print('Документ удален')


def move_doc():
    global documents, directories
    doc_num = check_doc('Введите номер документа: ')
    destination_shelf = check_shelf('Введите конечную полку: ')
    for shelf, docs in directories.items():
        if doc_num in docs:
            directories[shelf] = list(filter(lambda i: i != doc_num, docs))
            for shelf, docs in directories.items():
                if destination_shelf == shelf:
                    directories[shelf].append(doc_num)
                    print(f'Документ перемещен на полку № {shelf}')
                    return


def add_shelf():
    while True:
        new_shelf = input('Введите номер новой папки: ')
        if new_shelf == 'q':
            return
        if new_shelf not in directories:
            directories[new_shelf] = []
            print(f'Папка № {new_shelf} добавлена.')
            return
        else:
            print(f'Папка {new_shelf} уже сужествует')


def list_shelf():
    print(directories)
    return


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




input_dict = {'p': people_docs, 's': shelf_docs, 'l': list_docs,
              'ls': list_shelf, 'a': add_doc, 'd': delete_doc,
              'm': move_doc, 'as': add_shelf}


def user_choice():
    with open('commands.txt', 'r', encoding='utf-8') as file:
        print(file.read())

    y = True
    while y:
        choice = input('Введите команду:').lower()
        if choice == 'q':
            y = False
        elif choice not in input_dict:
            print('Введена неверная команда')
        else:
            input_dict[choice]()


user_choice()
