import sqlite3

# Database Setup
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    quantity INTEGER NOT NULL
)
""")

conn.commit()


# Functions
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    quantity = int(input("Enter quantity: "))

    cursor.execute(
        "INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
        (title, author, quantity)
    )

    conn.commit()
    print("\nBook added successfully!\n")


def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if not books:
        print("\nNo books found.\n")
        return

    print("\n===== BOOK LIST =====")

    for book in books:
        print(
            f"ID: {book[0]} | "
            f"Title: {book[1]} | "
            f"Author: {book[2]} | "
            f"Quantity: {book[3]}"
        )

    print()


def search_book():
    keyword = input("Enter title to search: ")

    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        ('%' + keyword + '%',)
    )

    books = cursor.fetchall()

    if books:
        print("\nSearch Results:")
        for book in books:
            print(
                f"ID: {book[0]} | "
                f"Title: {book[1]} | "
                f"Author: {book[2]} | "
                f"Quantity: {book[3]}"
            )
    else:
        print("\nBook not found.")

    print()


def update_book():
    book_id = int(input("Enter Book ID: "))

    cursor.execute(
        "SELECT * FROM books WHERE id=?",
        (book_id,)
    )

    book = cursor.fetchone()

    if not book:
        print("\nBook not found.\n")
        return

    title = input("New title: ")
    author = input("New author: ")
    quantity = int(input("New quantity: "))

    cursor.execute("""
        UPDATE books
        SET title=?, author=?, quantity=?
        WHERE id=?
    """, (title, author, quantity, book_id))

    conn.commit()

    print("\nBook updated successfully!\n")


def delete_book():
    book_id = int(input("Enter Book ID to delete: "))

    cursor.execute(
        "DELETE FROM books WHERE id=?",
        (book_id,)
    )

    conn.commit()

    print("\nBook deleted successfully!\n")


def issue_book():
    book_id = int(input("Enter Book ID to issue: "))

    cursor.execute(
        "SELECT quantity FROM books WHERE id=?",
        (book_id,)
    )

    book = cursor.fetchone()

    if not book:
        print("\nBook not found.\n")
        return

    if book[0] <= 0:
        print("\nBook out of stock.\n")
        return

    cursor.execute(
        "UPDATE books SET quantity = quantity - 1 WHERE id=?",
        (book_id,)
    )

    conn.commit()

    print("\nBook issued successfully!\n")


def return_book():
    book_id = int(input("Enter Book ID to return: "))

    cursor.execute(
        "SELECT * FROM books WHERE id=?",
        (book_id,)
    )

    if not cursor.fetchone():
        print("\nBook not found.\n")
        return

    cursor.execute(
        "UPDATE books SET quantity = quantity + 1 WHERE id=?",
        (book_id,)
    )

    conn.commit()

    print("\nBook returned successfully!\n")


# Main Menu
while True:
    print("========== LIBRARY MANAGEMENT SYSTEM ==========")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Issue Book")
    print("7. Return Book")
    print("8. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        add_book()

    elif choice == "2":
        view_books()

    elif choice == "3":
        search_book()

    elif choice == "4":
        update_book()

    elif choice == "5":
        delete_book()

    elif choice == "6":
        issue_book()

    elif choice == "7":
        return_book()

    elif choice == "8":
        print("\nThank you for using Library Management System.")
        break

    else:
        print("\nInvalid choice.\n")

conn.close()