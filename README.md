````markdown
# Library Management System (LMS)

A terminal-based library management system using Python, JSON, and pandas. It allows librarians and students to manage books, users, and borrowing records with fuzzy search via RapidFuzz.

## 📁 Project Structure

📁 library management repository
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── 📁 data/
│   ├── books.json
│   ├── borrowed_books.json
│   ├── borrowed_history.json
│   ├── people.json
│   └── passwords.json
│
├── 📁 src/
│   ├── config.py
│   ├── login.py
│   ├── manage_books.py
│   ├── manage_people.py
│   ├── manage_files.py
│   ├── utils.py
│   └── main.py
└──────────────────────────────

````

## ⚙️ Configuration (src/config.py)

* `Lib_pass`: Password for librarian actions (default: `lib123`)
* `Borrow_limit`: Max books a user can borrow (default: `5`)
* `Return_days`: Days until due date (default: `7`)
* `Match_limit`: Max fuzzy matches to display (default: `3`)
* `Match_cutoff`: Minimum match score % to include in results (default: `65`)

## 🔐 Login System (src/login.py)

* **Existing users**: Enter ID and name to log in. Students use personal password, librarians use shared password.
* **New users**: Enter name, email, role (validated with RapidFuzz). Student sets a password, librarian must provide `Lib_pass`.
* Duplicate name warnings prevent accidental duplicate accounts.

## 📚 Book Management (src/manage\_books.py)

* `View all books`: Shows full book database.
* `*View library card`: See your (or selected user's) details.
* `*Issue book`: Check borrowed books, validate conditions, confirm before issuing.
* `*Return book`: Show borrowed books, validate, confirm before returning.
* `*Borrowed history`: View books returned (students: self only; librarians: all/users/self).
* `View all borrowed books`: List all currently borrowed books.
* `View due books`: List all overdue books.
* `Add book`: Librarian-only, warns on duplicates, requires confirmation.
* `Remove book`: Librarian-only, by name, with confirmation.

## 👤 People Management (src/manage\_people.py)

* `Add person`: Librarian-only, warns on similar names, requires confirmation.
* `Remove person`: By ID (students: self only; librarians: anyone). Triggers exit after deletion.
* `Update person`: Change name or email.
* `Change password`: Students require old password; librarians can change student passwords without it.
* `View all people`: Librarian-only, passwords are never shown.
* `Find person`: Librarian-only, search by name (used to get user ID).

## 🗃️ File Management (src/manage\_files.py)

* `Load files`: Converts JSON to pandas DataFrame or dict.
* `Export files`: Converts updated data back to JSON. Passwords use string keys to avoid errors.

## 🛠️ Utilities (src/utils.py)

* `col_string(df)`: Converts all columns to string type.
* `format_input(...)`: Input formatting with options (trim, lower, alphanumeric, etc.).
* `validate_id(pid, df)`: Checks if ID exists in a DataFrame.
* `consent(prompt)`: Yes/No confirmation (used before critical actions).
* `match_input(value, iterable)`: RapidFuzz-powered fuzzy match with confirmations.
* `print_borrowed(user_id)`: Lists borrowed books for the user.

### 📌 ID Utils (class Get\_ID in utils.py)

* `get_pid(self)`: Returns own ID or asks for a valid person ID (librarians only).
* `get_pid2(self)`: Same as above but allows `"all"` for history view.
* `create_pid()`: Generates a unique user ID.
* `create_bid()`: Generates a unique book ID.
* Book and user IDs are always unique and never reused.

## 🧠 Main Flow (src/main.py)

1. Files are loaded using `load_files()`.

2. User logs in (existing or new).

3. Menu options shown based on role:

   * `options`: Reprints the available options
   * `exit`: Ends session after confirmation

4. On `exit`:

   * Confirms if user wants to save changes (`save` / `don't save`)
   * If yes, all databases are exported. If not, session ends without saving.

## 📄 Databases (data/)

* `books.json`: Book ID → name, author, genre, available/total copies
* `borrowed_books.json`: Unique index → book/user ID, name, issue date, due date
* `borrowed_history.json`: Same as above + return date and late return flag
* `people.json`: User ID → name, email, role, join date
* `passwords.json`: `{ user_id (str): password }`

## 🧾 User Options Menu

```
`*` indicates student can do for themselves; librarian can do for any user.

*1. View library card  
2. View all books  
*3. Issue a book  
*4. Return a book  
*5. View borrowed books history  
*6. Update account  
*7. Change password  
*8. Delete a user  

- Librarian Only:
9. View all borrowed books  
10. View all due books  
11. View all users  
12. Find a user from name  
13. Add a new book  
14. Remove a book  
15. Add a new user  

- 'option' displays this menu again  
- 'exit' ends the session and asks to save changes  
```

## 💡 Notes

* IDs, names, books are all case-insensitive and fuzzy matched using RapidFuzz.
* All critical actions require confirmation to prevent mistakes.
