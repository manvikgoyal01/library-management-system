'''
Contains ManagePeople class
- Allows you to access and modify people database
'''

from utils import Utils, GetID
from datetime import datetime
import sys
from manage_books import ManageBooks

class ManagePeople:

    '''
    - Add person      - Add a person to database (librarian only)
    - Remove person   - Remove a person from database by id (librarian only)
    - Update person   - Update details of the user (librarian can specify a user id)
    - Change password - Allows you to change password (librarians can specify a user id)
    - View all people - Allows you to view all users in database (librarian only)
    - Find person     - Allows you find a person's details by Name (librarian only)
    '''

    def __init__(self, database, user):
        self.passwords = database.passwords
        self.user = user
        self.database = database
        self.id = user.id
        self.name = user.name
        self.role = user.role
        self.email = user.email

        self.people = database.people
        self.borrowed = database.borrowed
        self.history = database.history
        self.books = database.books
        self.get_id = GetID(user, database)


    def add_person(self):

        '''
        - Add a person
        - Asks for name and warns if similar names exist in database
        - Asks for email, valid role and password
        '''

        target_name = Utils.format_input("Enter the name of the person (or 'Cancel') : ", case="title")

        if target_name == "Cancel":
            print("\nCancelling add person command")

        matching_names = Utils.matching_list(target_name, self.people["Name"].values)

        #if matching names are found, details are displayed and user can confirm if the person exists
        if len(matching_names) > 0:
            print("\nPlease confirm the person is not existing in database already :\n")

            for row in self.people[self.people["Name"].isin(matching_names)].values:
                print(f"Name : {row[0]}  -  Email : {row[1]}  -  Role : {row[2]}  -  Joined On : {row[3]}")

            confirm = Utils.consent("Is the person to be added in list above? ('Yes'/'No') : ")
            if confirm:
                print("\nCancelling add person command.")
                return

        target_email = Utils.format_input("Enter the email of the person : ", case="lower")

        #asks for role of the user and validates the role
        while True:
            target_role = Utils.format_input("Enter the role of the person : ", case="title")
            target_role = Utils.match_input(target_role, ["Librarian", "Student"])

            if target_role not in ["Librarian", "Student"]:
                print("\nEnter a valid role.")
            else:
                break
        
        #if user is a student, allows you to set their password
        if target_role == "Student":
            while True:
                passi = input("\nEnter the password :  ").strip()

                # intentionally not stripping so user doenst believe password with spaces is allowed
                passii = input("\nRe-enter the password :  ")

                if passi == passii:
                    break
                else:
                    print("\nThe passwords do not match.")

        #pid refers to person id. It is uniquely generated
        pid = self.get_id.create_pid()

        #prints details of user to add and confirms
        print("\nYou are about to add a person with following details :\n")
        print(f" ID: {pid} \n Name : {target_name} \n Email : {target_email} \n Role : {target_role}")

        confirm = Utils.consent()
        if confirm:
            self.people.loc[pid, :] = [
                target_name,
                target_email,
                target_role,
                datetime.strftime(datetime.today(), "%d-%m-%Y"),
            ]
            self.passwords[str(pid)] = passi
            print("\nThe person has been successfully addded.")

        else:
            print("\nCancelling add person command.")
            return


    def remove_person(self, target_id=None):

        '''
        Allows to remove yourself, librarians can specify a user id to remove
        Exits/Cancels the function if there are borrowed books
        Confirms if you want to remove the user
        If you delete your own account, the program is exited (logic executed in main.py)
        Returns true if account is deleted else false
        '''

        if target_id is None:
            target_id = self.id

        print("\nYou are about to remove a person with following details :\n")

        #printing user's details and borrowed books
        manage_books = ManageBooks(self.user, self.database)
        borrowed_books_df = manage_books.view_card(targeted_id=target_id, ret=True)

        if len(borrowed_books_df) > 0:
            print("Please return all books before deleting the account.")
            return False

        if self.id == target_id:
            print("\n!! WARNING : Deleting your account will lead to automatic exit from the program !!")

        print(f"\nAre you sure you want to delete this person?")
        confirm = Utils.consent()

        if confirm:
            if self.role == "Student":
                del self.passwords[str(target_id)]
            self.people.drop(target_id, inplace=True)
            print("\nThe person has been successfully deleted")
            return True

        else:
            print("\nCancelling remove person command.")
            return False


    def update_person(self, target_id=None):

        '''
        - Allows update to a person's name and email
        - Password cannot be changed here
        '''

        if target_id is None:
            target_id = self.id

        #prints current details
        print("\nCurrent details :")
        manage_books = ManageBooks(self.user, self.database)
        manage_books.view_card(targeted_id=target_id)

        #asks for new name and email
        new_name = Utils.format_input("Enter your name (or 'Same') : ", case="title")
        new_email = Utils.format_input("Enter your email (or 'Same') : ")

        if new_name == "Same":
            new_name = self.people.loc[target_id, "Name"]
        if new_email == "same":
            new_email = self.people.loc[target_id, "Email"]

        #confirm's updated details
        print("\nYou are about to update the account to following details :")
        print(f"Name : {new_name}")
        print(f"Email : {new_email}")

        confirm = Utils.consent()

        if confirm:
            self.people.loc[target_id, "Name"] = new_name
            self.people.loc[target_id, "Email"] = new_email
            print("\nThe account has been updated successfully")

        else:
            print("\nCancelling ccount update command.")
            return


    def find_person(self):

        '''
        - Find users and their details who have names similar to the name provided
        '''

        target_name = Utils.format_input("Enter the name of person to find : ", case="title")

        #finds all people with similar name and allows to choose
        target_name = Utils.match_input(
            target_name, self.people["Name"].drop_duplicates().values
            )

        if target_name not in self.people["Name"].drop_duplicates().values:
            print("\nNo user found with this name.")
            return

        #finds all people who have the name given
        print("\nUsers found :\n")
        print(self.people[self.people["Name"] == target_name])


    def view_all_people(self): 

        '''
        - Displays all users in the database
        '''

        print("\nAll users in the database\n")
        print(self.people)


    def change_password(self, target_id=None):

        '''
        - Allows students to change their password by entering current one
        - Librarian cannot change the librarian password
        - Librarians can change student's password but they wont be asked/displayed current one
        '''

        if target_id == None:
            target_id = self.id

        role = self.people.loc[target_id, "Role"]

        #if librarian tries to change librarian password, function is exited
        if role == "Librarian" and target_id == self.id:
            print("\nPlease ask the technical team to update the librarian password.")
            return

        #students need to their their old password 
        if self.role == "Student":

            while True:
                old_pass = input("\nEnter your old password (or 'Cancel') : ").strip()

                if old_pass.lower() == "cancel":
                    print("\nCancelling change password command.")
                    return

                if old_pass == self.passwords[str(target_id)]:
                    break
                else:
                    print("\nPassword entered does not match your current password.")

        #allows new password to be set
        while True:
            new_passi = input("\nEnter the new password (or 'Cancel') :  ").strip()

            if new_passi.lower() == "cancel":
                print("\nCancelling change password command.")
                return

            # intentionally not stripping so user doenst believe password with spaces is allowed
            new_passii = input("\nRe-enter the new password :  ")

            if new_passi == new_passii:
                break
            else:
                print("\nThe passwords do not match.")
        
        #confirmation to change the password
        print("\nPlease confirm that you want to change the password.")
        confirm = Utils.consent()

        if confirm:
            self.passwords[str(target_id)] = new_passi
            print("\nThe password has been successfully changed.")
            return
        
        else:
            print("\nCancelling change password command.")
            return