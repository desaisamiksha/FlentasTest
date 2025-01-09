import sqlite3


class Book:
    def __init__(self, title, author, isbn, is_borrowed=False):
        """Initialize a book object with title, author, ISBN, and borrowed status."""
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = is_borrowed

    def __str__(self):
        """Return a string representation of the book with its status."""
        status = "Available" if not self.is_borrowed else "Borrowed"
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {status}"


class Library:
    def __init__(self, db_name="library.db"):
        """Initialize the library and connect to the SQLite database."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Create the books table if it does not already exist."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE,
                is_borrowed INTEGER DEFAULT 0
            )
            """
        )
        self.connection.commit()

    def add_book(self, title, author, isbn):
        """Add a new book to the library."""
        try:
            self.cursor.execute(
                "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",
                (title, author, isbn),
            )
            self.connection.commit()
            print(f"Book '{title}' added successfully.")
        except sqlite3.IntegrityError:
            print(f"Book with ISBN '{isbn}' already exists.")

    def borrow_book(self, title):
        """Allow a user to borrow a book if it is available."""
        self.cursor.execute(
            "SELECT * FROM books WHERE title = ? AND is_borrowed = 0", (title,)
        )
        book = self.cursor.fetchone()
        if book:
            self.cursor.execute(
                "UPDATE books SET is_borrowed = 1 WHERE id = ?", (book[0],)
            )
            self.connection.commit()
            print(f"You have borrowed '{title}'.")
        else:
            print(f"Sorry, the book '{title}' is not available.")

    def return_book(self, title):
        """Allow a user to return a borrowed book."""
        self.cursor.execute(
            "SELECT * FROM books WHERE title = ? AND is_borrowed = 1", (title,)
        )
        book = self.cursor.fetchone()
        if book:
            self.cursor.execute(
                "UPDATE books SET is_borrowed = 0 WHERE id = ?", (book[0],)
            )
            self.connection.commit()
            print(f"Thank you for returning '{title}'.")
        else:
            print(f"The book '{title}' was not borrowed or does not exist.")

    def display_available_books(self):
        """Display all books currently available for borrowing."""
        self.cursor.execute("SELECT title, author, isbn FROM books WHERE is_borrowed = 0")
        available_books = self.cursor.fetchall()
        if available_books:
            print("Available Books:")
            for book in available_books:
                print(f"Title: {book[0]}, Author: {book[1]}, ISBN: {book[2]}")
        else:
            print("No books are currently available.")

    def search_book(self, query):
        """Search for a book by title or author."""
        self.cursor.execute(
            "SELECT title, author, isbn, is_borrowed FROM books WHERE title LIKE ? OR author LIKE ?",
            (f"%{query}%", f"%{query}%"),
        )
        results = self.cursor.fetchall()
        if results:
            print("Search Results:")
            for book in results:
                status = "Available" if book[3] == 0 else "Borrowed"
                print(f"Title: {book[0]}, Author: {book[1]}, ISBN: {book[2]}, Status: {status}")
        else:
            print(f"No books found matching '{query}'.")

    def close(self):
        """Close the connection to the database."""
        self.connection.close()


# Main Program
def main():
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Display Available Books")
        print("5. Search for a Book")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            library.add_book(title, author, isbn)
        elif choice == '2':
            title = input("Enter the title of the book to borrow: ")
            library.borrow_book(title)
        elif choice == '3':
            title = input("Enter the title of the book to return: ")
            library.return_book(title)
        elif choice == '4':
            library.display_available_books()
        elif choice == '5':
            query = input("Enter the title or author to search for: ")
            library.search_book(query)
        elif choice == '6':
            library.close()
            print("Exiting the Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
