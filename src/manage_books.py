'''
Contains manage books class
- Allows advaned access/modification to books database
'''

import pandas as pd
from datetime import datetime, timedelta
from utils import Utils, GetID
from config import borrow_limit, return_days
#borrow limit sets how many book one person can borrow without returning
#return days sets after how many days due date will be

class ManageBooks:

    '''
    - View all books   - view all books in database, sorted by genre,author
    - View card        - allows you to view your library card and borrowed books, librarians can check of someone else also
    - Issue book       - allows you to issue a book, librarians can also do for someone else
    - Return book      - allows you to return a book, librarians can also do for someone else
    - Borrowed books   - shows all the details of all books borrowed and by who (librarian only)
    - Borrowed History - shows all the details of previously borrowed books which have been returned (librarian only)
    - Due books        - shows all the details of users,book who have not returned the book and its past due date (librarian only)
    - Add book         - Allows you to add a book (librarian only)
    - Remove book      - Allows you to remove a book (librarian only)
    '''

    def __init__(self, user, database):
        self.name = user.name
        self.email = user.email
        self.role = user.role
        self.id = user.id

        self.people = database.people
        self.borrowed = database.borrowed
        self.history = database.history
        self.books = database.books

        self.get_id = GetID(user, database)


    def view_all_books(self):
        '''
        prints list of all the books in database, sorted by genre,author along with their available,total copies 
        '''

        sorted_books = self.books.copy()
        sorted_books = sorted_books.sort_values(by=["Genre", "Author", "Book Name"])

        print("\nHere is a list of all the books :\n")
        print("ID", end="")
        print(sorted_books.loc[:, ["Genre", "Author", "Book Name", "Available", "Total"]])


    def view_card(self, targeted_id=None, ret=False):

        '''
        - You can display your own card or librarian can specify a target id (handled in main.py)
        - Displays id, email, role, joining date and borrowed books
        - variable is targeted_date not target_id to avoid conflicts when specifying this from other functions/methods
        '''

        if targeted_id is None:
            targeted_id = self.id

        targeted_email = self.people.loc[targeted_id, "Email"]
        targeted_role = self.people.loc[targeted_id, "Role"]
        targeted_name = self.people.loc[targeted_id, "Name"]
        targeted_date = self.people.loc[targeted_id, "Joined On"]

        print(f"\n{targeted_name}'s Library Card :\n")
        print(f"Name : {targeted_name}")
        print(f"User ID : {targeted_id}")
        print(f"Email : {targeted_email}")
        print(f"Role : {targeted_role}")
        print(f"Joined On : {targeted_date}")

        borrowed_books_df = Utils.print_borrowed(self.borrowed, targeted_id)
        if ret:
            return borrowed_books_df


    def issue_book(self, target_id=None):
        '''
        - Shows the books you have borrowed
        - Librarians can specify a target id in main
        - Prevents borrowing if you have borrowed max books allowed
        - Asks for book name and rapidfuzz is used for matching
        - Checks if the user has already borrowed that book
        - Checks for book's availability
        '''

        if target_id is None:
            target_id = self.id
        

        #prints borrowed books by user and stores info in dataframe
        borrowed_books_df = Utils.print_borrowed(self.borrowed, target_id)

        if len(borrowed_books_df) >= borrow_limit:
            print(f"\nBooks borrow limit is {borrow_limit}. You cannot borrow more books without returning current ones.")
            return

        to_borrow = Utils.format_input("\nEnter the book name to borrow (or 'Cancel') : ", case="title")

        if to_borrow == "Cancel":
            print("\nCancelling issue book command.")
            return

        to_borrow = Utils.match_input(to_borrow, self.books["Book Name"].values)

        if to_borrow not in self.books.loc[:, "Book Name"].values:
            print("\nThis book does not exist.")
            return

        if to_borrow in borrowed_books_df["Book Name"].values:
            print("\nYou have already borrowed this book.")
            return

        if (self.books.loc[self.books["Book Name"] == to_borrow, "Available"].values) == 0:
            print("This book has no more copies left in library. All have been borrowed")
            return

        #prints info of book and confirms if user wants to borrow
        print("\nYou are about to isssue the following book :")
        print(f"Book Name : {to_borrow}")
        print(f"Book Author : {self.books.loc[self.books["Book Name"]== to_borrow,"Author"].values[0]}")
        print(f"Book Genre : {self.books.loc[self.books["Book Name"]== to_borrow,"Genre"].values[0]}")

        confirm = Utils.consent()

        if confirm:

            #modifying the books, borrowed database
            self.books.loc[self.books["Book Name"] == to_borrow,"Available"] -= 1

            self.borrowed.loc[self.history.index.max() + 1, :] = [
                self.people.loc[target_id, "Name"],
                to_borrow,
                target_id,
                self.books.loc[self.books["Book Name"] == to_borrow].index.values[0],
                datetime.strftime(datetime.today(), "%d-%m-%Y"),
                datetime.strftime(
                    datetime.today() + timedelta(days=return_days), "%d-%m-%Y"
                ),
            ]
            print("\nThis book has been successfully issued.")

        else:
            print("\nCancelling issue book command.")
            return


    def return_book(self, target_id=None):
        '''
        - Shows the books you have borrowed
        - Librarians can specify a target id in main
        - Asks for book name and rapidfuzz is used for matching
        - Checks if the user has borrowed that book
        '''

        if target_id is None:
            target_id = self.id

        #prints borrowed books by user and also stores in dataframe
        borrowed_books_df = Utils.print_borrowed(self.borrowed, target_id)

        to_return = Utils.format_input("\nEnter the book name to return (or 'Cancel') : ", case="title")

        if to_return == "Cancel":
            print("\nCancelling return book command.")
            return

        to_return = Utils.match_input(to_return, borrowed_books_df["Book Name"].values)

        if to_return not in self.books.loc[:, "Book Name"].values:
            print("\nThis book does not exist.")
            return

        if to_return not in borrowed_books_df["Book Name"].values:
            print("\nYou have not borrowed this book.")
            return

        print(f"\nAre you sure you want to return {to_return}?")
        confirm = Utils.consent()

        if confirm:
            
            #finds the row where user id and book name match
            row_index = self.borrowed[
                (self.borrowed["Book Name"] == to_return)
                & (self.borrowed["User ID"] == target_id)
            ].index.values[0]

            #extracts values from the row to to_list
            to_list = []
            for i in self.borrowed.loc[row_index:].values[0]:
                to_list.append(i)

            #return date is added
            to_list.append(datetime.strftime(datetime.today(), "%d-%m-%Y"))

            #if book is returned late, late return is set as True
            if datetime.strptime(to_list[-1], "%d-%m-%Y") > datetime.strptime(to_list[-2], "%d-%m-%Y"):
                to_list.append(True)
            else:
                to_list.append(False)

            #books,borrowed and book history are updated
            self.books.loc[self.books["Book Name"] == to_return,"Available"] += 1
            self.history.loc[row_index, :] = to_list
            self.borrowed.drop(row_index, inplace=True)
            print("\nThe book has been successfully returned")

        else:
            print(f"\nCancelling return book command")
            return


    def borrowed_books(self):

        '''
        - Prints all of the borrowed books which have not been returned
        '''

        print("\nAll Borrowed Books:\n")
        print(self.borrowed)


    def borrowed_history(self, target_id=None):

        '''
        - Shows all of the borrowed books which have been returned 
        - You can also view for a specific user only
        '''

        if target_id == None:
            target_id = self.id

        print("\nBorrowed Books History (doesn't include non-returned books) :\n")


        if target_id == "all":
            print(self.history)

        else:
            if len(self.history[self.history["User ID"] == target_id]) > 0:
                print(self.history[self.history["User ID"] == target_id])
            else:
                print("You have never borrowed any books.")


    def due_books(self):

        '''
        - Prints all of the borrowed books which have not been returned and are also due
        '''

        due_books = self.borrowed.copy()

        due_books["Due On"] = pd.to_datetime(due_books["Due On"], format="%d-%m-%Y")
        due_books = due_books[due_books["Due On"] < datetime.today()]
        due_books["Due On"] = due_books["Due On"].dt.strftime("%d-%m-%Y")

        print("\nDue Books:\n")
        print(due_books)


    def add_book(self):

        '''
        - Allows you to add a book
        - Warns if books with similar names exist
        - Asks for genre, author, total
        '''

        to_add = Utils.format_input("Enter the name of book to add : ", case="title")

        if to_add == "Cancel":
            print("\nCancelling add book command.")
            return

        to_add = Utils.match_input(to_add, self.books["Book Name"].values)

        #if book with exact same name exists, function is cancelled/returned and book's details are displayed
        if to_add in self.books["Book Name"].values:
            print("\nThis book already exists.")
            print(self.books[self.books["Book Name"] == to_add])
            return

        book_qty = Utils.format_input("Enter the total number of copies available : ", typ="int", mini=1)

        #rapidfuzz matching of author and genre
        book_author = Utils.format_input("Enter the author of this book : ", case="title")
        book_author = Utils.match_input(book_author, self.books["Author"].drop_duplicates().values)

        book_genre = Utils.format_input("Enter the genre of this book : ", case="title")
        book_genre = Utils.match_input(book_genre, self.books["Genre"].drop_duplicates().values)

        #bid means a new generated book id
        bid = self.get_id.create_bid

        #prints details of book and confirms if to add it
        print("\nYou are about to add a book with following details:")
        print(f"Book ID : {bid}")
        print(f"Book Name : {to_add}")
        print(f"Author : {book_author}")
        print(f"Genre : {book_genre}")
        print(f"Total Copies : {book_qty}")

        confirm = Utils.consent()

        if confirm:
            self.books.loc[bid, :] = [
                to_add,
                book_author,
                book_genre,
                book_qty,
                book_qty,
            ]
            print("\nThis book has been successfully added.")

        else:
            print("\nCancelling add book command.")
            return
        

    def remove_book(self):

        '''
        - Allows you to remove a book by name
        - Rapidfuzz matches the book name
        - Checks if book exists
        '''

        to_remove = Utils.format_input("Enter the name of book to remove : ", case="title")

        if to_remove == "Cancel":
            print("\nCancelling remove book command.")
            return

        to_remove = Utils.match_input(to_remove, self.books["Book Name"].values)

        #if book doesnt exist, function is returned/exited
        if to_remove not in self.books["Book Name"].values:
            print("\nThis book does not exist.")
            return

        #details of book to be deleted and confirmation
        print("\nYou are about to delete :")
        print(self.books[self.books["Book Name"] == to_remove])

        confirm = Utils.consent()
        if confirm:
        
            self.books.drop(
                self.books[self.books["Book Name"] == to_remove].index[0], inplace=True
            )
            print("\nThis book has been successfully removed.")

        else:
            print("\nCancelling remove book command.")
            return