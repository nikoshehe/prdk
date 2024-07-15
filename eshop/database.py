import sqlite3
import os

DB_PATH = 'database.db'

def initialize_database():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO Product (name, price) VALUES (?, ?)
        ''', ('DUB', 2599))
        conn.commit()
        conn.close()

def get_product():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Product WHERE id = 1')
    Product = cursor.fetchone()
    conn.close()
    return Product