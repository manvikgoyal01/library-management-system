'''
The main file where everything is stiched and ran
Contains the logic to run the program
'''
from manage_files import ManageFiles
from utils import Utils, GetID
from login import Login
from manage_people import ManagePeople
from manage_books import ManageBooks
import os
import sys

#ensuring each program starts with a clean terminal
os.system("cls")

def main():
    '''
    - Importing databases
    - Presenting user with options based on their role
    - Librarians can specify target user id in certain options (options marked with *)
    - Options available :
        *1. View library card 
        2. View all books
        *3. Issue a book
        *4. Return a book
        *5. View borrowed books history
        *6. Update account
        *7. Change password
        *8. Delete a user
      - Librarian Only :
        9. View all borrowed books
        10. View all due books
        11. View all users
        12. Find a user from name
        13. Add a new book
        14 Remove a book
        15. Add a new user
        - 'option' displays the options available based on role
        - 'exit' option exits the loop and initiates the steps below
    - Upon completion, confirms if changes are to be saved
    - If user wants to save, database is exported else its not

    '''

    # importing the data and formatting it
    df = ManageFiles()
    df.load_data()
    user = Login(df)

    #asks if user is existing and take login/create account action
    print("Are you an existing user?")
    ask = Utils.consent()

    if ask:
        user.existing_user()

    else:
        user.create_user()

    #assignment of classes used
    target_id = GetID(user, df)
    manage_books = ManageBooks(user, df)
    manage_people = ManagePeople(df, user)

    #initially all options are printed
    print("\nYou can use the following options (or 'exit') :\n")
    print("1. View library card")
    print("2. View all books")
    print("3. Issue a book")
    print("4. Return a book")
    print("5. View borrowed books history")
    print("6. Update account")
    print("7. Change password.")
    print("8. Delete a user")
    if user.role == "Librarian":
        print("9. View all borrowed books")
        print("10. View all due books")
        print("11. View all users")
        print("12. Find a user from name")
        print("13. Add a new book")
        print("14 Remove a book")
        print("15. Add a new user")

    #while loop ensures the program runs until the user wants to quit
    while True:

        option = Utils.format_input("Enter the option code (or 'options' to show options) : ")

        match option:

            #if user wants to exit and confirms, rest exit process take place outside the loop
            case "exit":
                print("\nConfirm that you want to exit the program")

                confirm = Utils.consent()
                if not confirm:
                    continue
                else:
                    break
            
            #options are only printed when user asks to avoid cluttering
            case "options":
                print("\nYou can use the following options (or 'exit') :\n")
                print("1. View library card")
                print("2. View all books")
                print("3. Issue a book")
                print("4. Return a book")
                print("5. View borrowed books history")
                print("6. Update account")
                print("7. Change password.")
                print("8. Delete a user")
                if user.role == "Librarian":
                    print("9. View all borrowed books")
                    print("10. View all due books")
                    print("11. View all users")
                    print("12. Find a user from name")
                    print("13. Add a new book")
                    print("14 Remove a book")
                    print("15. Add a new user")

            #View library card
            case "1":
                tid = target_id.get_pid()
                manage_books.view_card(tid)

            #view all books in database
            case "2":
                manage_books.view_all_books()

            #issue a book
            case "3":
                tid = target_id.get_pid()
                manage_books.issue_book(tid)

            #return a book
            case "4":
                tid = target_id.get_pid()
                manage_books.return_book(tid)

            #view borrowed books history
            case "5":
                tid = target_id.get_pid2()
                manage_books.borrowed_history(tid)

            #update details of a user
            case "6":
                tid = target_id.get_pid()
                manage_people.update_person(tid)

            #change password of a user
            case "7":
                tid = target_id.get_pid()
                manage_people.change_password(tid)

            #remove a person from database
            case "8":
                tid = target_id.get_pid()
                manage_people.remove_person(tid)

            ##librarians only options start here
            
            #view all currently borrowed books
            case "9" if user.role == "Librarian":
                manage_books.borrowed_books()

            #view all due books
            case "10" if user.role == "Librarian":
                manage_books.due_books()

            #view all users and their details
            case "11" if user.role == "Librarian":
                manage_people.view_all_people()

            #find a person from name
            case "12" if user.role == "Librarian":
                manage_people.find_person()

            #add a book
            case "13" if user.role == "Librarian":
                manage_books.add_book()

            #remove a book
            case "14" if user.role == "Librarian":
                manage_books.remove_book()

            #add a person
            case "15" if user.role == "Librarian":
                tid = target_id.get_pid()
                manage_people.add_person(tid)
    
    #completing the exit process
    #asks if user wants to update the database for changes made during their session activity
    print("\nDo you want to save all the updates to library records you made?")

    while True:
        inp = Utils.format_input("Please enter 'Save' or 'Dont Save : ")

        if inp == "save":
            df.export_data()
            sys.exit("\nExiting the program and saving changes.\n")

        elif inp == "dont save":
            sys.exit("\nExiting the program without saving changes.\n")

        else:
            print("\nPlease enter 'Save' or 'Dont Save'.")

if __name__ == "__main__" :
    main()