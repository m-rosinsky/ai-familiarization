import sqlite3

def init_db():
    conn = sqlite3.connect("warehouse.db")
    cursor = conn.cursor()
    
    # Create inventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE NOT NULL,
            quantity INTEGER NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    
    # Seed data
    items = [
        ('hammers', 45, 'Aisle 3A'),
        ('screwdrivers', 120, 'Aisle 3B'),
        ('screws (100pk)', 350, 'Aisle 5'),
        ('measuring tapes', 18, 'Aisle 2A')
    ]
    
    try:
        cursor.executemany('INSERT OR IGNORE INTO inventory (item_name, quantity, location) VALUES (?, ?, ?)', items)
        conn.commit()
        print("Database initialized successfully with inventory data!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
