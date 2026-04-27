import csv
import json
import os
from connect import get_connection

VALID_PHONE_TYPES = {"home", "work", "mobile"}

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def normalize_phone_type(value: str) -> str:
    value = (value or "").strip().lower()
    return value if value in VALID_PHONE_TYPES else "mobile"

def get_or_create_group(cur, group_name: str) -> int:
    group_name = (group_name or "Other").strip() or "Other"
    cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (group_name,))
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    row = cur.fetchone()
    return row[0]

def insert_contact(cur, name, email=None, birthday=None, group_name="Other"):
    group_id = get_or_create_group(cur, group_name)
    cur.execute(
        """
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (name, email, birthday or None, group_id),
    )
    return cur.fetchone()[0]

def add_phone_row(cur, contact_id, phone, phone_type="mobile"):
    if not phone:
        return
    cur.execute(
        """
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
        ON CONFLICT (contact_id, phone) DO NOTHING
        """,
        (contact_id, phone.strip(), normalize_phone_type(phone_type)),
    )

# --- ОСНОВНЫЕ ФУНКЦИИ ---

def add_contact_interactive():
    name = input("Name: ").strip()
    if not name:
        print("Name is required.")
        return

    email = input("Email (optional): ").strip() or None
    birthday = input("Birthday YYYY-MM-DD (optional): ").strip() or None
    group_name = input("Group: ").strip() or "Other"

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        if cur.fetchone():
            print(f"Contact '{name}' already exists.")
            return

        contact_id = insert_contact(cur, name, email, birthday, group_name)

        while True:
            phone = input("Phone (leave empty to stop): ").strip()
            if not phone: break
            phone_type = input("Type (home/work/mobile): ").strip()
            add_phone_row(cur, contact_id, phone, phone_type)

        conn.commit()
        print("Contact added successfully!")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def search_contacts_advanced():
    query = input("Search text (name/email/phone): ").strip()
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Здесь вызывается SQL-функция из procedures.sql
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()
        if not rows:
            print("No results found.")
        else:
            for r in rows:
                print(f"ID:{r[0]} | {r[1]} | Email:{r[2]} | Group:{r[4]} | Phones:{r[5]}")
    except Exception as e:
        print("Error: Make sure you ran 'Init DB' first. Details:", e)
    finally:
        cur.close()
        conn.close()

def browse_with_filters():
    sort_key = input("Sort by (name/birthday/id): ").strip().lower() or "name"
    page_size = 5
    page = 0

    order_map = {"name": "c.name", "birthday": "c.birthday", "id": "c.id"}
    sort_col = order_map.get(sort_key, "c.name")

    while True:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM contacts")
            total = cur.fetchone()[0]
            total_pages = (total + page_size - 1) // page_size

            cur.execute(f"""
                SELECT c.id, c.name, c.email, g.name, 
                       COALESCE(STRING_AGG(p.phone, ', '), 'No phones')
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                LEFT JOIN phones p ON p.contact_id = c.id
                GROUP BY c.id, g.name
                ORDER BY {sort_col} LIMIT %s OFFSET %s
            """, (page_size, page * page_size))
            
            rows = cur.fetchall()
            print(f"\n--- Page {page + 1}/{max(total_pages, 1)} ---")
            for r in rows:
                print(f"[{r[0]}] {r[1]} | {r[2]} | {r[3]} | {r[4]}")

            cmd = input("\n[n]ext, [p]rev, [q]uit: ").lower().strip()
            if cmd == 'n' and page + 1 < total_pages: page += 1
            elif cmd == 'p' and page > 0: page -= 1
            elif cmd == 'q': break
        finally:
            cur.close()
            conn.close()

def export_to_json():
    filename = "contacts_export.json"
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, email, birthday FROM contacts")
        rows = cur.fetchall()
        data = []
        for r in rows:
            cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (r[0],))
            phones = [{"phone": p[0], "type": p[1]} for p in cur.fetchall()]
            data.append({"name": r[1], "email": r[2], "birthday": str(r[3]), "phones": phones})
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Exported to {filename}")
    finally:
        cur.close()
        conn.close()

# --- СИСТЕМНЫЕ ФУНКЦИИ ---

def run_sql_file(filename):
    if not os.path.exists(filename):
        print(f"CRITICAL ERROR: File '{filename}' not found in current folder!")
        return False
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(filename, "r", encoding="utf-8") as f:
            cur.execute(f.read())
        conn.commit()
        print(f"Successfully executed {filename}")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error in {filename}: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def init_db():
    print("Initializing database...")
    if run_sql_file("schema.sql"):
        run_sql_file("procedures.sql")
        print("Database setup complete.")

# --- МЕНЮ ---

def menu():
    while True:
        # Очистка экрана (опционально)
        # os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n============================")
        print("   PHONEBOOK SYSTEM v2.0")
        print("============================")
        print("1. Init Database (SQL)")
        print("2. Add New Contact")
        print("3. Search (Function)")
        print("4. Browse (Pagination)")
        print("5. Export to JSON")
        print("0. Exit")
        print("----------------------------")

        choice = input("Choose option: ").strip()

        if choice == "1":
            init_db()
        elif choice == "2":
            add_contact_interactive()
        elif choice == "3":
            search_contacts_advanced()
        elif choice == "4":
            browse_with_filters()
        elif choice == "5":
            export_to_json()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")
        
        
        input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    menu()