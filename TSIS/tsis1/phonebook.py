import csv
import json
from connect import get_connection


def close_connection(conn, cur):
    cur.close()
    conn.close()


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            )
        """)

        cur.execute("""
            INSERT INTO groups(name)
            VALUES ('Family'), ('Work'), ('Friend'), ('Other')
            ON CONFLICT (name) DO NOTHING
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100),
                birthday DATE,
                group_id INTEGER REFERENCES groups(id),
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            ALTER TABLE contacts
            ADD COLUMN IF NOT EXISTS date_added
            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
                phone VARCHAR(20) NOT NULL,
                type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
            )
        """)

        conn.commit()
        print("Tables created successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    close_connection(conn, cur)


def create_db_objects():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DROP FUNCTION IF EXISTS search_contacts(TEXT)")

        cur.execute("""
            CREATE OR REPLACE PROCEDURE add_phone(
                p_contact_name VARCHAR,
                p_phone VARCHAR,
                p_type VARCHAR
            )
            LANGUAGE plpgsql
            AS $$
            DECLARE
                v_contact_id INT;
            BEGIN
                SELECT id INTO v_contact_id
                FROM contacts
                WHERE username = p_contact_name;

                IF v_contact_id IS NULL THEN
                    RAISE EXCEPTION 'Contact not found';
                END IF;

                INSERT INTO phones(contact_id, phone, type)
                VALUES (v_contact_id, p_phone, p_type);
            END;
            $$;
        """)

        cur.execute("""
            CREATE OR REPLACE PROCEDURE move_to_group(
                p_contact_name VARCHAR,
                p_group_name VARCHAR
            )
            LANGUAGE plpgsql
            AS $$
            DECLARE
                v_group_id INT;
            BEGIN
                INSERT INTO groups(name)
                VALUES (p_group_name)
                ON CONFLICT (name) DO NOTHING;

                SELECT id INTO v_group_id
                FROM groups
                WHERE name = p_group_name;

                UPDATE contacts
                SET group_id = v_group_id
                WHERE username = p_contact_name;
            END;
            $$;
        """)

        cur.execute("""
            CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
            RETURNS TABLE(
                contact_id INT,
                contact_username VARCHAR,
                contact_email VARCHAR,
                contact_birthday DATE,
                contact_group VARCHAR,
                contact_phone VARCHAR,
                phone_type VARCHAR
            )
            AS $$
            BEGIN
                RETURN QUERY
                SELECT 
                    c.id,
                    c.username,
                    c.email,
                    c.birthday,
                    g.name,
                    p.phone,
                    p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE c.username ILIKE '%' || p_query || '%'
                   OR c.email ILIKE '%' || p_query || '%'
                   OR p.phone ILIKE '%' || p_query || '%'
                   OR g.name ILIKE '%' || p_query || '%'
                ORDER BY c.id;
            END;
            $$ LANGUAGE plpgsql;
        """)

        conn.commit()
        print("Functions and procedures created successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    close_connection(conn, cur)


def insert_or_update_contact():
    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    birthday = input("Enter birthday YYYY-MM-DD: ").strip()
    group_name = input("Enter group: ").strip()
    phone = input("Enter phone: ").strip()
    phone_type = input("Enter phone type home/work/mobile: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO groups(name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (group_name,))

        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
        group_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO contacts(username, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username)
            DO UPDATE SET
                email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
            RETURNING id
        """, (username, email, birthday, group_id))

        contact_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (contact_id, phone, phone_type))

        conn.commit()
        print("Contact inserted or updated successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    close_connection(conn, cur)


def add_phone_to_contact():
    username = input("Enter contact username: ").strip()
    phone = input("Enter new phone: ").strip()
    phone_type = input("Enter phone type home/work/mobile: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL add_phone(%s::VARCHAR, %s::VARCHAR, %s::VARCHAR)",
            (username, phone, phone_type)
        )

        conn.commit()
        print("Phone added successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    close_connection(conn, cur)


def move_contact_to_group():
    username = input("Enter contact username: ").strip()
    group_name = input("Enter new group: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL move_to_group(%s::VARCHAR, %s::VARCHAR)",
            (username, group_name)
        )

        conn.commit()
        print("Contact moved to group successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    close_connection(conn, cur)


def import_from_csv():
    filename = input("Enter CSV filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                username = row["username"].strip()
                email = row["email"].strip()
                birthday = row["birthday"].strip()
                group_name = row["group"].strip()
                phone = row["phone"].strip()
                phone_type = row["type"].strip()

                cur.execute("""
                    INSERT INTO groups(name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                """, (group_name,))

                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                group_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO contacts(username, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (username)
                    DO UPDATE SET
                        email = EXCLUDED.email,
                        birthday = EXCLUDED.birthday,
                        group_id = EXCLUDED.group_id
                    RETURNING id
                """, (username, email, birthday, group_id))

                contact_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, phone, phone_type))

        conn.commit()
        print("CSV imported successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    close_connection(conn, cur)


def export_to_json():
    filename = input("Enter JSON filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                c.id,
                c.username,
                c.email,
                c.birthday,
                g.name,
                c.date_added
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
        """)

        contacts = []

        for row in cur.fetchall():
            contact_id = row[0]

            cur.execute("""
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s
            """, (contact_id,))

            phones = []

            for phone_row in cur.fetchall():
                phones.append({
                    "phone": phone_row[0],
                    "type": phone_row[1]
                })

            contacts.append({
                "username": row[1],
                "email": row[2],
                "birthday": row[3].strftime("%Y-%m-%d") if row[3] else None,
                "group": row[4],
                "date_added": str(row[5]),
                "phones": phones
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4)

        print("Exported to JSON successfully.")

    except Exception as e:
        print("Error:", e)

    close_connection(conn, cur)


def import_from_json():
    filename = input("Enter JSON filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            contacts = json.load(file)

        for contact in contacts:
            username = contact["username"]
            email = contact["email"]
            birthday = contact["birthday"]
            group_name = contact["group"]

            cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
            existing = cur.fetchone()

            if existing:
                choice = input(f"{username} already exists. skip/overwrite: ").strip().lower()

                if choice == "skip":
                    continue

                cur.execute("DELETE FROM contacts WHERE username = %s", (username,))

            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (group_name,))

            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(username, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (username, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

            for phone in contact["phones"]:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, phone["phone"], phone["type"]))

        conn.commit()
        print("JSON imported successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    close_connection(conn, cur)


def print_rows(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        row = list(row)

        if len(row) > 3 and row[3] is not None:
            row[3] = row[3].strftime("%Y-%m-%d")

        print(tuple(row))


def query_contacts():
    print("1. Show all")
    print("2. Search by name/email/phone/group")
    print("3. Filter by group")
    print("4. Sort by name")
    print("5. Sort by birthday")
    print("6. Sort by date added")
    print("7. Paginated navigation")

    choice = input("Choose option: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                ORDER BY c.id
            """)

            print_rows(cur.fetchall())

        elif choice == "2":
            query = input("Enter search query: ").strip()
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            print_rows(cur.fetchall())

        elif choice == "3":
            group_name = input("Enter group: ").strip()

            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE g.name = %s
                ORDER BY c.id
            """, (group_name,))

            print_rows(cur.fetchall())

        elif choice == "4":
            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                ORDER BY c.username
            """)

            print_rows(cur.fetchall())

        elif choice == "5":
            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                ORDER BY c.birthday
            """)

            print_rows(cur.fetchall())

        elif choice == "6":
            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                ORDER BY c.date_added
            """)

            print_rows(cur.fetchall())

        elif choice == "7":
            limit = int(input("Enter page size: "))
            offset = 0

            while True:
                cur.execute("""
                    SELECT c.id, c.username, c.email, c.birthday, g.name, p.phone, p.type
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    LEFT JOIN phones p ON c.id = p.contact_id
                    ORDER BY c.id
                    LIMIT %s OFFSET %s
                """, (limit, offset))

                rows = cur.fetchall()
                print_rows(rows)

                command = input("next/prev/quit: ").strip().lower()

                if command == "next":
                    offset += limit

                elif command == "prev":
                    offset = max(0, offset - limit)

                elif command == "quit":
                    break

                else:
                    print("Invalid command.")

        else:
            print("Invalid option.")

    except Exception as e:
        print("Error:", e)

    close_connection(conn, cur)


def delete_contact():
    value = input("Enter username, email or phone: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT DISTINCT c.id
            FROM contacts c
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.username = %s
               OR c.email = %s
               OR p.phone = %s
        """, (value, value, value))

        rows = cur.fetchall()

        if not rows:
            print("No contact found.")

        else:
            for row in rows:
                cur.execute("DELETE FROM contacts WHERE id = %s", (row[0],))

            conn.commit()
            print("Contact deleted successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    close_connection(conn, cur)


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create tables")
        print("2. Create functions and procedures")
        print("3. Insert or update contact")
        print("4. Add phone to contact")
        print("5. Move contact to group")
        print("6. Import from CSV")
        print("7. Export to JSON")
        print("8. Import from JSON")
        print("9. Query contacts")
        print("10. Delete contact")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_tables()

        elif choice == "2":
            create_db_objects()

        elif choice == "3":
            insert_or_update_contact()

        elif choice == "4":
            add_phone_to_contact()

        elif choice == "5":
            move_contact_to_group()

        elif choice == "6":
            import_from_csv()

        elif choice == "7":
            export_to_json()

        elif choice == "8":
            import_from_json()

        elif choice == "9":
            query_contacts()

        elif choice == "10":
            delete_contact()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()