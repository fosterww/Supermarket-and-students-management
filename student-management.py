import psycopg2
import os
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_USER = os.getenv("DB_USER2")
DB_PASSWORD = os.getenv("DB_PASSWORD2")
DB_HOST = os.getenv("DB_HOST2")
DB_NAME = os.getenv("DB_NAME2")
DB_PORT = os.getenv("DB_PORT2")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT]):
    raise ValueError("Missing required database environment variables")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("Database connected successfully!")

except Error as e:
    print(f"Connection error: {e}")
    exit(1)


def validate_student_data(name, number, quarter):
    if not name or len(name) > 100:
        raise ValueError("Invalid name length")
    if not number.isdigit() or len(number) > 20:
        raise ValueError("Invalid student number")



def get_all_students():
    cur.execute("SELECT * FROM students")
    return cur.fetchall()


def add_student(name, number, quarter):
    try:
        validate_student_data(name, number, quarter)
        cur.execute(
            "INSERT INTO students (name, number, quarter) VALUES (%s, %s, %s)",
            (name, number, quarter)
        )
        conn.commit()
    except (Error, ValueError) as e:
        conn.rollback()
        raise Exception(f"Error adding student: {e}")


def delete_student(name):
    try:
        cur.execute("DELETE FROM students WHERE name = %s", (name,))
        conn.commit()
    except Error as e:
        conn.rollback()
        raise Exception(f"Error deleting student: {e}")


def find_student(name):
    cur.execute("SELECT * FROM students WHERE LOWER(name) = LOWER(%s)", (name,))
    return cur.fetchone()


# ----------------- STUDENT MANAGEMENT SYSTEM --------------------
try:
    while True:
        print("""
Welcome to Student Management System
====================================
1. View all students
2. Add student
3. Delete student
4. Find student
5. Exit
====================================
        """)

        try:
            choice = input('Enter your choice (1-5): ').strip()

            if choice == '1':
                try:
                    students = get_all_students()
                    print('\nFetching all students...')
                    if students:
                        print('\nList of students:')
                        print('=' * 50)
                        print(f"{'Name':<20} {'Number':<15} {'Quarter':<8}")
                        print('=' * 50)
                        for student in students:
                            print(f"{student[1]:<20} {student[0]:<15} {student[3]:<8}")
                        print('=' * 50 + '\n')
                    else:
                        print('\nNo students found. Please add students first.\n')
                except Exception as e:
                    print(f"\nError retrieving students: {e}\n")

            elif choice == '2':
                try:
                    print("\nAdding new student")
                    print("----------------")
                    name = input('Enter student name: ').strip()
                    number = input('Enter student number: ').strip()
                    quarter = input('Enter student quarter: ').strip()

                    add_student(name, number, quarter)
                    print(f'\nSuccess: Student "{name}" added successfully!\n')

                except ValueError as ve:
                    print(f"\nValidation Error: {ve}\n")
                except Exception as e:
                    print(f"\nError: {e}\n")

            elif choice == '3':
                try:
                    print("\nDeleting student")
                    print("---------------")
                    name = input('Enter student name: ').strip()

                    student = find_student(name)
                    if not student:
                        print(f'\nError: Student "{name}" not found.\n')
                        continue

                    confirm = input(f'Are you sure you want to delete student "{name}"? (yes/no): ').strip().lower()
                    if confirm == 'yes':
                        delete_student(name)
                        print(f'\nSuccess: Student "{name}" deleted successfully!\n')
                    else:
                        print('\nDeletion cancelled.\n')

                except Exception as e:
                    print(f"\nError: {e}\n")

            elif choice == '4':
                try:
                    print("\nFinding student")
                    print("--------------")
                    name = input('Enter student name to find: ').strip()

                    student = find_student(name)
                    if student:
                        print('\nStudent found:')
                        print('=' * 50)
                        print(f"Name    : {student[1]}")
                        print(f"Number  : {student[0]}")
                        print(f"Quarter : {student[3]}")
                        print('=' * 50 + '\n')
                    else:
                        print(f'\nStudent "{name}" not found.\n')

                except Exception as e:
                    print(f"\nError: {e}\n")

            elif choice == '5':
                print('\nThank you for using Student Management System!')
                break

            else:
                print('\nError: Invalid option. Please enter a number between 1 and 5.\n')

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.\n")
        except Exception as e:
            print(f"\nUnexpected error: {e}\n")

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
finally:
    print("\nClosing database connections...")
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("Goodbye!")