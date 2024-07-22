import json
import os
from datetime import datetime

BOOKS_FILE = 'books.json'
MEMBERS_FILE = 'members.json'
TRANSACTIONS_FILE = 'transactions.json'

class Library:
    def __init__(self):

        self.books = []
        self.members = []
        self.transactions = []
        self.load_data()

    def load_data(self):

        if os.path.exists(BOOKS_FILE):
            with open(BOOKS_FILE, 'r') as file:
                self.books = json.load(file)
        if os.path.exists(MEMBERS_FILE):
            with open(MEMBERS_FILE, 'r') as file:
                self.members = json.load(file)
        if os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, 'r') as file:
                self.transactions = json.load(file)

    def save_data(self):

        with open(BOOKS_FILE, 'w') as file:
            json.dump(self.books, file, indent=4)
        with open(MEMBERS_FILE, 'w') as file:
            json.dump(self.members, file, indent=4)
        with open(TRANSACTIONS_FILE, 'w') as file:
            json.dump(self.transactions, file, indent=4)

    def add_book(self, title, author, isbn):

        book = {
            'id': len(self.books) + 1,
            'title': title,
            'author': author,
            'isbn': isbn,
            'available': True
        }
        self.books.append(book)
        self.save_data()
        print(f"Book '{title}' by {author} added.")

    def list_books(self):
        """List all books in the library."""
        if not self.books:
            print("No books found.")
            return
        for book in self.books:
            status = "Available" if book['available'] else "Borrowed"
            print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, Status: {status}")

    def edit_book(self, book_id, title=None, author=None, isbn=None):
        """Edit details of an existing book."""
        for book in self.books:
            if book['id'] == book_id:
                if title:
                    book['title'] = title
                if author:
                    book['author'] = author
                if isbn:
                    book['isbn'] = isbn
                self.save_data()
                print(f"Book ID {book_id} updated.")
                return
        print(f"Book ID {book_id} not found.")

    def delete_book(self, book_id):
        """Delete a book from the library."""
        self.books = [book for book in self.books if book['id'] != book_id]
        self.save_data()
        print(f"Book ID {book_id} deleted.")

    def add_member(self, name, email):
        """Register a new member."""
        member = {
            'id': len(self.members) + 1,
            'name': name,
            'email': email
        }
        self.members.append(member)
        self.save_data()
        print(f"Member '{name}' added.")

    def list_members(self):
        """List all registered members."""
        if not self.members:
            print("No members found.")
            return
        for member in self.members:
            print(f"ID: {member['id']}, Name: {member['name']}, Email: {member['email']}")

    def edit_member(self, member_id, name=None, email=None):
        """Edit details of an existing member."""
        for member in self.members:
            if member['id'] == member_id:
                if name:
                    member['name'] = name
                if email:
                    member['email'] = email
                self.save_data()
                print(f"Member ID {member_id} updated.")
                return
        print(f"Member ID {member_id} not found.")

    def delete_member(self, member_id):
        """Delete a member from the library."""
        self.members = [member for member in self.members if member['id'] != member_id]
        self.save_data()
        print(f"Member ID {member_id} deleted.")

    def borrow_book(self, member_id, book_id):
        """Handle borrowing a book by a member."""
        for book in self.books:
            if book['id'] == book_id:
                if not book['available']:
                    print(f"Book ID {book_id} is already borrowed.")
                    return
                book['available'] = False
                transaction = {
                    'transaction_id': len(self.transactions) + 1,
                    'member_id': member_id,
                    'book_id': book_id,
                    'borrow_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'return_date': None
                }
                self.transactions.append(transaction)
                self.save_data()
                print(f"Book ID {book_id} borrowed by Member ID {member_id}.")
                return
        print(f"Book ID {book_id} not found.")

    def return_book(self, member_id, book_id):
        """Handle returning a book by a member."""
        for transaction in self.transactions:
            if transaction['member_id'] == member_id and transaction['book_id'] == book_id and transaction['return_date'] is None:
                transaction['return_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for book in self.books:
                    if book['id'] == book_id:
                        book['available'] = True
                self.save_data()
                print(f"Book ID {book_id} returned by Member ID {member_id}.")
                return
        print(f"No active borrow transaction found for Book ID {book_id} by Member ID {member_id}.")

    def list_transactions(self):
        """List all transactions."""
        if not self.transactions:
            print("No transactions found.")
            return
        for transaction in self.transactions:
            print(f"Transaction ID: {transaction['transaction_id']}, Member ID: {transaction['member_id']}, Book ID: {transaction['book_id']}, Borrow Date: {transaction['borrow_date']}, Return Date: {transaction['return_date']}")

def main():
    library = Library()

    while True:
        print("\nLibrary Management System\n")
        print("1. Add Book")
        print("2. List All Books")
        print("3. Edit Book")
        print("4. Delete Book")
        print("5. Add Member")
        print("6. List All Members")
        print("7. Edit Member")
        print("8. Delete Member")
        print("9. Borrow Book")
        print("10. Return Book")
        print("11. List All Transactions")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            library.add_book(title, author, isbn)
        elif choice == '2':
            library.list_books()
        elif choice == '3':
            book_id = int(input("Enter book ID to edit: "))
            title = input("Enter new title (leave blank to keep current): ")
            author = input("Enter new author (leave blank to keep current): ")
            isbn = input("Enter new ISBN (leave blank to keep current): ")
            library.edit_book(
                book_id,
                title if title else None,
                author if author else None,
                isbn if isbn else None
            )
        elif choice == '4':
            book_id = int(input("Enter book ID to delete: "))
            library.delete_book(book_id)
        elif choice == '5':
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            library.add_member(name, email)
        elif choice == '6':
            library.list_members()
        elif choice == '7':
            member_id = int(input("Enter member ID to edit: "))
            name = input("Enter new name (leave blank to keep current): ")
            email = input("Enter new email (leave blank to keep current): ")
            library.edit_member(
                member_id,
                name if name else None,
                email if email else None
            )
        elif choice == '8':
            member_id = int(input("Enter member ID to delete: "))
            library.delete_member(member_id)
        elif choice == '9':
            member_id = int(input("Enter member ID: "))
            book_id = int(input("Enter book ID: "))
            library.borrow_book(member_id, book_id)
        elif choice == '10':
            member_id = int(input("Enter member ID: "))
            book_id = int(input("Enter book ID: "))
            library.return_book(member_id, book_id)
        elif choice == '11':
            library.list_transactions()
        elif choice == '12':
            print("Exiting Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
