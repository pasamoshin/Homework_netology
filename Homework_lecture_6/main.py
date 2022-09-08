# Homework for lecture 6
# Task 1: Assistance to the secretary

print('Task 1: Assistance to the secretary')

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


def people_num_doc():
    pass


def main():
    with open('Homework_lecture_6/commands.txt', 'r') as file:
        print(file.read())
    while True:
        usr_cmd = input('Введите команду:')
        if usr_cmd == 'p':
            pass
        elif usr_cmd == 's':
            pass
        elif usr_cmd == 'l':
            pass
        elif usr_cmd == 'a':
            pass
        elif usr_cmd == 'd':
            pass
        elif usr_cmd == 'm':
            pass
        elif usr_cmd == 'as':
            pass
        elif usr_cmd == 'q':
            break
        else:
            print('Введена некоректная команда')


main()
