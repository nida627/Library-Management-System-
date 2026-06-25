import json

class Book:
    def __init__(self, book_id, title, author, quantity, issued_to=None):
        self.id = book_id.strip()
        self.title = title.strip()
        self.author = author.strip()
        self.quantity = int(quantity)
        # If issued_to is not provided, an empty list [] is created (to track multiple students)
        self.issued_to = issued_to if issued_to is not None else []

    def to_dict(self):
        """Converts object data into a dictionary so it can be saved in JSON format."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "quantity": self.quantity,
            "issued_to": self.issued_to
        }


class Library:
    def __init__(self):
        # Encapsulation: Hidden private list
        self.__books = []
        self.DATABASE_FILE = "library_data.json"
        self.load_from_file()

    # ==================== FILE HANDLING ====================
    def load_from_file(self):
        try:
            with open(self.DATABASE_FILE, "r") as file:
             raw_data = json.load(file)

            self.__books = [
                Book(
                    b["id"],
                    b["title"],
                    b["author"],
                    b["quantity"],
                    b.get("issued_to", [])
                )
                for b in raw_data
            ]

        except FileNotFoundError:
        # Agar file nahi mili to kuch nahi karna
         self.__books = []

        except Exception as e:
         print(f"Error loading data: {e}")

    def save_to_file(self):
        """Converts all Book objects into dictionary format and saves them into a JSON file."""
        try:
            with open(self.DATABASE_FILE, 'w') as file:
                # Converting each book object into a dictionary and saving it in a list
                json_ready_data = [book.to_dict() for book in self.__books]
                json.dump(json_ready_data, file, indent=4)
        except Exception as e:
            print(f" error occurs on data saving: {e}")
    # =======================================================

    # Add Book
    def add_book(self):
        book_id = input("Enter Book ID: ").strip()

        # Check duplicate ID
        for book in self.__books:
            if book.id == book_id:
                print("Book ID already exists!")
                return

        title = input("Enter Book Name: ").strip()
        author = input("Enter Author Name: ").strip()

        while True:
            try:
                quantity = int(input("Enter Quantity: "))
                if quantity < 0:
                    print("Quantity cannot be negative.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number.")

        # Creating a new Book object
        new_book = Book(book_id, title, author, quantity)
        self.__books.append(new_book)
        self.save_to_file()
        print("Book Added Successfully.")

    # View Books (With Issue & Student Status)
    def view_books(self):
        if len(self.__books) == 0:
            print("No books available.")
            return

        print("\n========== BOOK LIST ==========")
        for book in self.__books:
            # Check if the book is issued to anyone or not
            if book.issued_to:
                status = f"Issued to: {', '.join(book.issued_to)}"
            else:
                status = "Available in Library"

            print(f"Book ID  : {book.id}")
            print(f"Title    : {book.title}")
            print(f"Author   : {book.author}")
            print(f"Quantity : {book.quantity}")
            print(f"Status   : {status}")
            print("-" * 30)

    # Search Book
    def search_book(self):
        search = input("Enter Book ID or Book Name: ").lower().strip()
        found = False

        for book in self.__books:
            if book.id.lower() == search or book.title.lower() == search:
                print("\nBook Found")
                print("----------------------")
                print("Book ID  :", book.id)
                print("Title    :", book.title)
                print("Author   :", book.author)
                print("Quantity :", book.quantity)
                status = f"Issued to: {', '.join(book.issued_to)}" if book.issued_to else "Available"
                print("Status   :", status)
                found = True
                break

        if not found:
            print("Book not found.")

    # Issue Book
    def issue_book(self):
        book_id = input("Enter Book ID: ").strip()

        for book in self.__books:
            if book.id == book_id:
                if book.quantity > 0:
                    student = input("Enter Student Name: ").strip()
                    book.quantity -= 1
                    book.issued_to.append(student) # Added student name to the list
                    self.save_to_file()
                    print(f'Book issued successfully to {student}.')
                    print("Remaining Quantity:", book.quantity)
                else:
                    print("Book is out of stock.")
                return

        print("Book not found.")

    # Return Book
    def return_book(self):
        book_id = input("Enter Book ID: ").strip()

        for book in self.__books:
            if book.id == book_id:
                student = input("Enter Student Name: ").strip()
                
                if student in book.issued_to:
                    book.quantity += 1
                    book.issued_to.remove(student) # Removed student name from the list
                    self.save_to_file()
                    print(f'Book returned successfully by {student}.')
                    print("Available Quantity:", book.quantity)
                else:
                    print(f" Error: This book was not issued to {student}.")
                return

        print("Book not found.")


# Main Program Loop
library = Library()

while True:
    print("\n========== Library Management System ==========")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        library.add_book()
    elif choice == "2":
        library.view_books()
    elif choice == "3":
        library.search_book()
    elif choice == "4":
        library.issue_book()
    elif choice == "5":
        library.return_book()
    elif choice == "6":
        print("Thank You for using Library Management System.")
        break
    else:
        print("Invalid Choice. Please try again.")
