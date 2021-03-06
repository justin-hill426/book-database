from models import Base, session, Book, engine
import csv
import datetime
import time


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


def submenu():
    while True:
        print('''
                \n1) Edit Book
                \r2) Delete Book
                \r3) Return to Main Menu''')
        choice = input("What would you like to do? ")
        if choice in ['1', '2', '3']:
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
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1][:-1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
              \n****** DATE ERROR ******
              \rThe date format should include a valid Month Day Year
              \rEx: January 13, 2003
              \rPress enter to try again.
              \r*************************''')
        return
    else:
        return return_date


def clean_price(price_string):
    try:
        price_float = float(price_string)
    except ValueError:
        input('''
                      \n****** PRICE ERROR ******
                      \rThe price should be a number without a currency symbol
                      \rEx: 10.66
                      \rPress enter to try again.
                      \r*************************''')
        return
    else:
        return int(price_float * 100)


def clean_id(id_string, id_options):
    try:
        book_id = int(id_string)
    except ValueError:
        input('''
                              \n****** ID ERROR ******
                              \rThe id should be a number.
                              \rPress enter to try again.
                              \r*************************''')
        return
    else:
        if book_id in id_options:
            return book_id
        else:
            input(f'''
                                          \n****** ID ERROR ******
                                          \r ID options: {id_options}
                                          \rThe id should be a number in the range of options.
                                          \rPress enter to try again.
                                          \r*************************''')
            return


def edit_check(column_name, current_value):
    print(f'\n**** EDIT {column_name} ****')
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value / 100}')
    elif column_name == 'Date':
        print(f'\rCurrent Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'\rCurrent Value: {current_value}')

    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to? ')

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none()
            if book_in_db is None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date (Ex: October 25, 2017): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex: 25.64): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print(f"{title} was added to the library")
            time.sleep(1.5)

        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.published_date}')
            input('\nPress enter to return to the main menu. ')
            # view books
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nId Options: {id_options}
                    \rBook id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id == id_choice).first()
            print(f'''
                \n{the_book.title} by {the_book.author}
                \r Published: {the_book.published_date}
                \r Price: ${the_book.price / 100}''')
            sub_choice = submenu()
            if sub_choice == '1':
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.published_date = edit_check('Date', the_book.published_date)
                the_book.price = edit_check('Price', the_book.price)
                session.commit()
                print('Book Updated!')
                time.sleep(1.5)

            elif sub_choice == '2':
                session.delete(the_book)
                session.commit()
                print('Book Deleted!')
                time.sleep(1.5)
            # search for a book
        elif choice == '4':
            # book analysis
            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like('%Python%')).count()
            print(f'''
            \n***** BOOK ANALYSIS *****
            \rOldest Book: {oldest_book}
            \rNewest Book: {newest_book}
            \rTotal Books: {total_books}
            \rBooks with the word \'Python\' in them: {python_books}''')
            input('\n Press enter to return to the main menu.')
        else:
            print('GOODBYE')
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
    add_csv()
    app()
