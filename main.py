# Importing Necessary Modules
import random 
from models import Session, Book, Journal, Student, BookTransaction, JournalTransaction
from datetime import datetime, timedelta
from seed import initialize_db
from pathlib import Path

def borrow_item():
    session = Session()
    
    # Input the student ID to identify the borrower.
    student_id = input("Enter Student ID: ")
    
    # Query the database to find the student with the specified ID.
    student = session.query(Student).filter_by(student_id=student_id).first()

    if student:
        item_initials = input("Enter 'B' for book or 'J' for journal if you want to borrow: ")
        item_initials =item_initials.lower()
        
        if item_initials == 'b':
            item_type = 'book'
        elif item_initials == 'j':
            item_type = 'journal'
        else:
            item_type = 'invalid'
        
        if item_type == 'book' or item_type == 'journal':
            search_term = input(f"Enter a search term for the {item_type} you want to borrow: ")

            # Perform a search query to find items of the specified type matching the search term
            items = session.query(Book if item_type == 'book' else Journal).filter(
                Book.title.like(f"%{search_term}%") if item_type == 'book' else Journal.title.like(f"%{search_term}%")
            ).all() #like() method is used to search partial text match ,it will match titles that contain the search_term anywhere in their title.

            if not items:
                print(f"\nNo {item_type}s found matching your search.")
                return
            
            # Display the found items to the user.
            print(f"\n{item_type.capitalize()}s found: \n")
            #enumerate is used to track the index of each item
            for i, item in enumerate(items, start=1):#specify that index should start from 1
                #displays author/editor depending on whether the item type is book/journal
                print(f"{i}. {item_type.capitalize()} Title: {item.title}, {'Author' if item_type == 'book' else 'Editor'}: {item.author if item_type == 'book' else item.editor}")

            selection = input(f"Enter the number of the {item_type} you want to borrow: ")
            try:
                #convert the user's selection to an integer
                selection = int(selection)
                # Check if the user's selection is within the valid range (1 to the number of items).
                if 1 <= selection <= len(items):
                    #Get the selected item based on the user's selection.
                    selected_item = items[selection - 1]
                    # Check if the selected item is available for borrowing (has at least one available copy).
                    if selected_item.available_copies > 0:
                        # Reduce the available copies of the selected item by one, indicating it has been borrowed.
                        selected_item.available_copies -= 1
                        # Calculate a random return date, which is the current date plus a random number of days between -9 and 9.
                        return_date = datetime.now() + timedelta(days=random.randint(-4, 3))  # random return period
                        # Create a transaction record for the borrowed item.
                        transaction = BookTransaction(student_id=student.id, book_id=selected_item.id, return_date=return_date) if item_type == 'book' else JournalTransaction(student_id=student.id, journal_id=selected_item.id, return_date=return_date)
                        # Add the transaction to the session and commit it to the database.
                        session.add(transaction)
                        session.commit()
                        print(f"\n{student.name} of student ID {student.student_id} has successfully borrowed {item_type} of ID {selected_item.id} '{selected_item.title}' (Due Date: {return_date}).")
                    else:
                        print(f"Selected {item_type} is not available.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid item type")
    else:
        print("Student not found.")

def return_item():
    session = Session()

    student_id = input("Enter Student ID: ")
    
    # Check if the student exists
    student = session.query(Student).filter_by(student_id=student_id).first()

    if student:
        item_initials = input("Enter 'B' for book or 'J' for journal if you want to return: ")
        item_initials = item_initials.lower()
        
        if item_initials == 'b':
            item_type = 'book'
        elif item_initials == 'j':
            item_type = 'journal'
        else:
            item_type = 'invalid'
        
        if item_type == 'book' or item_type == 'journal':
            search_term = input(f"Enter a search term for the {item_type} you want to return: ")

            
            # Perform a search query to find items of the specified type matching the search term
            items = session.query(Book if item_type == 'book' else Journal).filter(
                Book.title.like(f"%{search_term}%") if item_type == 'book' else Journal.title.like(f"%{search_term}%")
            ).all()

            if not items:
                print(f"No {item_type}s found matching your search.")
                return

            print(f"{item_type.capitalize()}s found:")
            for i, item in enumerate(items, start=1):
                print(f"{i}. {item_type.capitalize()} Title: {item.title}, {'Author' if item_type == 'book' else 'Editor'}: {item.author if item_type == 'book' else item.editor}")

            selection = input(f"Enter the number of the {item_type} you want to return: ")
            try:
                #convert the user's input to an integer.
                selection = int(selection)
                #checks if the selected number is within the valid range of item indices
                if 1 <= selection <= len(items):
                    # If selection is valid, it assigns the selected item to the selected_item variable
                    selected_item = items[selection - 1]

                    # Check if the student has borrowed the selected item
                    if item_type == 'book':
                        transaction = session.query(BookTransaction).filter_by(student_id=student.id, book_id=selected_item.id).first()
                    else:
                        transaction = session.query(JournalTransaction).filter_by(student_id=student.id, journal_id=selected_item.id).first()

                    if transaction:
                        # Calculate late fee if the item is returned late
                        return_date = transaction.return_date
                        
                        today = datetime.now()
                        if today > return_date:
                            late_days = (today - return_date).days
                            #calculates the late fee based on the number of late days and the item's per-day late fee.#
                            late_fee = late_days * (selected_item.fee_per_day if item_type == 'book' else selected_item.fee_per_day)
                            transaction.late_fee = late_fee  # Update the late fee in the transaction
                            print(f"Late fee: ${late_fee:.2f}")
                            print(f"{student.name} of student ID {student.student_id} should pay the Late fee: ${late_fee:.2f} of the book ID {selected_item.id} '{selected_item.title}'.")
                            
                        else:
                            # Check if there are no late fees, and then delete the transaction
                            if transaction.late_fee == 0.00:
                                session.delete(transaction)
                            print(f"{student.name} has successfully returned '{selected_item.title}'.")
                        
                            # Update the item's available copies and update the transaction record
                            selected_item.available_copies += 1
                        
                        session.commit()#commits changes to the database session

                    else:
                        print(f"Student has not borrowed this {item_type}.")
                
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid item type")       
    else:
        print("Student not found.")
        
def pay_late_fees():
    session = Session()

    student_id = input("Enter Student ID: ")
    
    # Check if the student exists
    student = session.query(Student).filter_by(student_id=student_id).first()

    if student:
        item_type = input("Enter 'book' or 'journal' for the item you want to return: ")
        search_term = input(f"Enter a search term for the {item_type} you want to return: ")

        # Perform a search query to find items of the specified type matching the search term
        items = session.query(Book if item_type == 'book' else Journal).filter(
            Book.title.like(f"%{search_term}%") if item_type == 'book' else Journal.title.like(f"%{search_term}%")
        ).all()

        if not items:
            print(f"No {item_type}s found matching your search.")
            return

        print(f"{item_type.capitalize()}s found:")
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item_type.capitalize()} Title: {item.title}, {'Author' if item_type == 'book' else 'Editor'}: {item.author if item_type == 'book' else item.editor}")

        selection = input(f"Enter the number of the {item_type} you want to pay late fees for: ")
        try:
            # convert the user's input to an integer
            selection = int(selection)
            if 1 <= selection <= len(items):
                selected_item = items[selection - 1]

                # Check if the student has borrowed the selected item
                if item_type == 'book':
                    transaction = session.query(BookTransaction).filter_by(student_id=student.id, book_id=selected_item.id).first()
                else:
                    transaction = session.query(JournalTransaction).filter_by(student_id=student.id, journal_id=selected_item.id).first()

                if transaction:
                    # Update the item's available copies and update the transaction record
                    selected_item.available_copies += 1
                    
                    session.delete(transaction)
                    
                    session.commit()
                    
                    print(f"{student.name} has successfully payed late fees for '{selected_item.title}'.")

                else:
                    print(f"Student has not borrowed this {item_type}.")
            
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    else:
        print("Student not found.")
        
def search_library():
    session = Session()

    search_term = input("Enter title of book/journal to search: ")
    books = session.query(Book).filter(Book.title.ilike(f"%{search_term}%")).all()
    journals = session.query(Journal).filter(Journal.title.ilike(f"%{search_term}%")).all()

    print("\nBooks found:")
    for book in books:
        print(f"- Title: {book.title}, Author: {book.author}")

    print("\nJournals found:")
    for journal in journals:
        print(f"- Title: {journal.title}, Editor: {journal.editor}")
        
def main():
    # Check if the database file exists
    db_file = Path("library.db")
    if not db_file.is_file():
      initialize_db()
    
    while True:
        print("\nLibrary Menu:")
        print("1. Borrow Item")
        print("2. Return Item")
        print("3. Pay Late Fees")
        print("4. Search Library")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            borrow_item()
        elif choice == "2":
            return_item()
        elif choice == "3":
            pay_late_fees()
        elif choice == "4":
            search_library()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
            