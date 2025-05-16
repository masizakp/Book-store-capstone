
import sqlite3

# Function to connect to the database
def connect_to_database():
    """
    Connects to the ebookstore database.  Creates the database
    if it does not exist.
    Handles potential connection errors.
    Returns:
        sqlite3.Connection: The database connection object,
        or None on error.
    """
    try:
        conn = sqlite3.connect('ebookstore.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to create the books table
def create_table(conn):
    """
    Creates the 'book' table in the database if it does not exist.
    Handles potential table creation errors.

    Args:
        conn (sqlite3.Connection): The database connection object.
    """
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                qty INTEGER
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        # Consider a rollback here to ensure data consistency
        conn.rollback()

# Function to populate the books table
def populate_table(conn):
    """
    Populates the 'book' table with initial data.  Checks if the
    table is already populated
    to avoid duplicate entries.

    Args:
        conn (sqlite3.Connection): The database connection object.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM book")
        count = cursor.fetchone()[0]

        if count == 0:
            books = [
            (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, 'Harry Potter and the Philosopher\'s Stone',
            'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe',
            'C. S. Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
            ]
            cursor.executemany(
            'INSERT INTO book VALUES (?, ?, ?, ?)', books)
            conn.commit()
            print("Initial data populated.")  #Added message
        else:
            print("Table already populated.") #Added message
    except sqlite3.Error as e:
        print(f"Error populating table: {e}")
        conn.rollback()

# Function to add a new book to the database
def add_book(conn):
    """
    Adds a new book to the 'book' table.  Prompts the user for book
    details and validates the input.

    Args:
        conn (sqlite3.Connection): The database connection object.
    """
    try:
        cursor = conn.cursor()
        while True:
            try:
                id = int(input("Enter book ID: "))
                break # Exit loop if ID is valid
            except ValueError:
                print(
            "Invalid input. Please enter a valid integer for the book ID."
            )

        title = input("Enter book title: ")
        author = input("Enter book author: ")

        while True:
            try:
                qty = int(input("Enter book quantity: "))
                if qty >= 0:
                    break # Exit loop if quantity is valid
                else:
                    print("Quantity must be a non-negative integer.")
            except ValueError:
                print(
                "Invalid input. Please enter a valid integer for the" \
                "quantity.")
        # Check if the book ID already exists
        cursor.execute("SELECT id FROM book WHERE id = ?", (id,))
        existing_id = cursor.fetchone()
        if existing_id:
            print(f"Error: Book with ID {id} already exists.")
            return  # Return to the main menu, do not add the book

        cursor.execute(
        'INSERT INTO book VALUES (?, ?, ?, ?)',
        (id, title, author, qty))
        conn.commit()
        print("Book added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding book: {e}")
        conn.rollback()

# Function to update book information in the database
def update_book(conn):
    """
    Updates the information for an existing book in the 'book' table.
    Prompts the user for the book ID and new information.  Validates input.

    Args:
        conn (sqlite3.Connection): The database connection object.
    """
    try:
        cursor = conn.cursor()
        while True:
            try:
                id = int(input(
                "Enter the ID of the book to update: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer"
                "for the book ID.")
        # Check if the book exists
        cursor.execute("SELECT * FROM book WHERE id = ?", (id,))
        book = cursor.fetchone()
        if not book:
            print("Book not found.")
            return

        title = input(
        f"Enter new title (current: {book[1]}): ") or book[1]
        author = input(
        f"Enter new author (current: {book[2]}): ") or book[2]

        while True:
            qty_input = input(
            f"Enter new quantity (current: {book[3]}): ")
            if not qty_input:
                qty = book[3] # Keep old value
                break
            try:
                qty = int(qty_input)
                if qty >= 0:
                    break
                else:
                    print(
                    "Quantity must be a non-negative integer.")
            except ValueError:
                print(
                "Invalid input. Please enter a valid integer for" \
                " the quantity.")
        cursor.execute(
        'UPDATE book SET title = ?, author = ?, qty = ? WHERE id = ?',
        (title, author, qty, id))
        conn.commit()
        print("Book updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating book: {e}")
        conn.rollback()

# Function to delete a book from the database
def delete_book(conn):
    """
    Deletes a book from the 'book' table.  Prompts the user
    for the book ID and confirms the deletion.

    Args:
        conn (sqlite3.Connection): The database connection object.
    """
    try:
        cursor = conn.cursor()
        while True:
            try:
                id = int(input(
                "Enter the ID of the book to delete: "))
                break
            except ValueError:
                print(
                "Invalid input. Please enter a valid integer for" \
                " the book ID.")

        # Check if the book exists before attempting to delete
        cursor.execute("SELECT * FROM book WHERE id = ?", (id,))
        book = cursor.fetchone()
        if not book:
            print("Book not found.")
            return  # Exit the function if the book doesn't exist

        confirmation = input(
        f"Are you sure you want to delete the book with ID {id}? (y/n): ")
        if confirmation.lower() == 'y':
            cursor.execute('DELETE FROM book WHERE id = ?', (id,))
            conn.commit()
            print("Book deleted successfully.")
        else:
            print("Deletion cancelled.")
    except sqlite3.Error as e:
        print(f"Error deleting book: {e}")
        conn.rollback()

# Function to search for a book in the database
def search_books(conn):
    """
    Searches for books in the 'book' table based on title or author.
    Prompts the user for the search term and displays the results.

    Args:
        conn (sqlite3.Connection): The database connection object.
    """
    try:
        cursor = conn.cursor()
        search_term = input("Enter title or author to search: ")
        cursor.execute("SELECT * FROM book WHERE title LIKE ? OR author LIKE ?",
         ('%' + search_term + '%', '%' + search_term + '%'))
        books = cursor.fetchall()

        if not books:
            print("No books found matching your search.")
        else:
            print("\nSearch Results:")
            for book in books:
                print(
                f"ID: {book[0]}, Title: {book[1]}, Author: {
                book[2]}, Quantity: {book[3]}")
    except sqlite3.Error as e:
        print(f"Error searching books: {e}")

# Function to display the main menu
def display_menu():
    """
    Displays the main menu options to the user.
    """
    print("\nBookstore Management System")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")

# Main function to run the program
def main():
    """
    Main function to run the bookstore management program.
    Connects to the database, creates the table, populates it, and
    displays the main menu.
    """
    conn = connect_to_database()
    if conn is None:
        return  # Exit if database connection fails

    create_table(conn)
    populate_table(conn)

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            add_book(conn)
        elif choice == '2':
            update_book(conn)
        elif choice == '3':
            delete_book(conn)
        elif choice == '4':
            search_books(conn)
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
