📝 Student & Supermarket Management (Console Apps)

This repository contains two simple console-based management systems written in Python with PostgreSQL integration:
📚 Student Management System

File: student-management.py

Features:
    View all students
    Add new student
    Delete student
    Search for a student

Student fields:
    name (string)
    number (string/integer)
    quаrter (string/integer)

Run:
python student-management.py

🛒 Supermarket Management System

File: supermarket-management.py

Features:
    View available items
    Add new items
    Purchаse item (reduce quantity)
    Search items
    Edit item details (name, price, quantity)

Item fields:
    name (string)
    price (float)
    quantity (int)

Run:
python supermarket-management.py

⚙️ Environment Setup
Both scripts load database credentials from a .env file.
Example structure for .env:

# For supermarket-management.py
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=supermarket_db
DB_PORT=5432

# For student-management.py
DB_USER2=your_user
DB_PASSWORD2=your_password
DB_HOST2=localhost
DB_NAME2=student_db
DB_PORT2=5432

🧷 Notes
    PostgreSQL must be running and the required tables (items, students) must exist.
    These are console-only apps intended for local/demo purposes.
