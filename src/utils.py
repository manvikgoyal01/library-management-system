'''
Contains Utils class:
- various reusable static methods
Contains GetID class
- Validate ID, create unique person and book id
'''

import pandas as pd
import sys
from rapidfuzz import process, fuzz
from config import match_limit, match_cutoff
#match limit is how many max rapidfuzz matches you want user to see
#match cutoff is min match ratio

class Utils:
    '''
    - Col String     - Converts pandas column datatype to string and returns it
    - Format Input   - Formats input based on various parameters/options and returns formatted input
    - Validate ID    - Returns boolean value whether the user ID exists
    - Consent        - Return boolean value whether the user consents or not
    - Match Input    - Rapidfuzz matches a value in an iterable, returns oringal/corrected input
    - Print Borrowed - Prints the borrowed books of the user
    '''

    @staticmethod
    def col_string(database, col_name):

        '''
        - Convert pandas column datatype to string
        '''

        return database[col_name].astype("str")


    @staticmethod
    def format_input(prompt, case="lower", typ="str", mini=None, maxi=None, stop=None, ret=[]):

        '''
        - Formats the input based on various perimeters
        - Returns the formatted input or action word (cancel,stop,etc)

        - Prompt - The message in the input
        - Case   - Input is formatted to this case
        - typ    - typ = 'int' will try to convert input to int, only returns when integer is passed
        - mini   - The minimum value the integer can be (requires typ=int)
        - maxi   - The maximum value the integer can be (requires typ=int)
        - stop   - if input = stop, program exits without saving any changes to files
        - ret    - if input = return, the formatting stops and input is retuned
        '''

        while True:
            inp = input(f"\n{prompt}").strip()
            inp = getattr(inp, case)()

            if inp.lower() == stop:
                sys.exit("\nExiting...\n")

            if inp.lower() in ret:
                return inp

            if typ == "str":
                return inp
            
            #if typ is not integer, the function ends above

            elif typ == "int":

                try:
                    inp = int(inp)

                    #confirms if mini is not None and if input is greater than it, else retakes input
                    if mini is not None:
                        if inp < mini:
                            print(f"The number must be greater than {mini}")
                            continue
                    
                    #confirms if maxi is not None and if input is smaller than it, else retakes input
                    if maxi is not None:
                        if inp > maxi:
                            print(f"The number must be lower than {maxi}")
                            continue

                    #if all conditions of integer, maxi,mini are met, it returns int(input)
                    return inp

                except ValueError:
                    print("\nPlease enter a integer.")


    @staticmethod
    def validate_id(id, database):

        '''
        Returns boolean value of whether a user id exists
        '''

        if id in database.index:
            return True
        else:
            return False


    @staticmethod
    def consent(prompt="Please enter 'Yes'/'No' : "):

        '''
        - Displays the prompt and inputs whether the user consents or no
        - Best used with a print statement asking the question before calling it
        - Returns boolean value, True if user consents else False
        '''

        while True:
            inp = Utils.format_input(prompt)
            if inp == "yes":
                return True
            elif inp == "no":
                return False


    @staticmethod
    def match_input(inp, lst, caution="Please confirm if you meant any of the following :"):

        '''
        - Takes value (inp) and matches it in iterable (lst)
        - You can set match limit and score cutoff in config.py
        - Returns either orignal input or corrected input
        '''

        try:
            #try ensures that if process.extract returns empty, it doesnt lead to an error
            matching = process.extract(
                inp,
                lst,
                limit=match_limit,
                score_cutoff=match_cutoff,
                scorer=fuzz.token_sort_ratio,
            )

            if matching[0][1] >= 97:
                return matching[0][0]
            
            print(f"\n{caution}")

            #asks user if they meant <value> for <value,score,index> in the extract process list
            for i in matching:
                ask = Utils.consent(f"Did you mean {i[0]}? ('Yes'/'No') : ")
                if ask:
                    return i[0]
                
            #if user doesnt mean any of above, orignal input is returned
            return inp
        
        except:
            return inp


    @staticmethod
    def matching_list(inp, lst):

        '''
        - Upto match_limit no of results in the iterable (lst), similar to the input (inp) are returned
        - If none are matched, empty list is returned
        '''

        try:
            matching = process.extract(
                inp, lst, limit=match_limit, score_cutoff=match_cutoff, scorer=fuzz.token_sort_ratio
            )

            matching = [i[0] for i in matching]
            return matching
        
        except:
            return []


    @staticmethod
    def print_borrowed(borrowed_df, target_id):

        '''
        - Looks for the borrowed books of target_id in borrowed_df
        - Prints all of the borrowed books
        - Returns the books database with only target_id rows
        '''

        borrowed_books_df = borrowed_df[borrowed_df["User ID"] == target_id]
        borrowed_books = borrowed_books_df[["Book Name", "Due On"]].values

        print("\nBorrowed Books :")

        if len(borrowed_books) < 1:
            print("   None")

        else:
            print("Sno. Book Name  -  Due Date")

            for index, (book, due) in enumerate(borrowed_books, start=1):
                print(f"{index}. {book} - {due}")

        return borrowed_books_df


class GetID:

    '''
    - Get PID    - Get a valid person id from user
    - Get PID2   - Get a valid person id from user, modified for view_book_history
    - create PID - Generates a unique person id
    - create BID - Generates a unique book id
    '''

    def __init__(self, user, database):
        if user is not None:
            self.role = user.role
        self.people = database.people
        self.books = database.books
        self.history = database.history


    def get_pid(self):

        '''
        - If role is student, None is returned
        - If role is librarian, they can either choose 'me' - returns None
        - Or librarian can provide a valid user id of target user - returns user id
        '''

        if self.role == "Student":
            return None
        
        else:
            while True:
                target_id = Utils.format_input("Enter the id of the person (or 'me') : ", ret=["me"], typ="int")

                if target_id == "me":
                    return None

                if target_id not in self.people.index:
                    print("No person exists with this id.")

                else:
                    return target_id


    def get_pid2(self):
        
        '''
        - If role is student, None is returned
        - If role is librarian, they can either choose 'me' - returns None
        - Or librarian can provide a valid user id of target user - returns user id
        - Or librarian can choose 'all' (to view all user's borrow history) - returns 'all'
        '''

        if self.role == "Student":
            return None
        
        else:
            while True:
                target_id = Utils.format_input(
                    "Enter the id of the person (or 'me'/'all') : ",
                    ret=["me", "all"],
                    typ="int",
                )

                if target_id == "me":
                    return None
                if target_id == "all":
                    return target_id

                if target_id not in self.people.index:
                    print("No person exists with this id.")

                else:
                    return target_id


    def create_pid(self):

        '''
        - Create a valid unique person id
        '''

        curr = max(self.people.index.max(), self.history["User ID"].max())
        return curr + 1


    def create_bid(self):

        '''
        - Create a valid unique book id
        '''
        
        curr = max(self.books.index.max(), self.history["Book ID"].max())
        return curr + 1
