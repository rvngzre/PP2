import csv
from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
            (username, phone)
        )
        conn.commit()
        print("Contact added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def insert_from_csv():
    filename = input("Enter CSV filename: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    username = row[0].strip()
                    phone = row[1].strip()

                    cur.execute(
                        """
                        INSERT INTO phonebook (username, phone)
                        VALUES (%s, %s)
                        ON CONFLICT (phone) DO NOTHING
                        """,
                        (username, phone)
                    )

        conn.commit()
        print("CSV data imported successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def update_contact():
    print("1. Update username by phone")
    print("2. Update phone by username")
    choice = input("Choose option: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            phone = input("Enter current phone: ")
            new_username = input("Enter new username: ")

            cur.execute(
                "UPDATE phonebook SET username = %s WHERE phone = %s",
                (new_username, phone)
            )

        elif choice == "2":
            username = input("Enter current username: ")
            new_phone = input("Enter new phone: ")

            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE username = %s",
                (new_phone, username)
            )
        else:
            print("Invalid option.")
            cur.close()
            conn.close()
            return

        conn.commit()

        if cur.rowcount == 0:
            print("No contact found.")
        else:
            print("Contact updated successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def query_contacts():
    print("1. Show all contacts")
    print("2. Search by username")
    print("3. Search by phone prefix")
    choice = input("Choose option: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            cur.execute("SELECT * FROM phonebook ORDER BY id")

        elif choice == "2":
            username = input("Enter username: ")
            cur.execute(
                "SELECT * FROM phonebook WHERE username ILIKE %s ORDER BY id",
                (f"%{username}%",)
            )

        elif choice == "3":
            prefix = input("Enter phone prefix: ")
            cur.execute(
                "SELECT * FROM phonebook WHERE phone LIKE %s ORDER BY id",
                (f"{prefix}%",)
            )

        else:
            print("Invalid option.")
            cur.close()
            conn.close()
            return

        rows = cur.fetchall()

        if not rows:
            print("No contacts found.")
        else:
            for row in rows:
                print(f"id={row[0]}, username={row[1]}, phone={row[2]}")

    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def delete_contact():
    print("1. Delete by username")
    print("2. Delete by phone")
    choice = input("Choose option: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            username = input("Enter username: ")
            cur.execute(
                "DELETE FROM phonebook WHERE username = %s",
                (username,)
            )

        elif choice == "2":
            phone = input("Enter phone: ")
            cur.execute(
                "DELETE FROM phonebook WHERE phone = %s",
                (phone,)
            )

        else:
            print("Invalid option.")
            cur.close()
            conn.close()
            return

        conn.commit()

        if cur.rowcount == 0:
            print("No contact found.")
        else:
            print("Contact deleted successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert from console")
        print("3. Insert from CSV")
        print("4. Update contact")
        print("5. Query contacts")
        print("6. Delete contact")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()