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


def people_or_shelf(usr_cmd):
    '''The function outputs people or a shelf by document number.
    '''
    while True:
        usr_input = check_doc('Введите номер документа: ')
        if usr_input == 'q':
            return
        if usr_cmd == 'p':
            for person in documents:
                if usr_input == person['number']:
                    print(person['name'])
        else:
            for shelf, docs in directories.items():
                if usr_input in docs:
                    print(f'Документ "{usr_input}" лежит на полке № {shelf}')


def list_docs():
    for person in documents:
        print(f'{list(person.values())[0]}' +
              ' '.join(f' "{text}"' for text in list(person.values())[1:]))


def check_shelf(str_input):
    ''' The function checks the availability of shelves in directories.
    '''
    while True:
        value = str(input(str_input))
        if value in directories.keys():
            return value
        elif value == 'q':
            return value
        else:
            print('Указанная полка не существует.')


def check_doc(str_input):
    while True:
        value = str(input(str_input))
        for document in documents:
            if value == document['number']:
                return value
        if value == 'q':
            return value
        else:
            print('Указанного документа нет в базе.')


def add_doc():
    ''' Adds a new document to the documents and to the directories,
    asking for its number, type, name of the owner and the number of the shelf
    on which it will be stored.
    '''
    while True:
        doc_type_num = input('Введите тип и номер документа: ').lower().split()
        if doc_type_num == ['q']:
            return
        owner_doc = input('Введите имя владельца: ').title()
        if owner_doc == 'Q':
            return
        num_shelf = check_shelf(
            'Введите номер полки на которой будет храниться документ: ')
        if num_shelf == 'q':
            return
        new_doc = {"type": doc_type_num[0],
                   "number": ' '.join(map(str, doc_type_num[1:])),
                   "name": owner_doc}
        if new_doc not in documents:
            documents.append(new_doc)
            directories[num_shelf].append(new_doc['number'])
            print('Документ добавлен.')
        else:
            for shelf, docs in directories.items():
                if str(doc_type_num[1:]) in docs:
                    print(f'Полка № {shelf}')
            print(f'Такой документ уже есть в базе и лежит на полке {shelf}')


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
                # directories[shelf] = list(filter(lambda i: i != doc_num, docs))
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


def main():
    with open('Homework_lecture_6/commands.txt', 'r') as file:
        print(file.read())
    while True:
        usr_cmd = input('Введите команду:')
        if usr_cmd == 'p' or usr_cmd == 's':
            people_or_shelf(usr_cmd)
        elif usr_cmd == 'l':
            list_docs()
        elif usr_cmd == 'ls':
            print(directories)
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
            print('Введена некоректная команда')


main()
