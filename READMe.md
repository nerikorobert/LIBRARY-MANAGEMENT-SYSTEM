# library-management-system
The Library Management System is a Python-based command-line application for managing a library's collection of books and journals. It provides functionality for borrowing items, returning items, paying late fees, and searching the library's collection.


## Table of content
* Description 
* Installation requirement
* Technology used
* Licence
* Authors info

# DESCRIPTION
* The Library Management System offers the following features:

* Borrow Item: Borrow books and journals from the library's collection. Check item availability and return dates.

* Return Item: Return borrowed items and calculate late fees for overdue returns.

* Pay Late Fees: Pay late fees for overdue items.

* Search Library: Search for books and journals by title, author, or editor.

* Database Management: The system uses SQLAlchemy to manage the library's database, which stores information about items, students, and transactions.


# INSTALLATION PROCESS

* Git clone the repository to your local machine using the command `https://github.com/nerikorobert/LIBRARY-MANAGEMENT-SYSTEM.git `
* Navigate to the code challenge directory using `cd library-management-system `
* To install the necessary dependencies run `pipenv install`,`pip install sqlalchemy`
* Run `Alembic init migration` to create our migration environment 
* Install the requirement packages using pip
`pip install sqlalchemy faker`



# TECHNOLOGY USED
python
SQLAlchemy
Faker


# LICENSE
MIT license

# AUTHORS INFO
Robert Neriko