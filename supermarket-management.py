# ----------------- SUPERMARKET MANAGEMENT SYSTEM --------------------
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# ---------- Basic Functions ----------
def get_all_items():
    cur.execute("SELECT * FROM items")
    return cur.fetchall()

def add_item(name, price, quantity):
    cur.execute("INSERT INTO items (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
    conn.commit()

def update_item_quantity(name, quantity):
    cur.execute("UPDATE items SET quantity = %s WHERE LOWER(name) = LOWER(%s)", (quantity, name))
    conn.commit()

def search_item(name):
    cur.execute("SELECT * FROM items WHERE LOWER(name) = LOWER(%s)", (name,))
    return cur.fetchone()

def edit_item(name, new_name, new_price, new_quantity):
    cur.execute("UPDATE items SET name = %s, price = %s, quantity = %s WHERE LOWER(name) = LOWER(%s)",
                (new_name, new_price, new_quantity, name))
    conn.commit()

# ---------- Utilities ----------
def display_items(items):
    if items:
        for item in items:
            print(f"Name: {item[1]}, Price: ${item[3]:.2f}, Quantity: {item[2]}")
    else:
        print('No items found. Please add items first.')

def prompt_float(prompt, default=None):
    value = input(prompt)
    if not value and default is not None:
        return default
    return float(value)

def prompt_int(prompt, default=None):
    value = input(prompt)
    if not value and default is not None:
        return default
    return int(value)

# ---------- Main cycle ----------
while True:
    input('Press Enter to continue...')
    print('\n------------------ Welcome to the Supermarket ------------------')
    print('1. View items\n2. Add items\n3. Purchase items\n4. Search items\n5. Edit items\n6. Exit')
    choice = input('Enter your choice (1-6): ').strip()

    if choice == '1':
        print('\n------------------ View Items ------------------')
        display_items(get_all_items())

    elif choice == '2':
        print('\n------------------ Add Item ------------------')
        name = input('Enter item name: ').strip()
        try:
            price = prompt_float('Enter item price: ')
            quantity = prompt_int('Enter item quantity: ')
            add_item(name, price, quantity)
            print(f'Item "{name}" added successfully.')
        except ValueError:
            print('Invalid input. Please enter valid numbers for price and quantity.')

    elif choice == '3':
        print('\n------------------ Purchase Item ------------------')
        items = get_all_items()
        display_items(items)

        name = input('Enter the name of the item to purchase: ').strip()
        item = search_item(name)
        if item:
            _, item_name, price, quantity = item
            if quantity > 0:
                print(f'Price: ${price:.2f}. Proceeding with the purchase...')
                update_item_quantity(name, quantity - 1)
                print(f'Success! Remaining stock for "{item_name}": {quantity - 1}')
            else:
                print('Item is out of stock.')
        else:
            print('Item not found.')

    elif choice == '4':
        print('\n------------------ Search Item ------------------')
        name = input('Enter item name to search: ').strip()
        item = search_item(name)
        if item:
            print(f'Item found: Name: {item[1]}, Price: ${item[2]:.2f}, Quantity: {item[3]}')
        else:
            print('Item not found.')

    elif choice == '5':
        print('\n------------------ Edit Item ------------------')
        name = input('Enter the name of the item to edit: ').strip()
        item = search_item(name)
        if item:
            _, current_name, current_price, current_quantity = item
            print(f'Editing "{current_name}" — Price: ${current_price:.2f}, Quantity: {current_quantity}')

            new_name = input('New name (or Enter to keep current): ').strip() or current_name
            try:
                new_price = prompt_float('New price (or Enter to keep current): ', current_price)
                new_quantity = prompt_int('New quantity (or Enter to keep current): ', current_quantity)
                edit_item(name, new_name, new_price, new_quantity)
                print(f'Item updated: {new_name}')
            except ValueError:
                print('Invalid input. Update cancelled.')
        else:
            print('Item not found.')

    elif choice == '6':
        print('\nExiting... Goodbye!')
        break

    else:
        print('Invalid choice. Please enter a number between 1 and 6.')

# ---------- Closing connection ----------
cur.close()
conn.close()











