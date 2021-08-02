from models import Base, session, Book, engine
import csv
import datetime

def menu():
    while True:
        print('''
                \nPROGRAMMING BOOKS
                \r1) Add book
                \r2) View all books
                \r3) Search for book
                \r4) Book Analysis
                \r5) Exit''')
        choice = input("What would you like to do? ")
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
              \rPlease choose one of the options above.
              \rA number from 1-5.
              \rPress enter to try again. ''')

def clean_date(date_string):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    split_date = date_string.split(' ')
    month = int(months.index(split_date[0]) + 1)
    day = int(split_date[1][:-1])
    year = int(split_date[2])
    return datetime.date(year, month, day)


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            print(row)



def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            pass
            # add book
        elif choice == '2':
            pass
            # view books
        elif choice == '3':
            pass
            # search for a book
        elif choice == '4':
            pass
            # book analysis
        else:
            print('Goodbye')
            app_running = False
# import models
# main menu - add, search, analysis, exit, view
# add books to the database
# edit books
# delete books
# search books
# data cleaning
# loop runs program


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    clean_date('November 12, 2019')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
