from models import Base, session, Book, engine

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
    print('Hello')
    Base.metadata.create_all(engine)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
