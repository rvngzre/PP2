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


def create_db_objects():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
            RETURNS TABLE(contact_id INT, contact_username VARCHAR, contact_phone VARCHAR)
            AS $$
            BEGIN
                RETURN QUERY
                SELECT p.id, p.username, p.phone
                FROM phonebook p
                WHERE p.username ILIKE '%' || p_pattern || '%'
                   OR p.phone ILIKE '%' || p_pattern || '%';
            END;
            $$ LANGUAGE plpgsql;
        """)

        cur.execute("""
            CREATE OR REPLACE PROCEDURE upsert_contact(p_username VARCHAR, p_phone VARCHAR)
            LANGUAGE plpgsql
            AS $$
            BEGIN
                IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_username) THEN
                    UPDATE phonebook
                    SET phone = p_phone
                    WHERE username = p_username;
                ELSE
                    INSERT INTO phonebook(username, phone)
                    VALUES (p_username, p_phone);
                END IF;
            END;
            $$;
        """)

        cur.execute("""
            CREATE OR REPLACE PROCEDURE insert_many_contacts(
                p_usernames TEXT[],
                p_phones TEXT[]
            )
            LANGUAGE plpgsql
            AS $$
            DECLARE
                i INT;
            BEGIN
                IF array_length(p_usernames, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
                    RAISE EXCEPTION 'Arrays must have the same length';
                END IF;

                FOR i IN 1..array_length(p_usernames, 1)
                LOOP
                    IF p_phones[i] ~ '^[0-9]{6,20}$' THEN
                        IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_usernames[i]) THEN
                            UPDATE phonebook
                            SET phone = p_phones[i]
                            WHERE username = p_usernames[i];
                        ELSE
                            BEGIN
                                INSERT INTO phonebook(username, phone)
                                VALUES (p_usernames[i], p_phones[i]);
                            EXCEPTION
                                WHEN unique_violation THEN
                                    RAISE NOTICE 'Skipped duplicate phone: %', p_phones[i];
                            END;
                        END IF;
                    ELSE
                        RAISE NOTICE 'Incorrect data: %, %', p_usernames[i], p_phones[i];
                    END IF;
                END LOOP;
            END;
            $$;
        """)

        cur.execute("""
            CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
            RETURNS TABLE(contact_id INT, contact_username VARCHAR, contact_phone VARCHAR)
            AS $$
            BEGIN
                RETURN QUERY
                SELECT p.id, p.username, p.phone
                FROM phonebook p
                ORDER BY p.id
                LIMIT p_limit OFFSET p_offset;
            END;
            $$ LANGUAGE plpgsql;
        """)

        cur.execute("""
            CREATE OR REPLACE PROCEDURE delete_contact_by_value(p_value VARCHAR)
            LANGUAGE plpgsql
            AS $$
            BEGIN
                DELETE FROM phonebook
                WHERE username = p_value OR phone = p_value;
            END;
            $$;
        """)

        conn.commit()
        print("Functions and procedures created successfully.")

    except Exception as e:
        conn.rollback()
        print("Error while creating DB objects:", e)

    cur.close()
    conn.close()


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL upsert_contact(%s, %s)", (username, phone))
        conn.commit()
        print("Contact added/updated successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def insert_from_csv():
    filename = input("Enter CSV filename: ")

    usernames = []
    phones = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    usernames.append(row[0].strip())
                    phones.append(row[1].strip())
    except Exception as e:
        print("Error while reading CSV:", e)
        return

    if not usernames:
        print("No valid data found in CSV.")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL insert_many_contacts(%s, %s)", (usernames, phones))
        conn.commit()
        print("CSV data processed successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def update_contact():
    username = input("Enter username to update or insert: ")
    phone = input("Enter new phone: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL upsert_contact(%s, %s)", (username, phone))
        conn.commit()
        print("Contact inserted/updated successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def query_contacts():
    print("1. Show all contacts")
    print("2. Search by pattern")
    print("3. Search by phone prefix")
    print("4. Show paginated contacts")
    choice = input("Choose option: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            cur.execute("SELECT * FROM phonebook ORDER BY id")

        elif choice == "2":
            pattern = input("Enter pattern: ")
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))

        elif choice == "3":
            prefix = input("Enter phone prefix: ")
            cur.execute(
                "SELECT * FROM phonebook WHERE phone LIKE %s ORDER BY id",
                (f"{prefix}%",)
            )

        elif choice == "4":
            limit = int(input("Enter limit: "))
            offset = int(input("Enter offset: "))
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))

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
    value = input("Enter username or phone: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL delete_contact_by_value(%s)", (value,))
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
        print("2. Create functions and procedures")
        print("3. Insert from console")
        print("4. Insert from CSV")
        print("5. Update/Insert contact")
        print("6. Query contacts")
        print("7. Delete contact")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            create_db_objects()
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            insert_from_csv()
        elif choice == "5":
            update_contact()
        elif choice == "6":
            query_contacts()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()