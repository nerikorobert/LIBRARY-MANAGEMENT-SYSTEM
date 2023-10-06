import random
from faker import Faker
from models import Session, Book, Journal, Student

def initialize_db():
    session = Session()
    fake = Faker()

    # Generate Fake Data for Books
    books = []
    for book_id_number in range(1, 101):
        book_id_value = f"B0{book_id_number}"
        total_copies_number = random.randint(1, 100)

        book = Book(
            book_id=book_id_value,
            title=fake.catch_phrase(),
            author=fake.name(),
            total_copies=total_copies_number,
            available_copies=random.randint(1, total_copies_number),
            fee_per_day=10
        )

        session.add(book)
        books.append(book)

    # Generate Fake Data for Journals
    journals = []
    for journal_id_number in range(1, 101):
        journal_id_value = f"J0{journal_id_number}"
        total_copies_number = random.randint(1, 100)

        journal = Journal(
            journal_id=journal_id_value,
            title=fake.catch_phrase(),
            editor=fake.name(),
            total_copies=total_copies_number,
            available_copies=random.randint(1, total_copies_number),
            fee_per_day=10
        )

        session.add(journal)
        journals.append(journal)

    # Generate Fake Data for Students
    students = []
    for student_id_number in range(1, 101):
        student_id_value = f"S0{student_id_number}"

        student = Student(
            student_id=student_id_value,
            name=fake.name()
        )

        session.add(student)
        students.append(student)

    # Commit all changes to the database
    session.commit()

if __name__ == "__main__":
    initialize_db()
