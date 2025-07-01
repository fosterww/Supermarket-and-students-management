import psycopg2

import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER2")
DB_PASSWORD = os.getenv("DB_PASSWORD2")
DB_HOST = os.getenv("DB_HOST2")
DB_NAME = os.getenv("DB_NAME2")
DB_PORT = os.getenv("DB_PORT2")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()


def get_all_students():
    cur.execute("SELECT * FROM students")
    return cur.fetchall()

def add_student(name, number, quarter):
    cur.execute("INSERT INTO students (name, number, quarter) VALUES (%s, %s, %s)", (name, number, quarter))
    conn.commit()

def delete_student(name):
    cur.execute("DELETE FROM students WHERE name = %s", (name,))
    conn.commit()

def find_student(name):
    cur.execute("SELECT * FROM students WHERE LOWER(name) = LOWER(%s)", (name,))
    return cur.fetchone()

# ----------------- STUDENT MANAGEMENT SYSTEM --------------------
while True:
    print("""
Welcome to Student Managment
Enter an option of your choice
1.View all students\n2.Add students\n3.Delete students\n4.Find student\n5.Close the menu
    """)

    choice = input('Enter your choice (1-5): ').strip()
    if choice == '1':
        students = get_all_students()
        print('Fetching all students...')
        if students:
            print('List of students:')
            print('-------------------')
            for student in students:
                print(f'Name: {student[1]}, Number: {student[0]}, Quarter: {student[3]}')
        else:
            print('No students found. Please add students first.')

    elif choice == '2':
        name = input('Enter student name: ').strip()
        number = input('Enter student number: ').strip()
        quarter = input('Enter student quarter: ').strip()
        add_student(name, number, quarter)
        print(f'Student {name} added successfully!')

    elif choice == '3':
        name = input('Enter student name: ').strip()
        student = find_student(name)
        if not student:
            print('Incorrect Name. Please try again.')
            continue
        else:
            delete_student(student[1])
        print(f'Student {name} deleted successfully!')

    elif choice == '4':
        name = input('Enter student name to find: ').strip()
        student = find_student(name)
        if student:
            print(f'Found student - Name: {student[1]}, Number: {student[0]}, Quarter: {student[3]}')
        else:
            print(f'Student {name} not found.')

    elif choice == '5':
        print('Closing the menu')
        break
    else:
        print('Invalid option\nPlease try again')

cur.close()
conn.close()






