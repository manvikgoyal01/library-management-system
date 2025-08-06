'''
This file contains login class
- Managing login of an existing/new user
'''

import sys
from datetime import datetime
from utils import Utils, GetID
from config import lib_pass
#lib_pass is the librarian password

class Login:

    '''
    - Logs in new users by verifying with password
    - Creates a new account if doesnt exit
    - Gives warning on creation of account if a account with similar name exists 
    - User's data is stored in self.variable to ensure centralised management
    '''
    
    def __init__(self, database):
        self.people = database.people
        self.passwords = database.passwords
        self.get_id = GetID(None, database)


    def existing_user(self):

        '''
        - Asks for user id
        - Asks for user's password
        - If user fails to provide password, program exits
        - User can exit at any time
        - User's info is found and stored in self.variables
        '''

        #validating if the id exists
        while True:
            self.id = Utils.format_input("Enter your ID (or 'exit') : ", typ="int", stop="exit")

            validated = Utils.validate_id(self.id, self.people)
            if validated:
                break
            else:
                print("\nWe could not find your id.")

        #if user is librarian, asks for librarian password else for user password
        self.role = self.people.loc[self.id, "Role"]

        if self.role == "Librarian":

            while True:
                pwd = input("\nEnter the librarian password (or 'exit') : ")

                if pwd.lower() == "exit":
                    sys.exit("\nExiting...\n")
                elif pwd == lib_pass:
                    break
                else:
                    print("\nInvalid Password.")

        elif self.role == "Student":

            while True:
                pwd = input("\nEnter your password (or 'exit') : ")

                if pwd.lower() == "exit":
                    sys.exit("\nExiting...\n")
                elif self.passwords[str(self.id)] == pwd:
                    break
                else:
                    print("\nInvalid Password. If you forgot, please ask a librarian to reset your password.")

        self.name = self.people.loc[self.id, "Name"]
        self.email = self.people.loc[self.id, "Email"]


    def create_user(self):

        '''
        - Asks for user's name
        - Warns if similar name in database exists
        - Asks for email, valid role
        - Asks for librarian password if role is librarian
        - Asks to create a password if role is user
        '''

        #creates a new user id 
        pid = self.get_id.create_pid()

        self.name = Utils.format_input("Enter your name (or 'exit') : ", case="title", stop="exit")

        #finds similar names in Names of people database 
        #if user confirms they exist, program exits
        names_list = Utils.matching_list(self.name, self.people["Name"].values)

        if len(names_list) > 0:
            print("\nPlease confirm if you are in the database below :\n")
            print(self.people[self.people["Name"].isin(names_list)])
            print("\nAre you in the database?")

            confirm = Utils.consent()
            if confirm:
                sys.exit("\nPlease login with your credentials.\nExiting...\n")

        #if user doesnt exist, asks for id
        self.email = Utils.format_input("Enter your email (or 'exit') : ", stop="exit")

        #asks for a valid role
        while True:

            self.role = Utils.format_input("Enter your role (or 'exit') : ", case="title", stop="exit")
            self.role = Utils.match_input(self.role, ["Librarian", "Student"])

            if self.role not in ["Librarian", "Student"]:
                print("\nEnter a valid role ('Student'/'Librarian').")
            else:
                break
        
        #asks for librarian password if role is librarian
        if self.role == "Librarian":
            while True:

                pwd = input("\nPlease enter the librarian password (or 'exit') : ")
                if pwd == "exit":
                    sys.exit("\nExiting...\n")

                if pwd != lib_pass:
                    print("\nInvalid librarian passowrd. Please contact technical team if you forgot the password.")
                else:
                    break
        
        #asks to create a password if role is student
        elif self.role == "Student":

            while True:
                pwdi = input("\nEnter a password for your account (or 'exit') : ").strip()
                if pwdi.lower() == "exit":
                    sys.exit("\nExiting...\n")

                # intentionally not stripping so that user doesn't believe password with extra spaces is valid.
                pwdii = input("Re-enter your password to confirm : ")

                if pwdi == pwdii:
                    self.passwords[str(pid)] = pwdi
                    break
                else:
                    print("\nYours passwords do not match.")

        #shows user the details with which account will be created and confirms
        print("\nYou are about to create an account with following details :")
        print(f"User ID : {pid}")
        print(f"Name : {self.name}")
        print(f"Email : {self.email}")
        print(f"Role : {self.role}")

        confirm = Utils.consent()
        if confirm:
            self.id = pid
            self.people.loc[pid, :] = [
                self.name,
                self.email,
                self.role,
                datetime.strftime(datetime.today(), "%d-%m-%Y"),
            ]
        else:
            sys.exit("\nAccount Creation Stopped.\nExiting...\n")