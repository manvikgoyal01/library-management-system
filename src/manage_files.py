'''
Contains manage files class
- Manages import and export of files and databases
'''

import pandas as pd
from utils import Utils
import json


class ManageFiles:

    '''
    - Load data - Loading files from database and formatting fields
    - Export data - Formatting data and then exporting database to files
    '''

    def load_data(self): 

        '''
        - Imports following files to pandas dataframe :
             - people_database.json 
             - books_database.json
             - borrowed_books.json
             - borrowed_history.json
        - Imports following files to dictionary :
            - passwords.json
        
        - Dates are formatted into proper format
        '''

        # importing passwords
        with open(r"data\passwords.json", "r") as f:
            self.passwords = json.load(f)

        # importing databases to pandas
        self.people = pd.read_json(r"data\people_database.json").T
        self.books = pd.read_json(r"data\books_database.json").T
        self.borrowed = pd.read_json(r"data\borrowed_books.json").T
        self.history = pd.read_json(r"data\borrow_history.json").T


    def export_data(self):

        '''
        - Dates are formatted into strings to prevent export/format issues
        - Keys from passwords are ensured are in string format to prevent errors on exporting
        '''

        # formats all dates from datetime to string to avoid exporting issues
        self.passwords = {str(key): str(value) for key, value in self.passwords.items()}

        # exports all the data to json files
        with open(r"data\passwords.json", "w") as f:
            json.dump(self.passwords, f, indent=4)

        self.people.to_json(r"data\people_database.json", indent=4, orient="index")
        self.books.to_json(r"data\books_database.json", indent=4, orient="index")
        self.borrowed.to_json(r"data\borrowed_books.json", indent=4, orient="index")
        self.history.to_json(r"data\borrow_history.json", indent=4, orient="index")
