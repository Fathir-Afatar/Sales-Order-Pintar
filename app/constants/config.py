import sqlite3

DB_PATH = "C:/Users/Fathir/Documents/pos-pintar-by-fathir/data/pos.db"

def get_connection():
    return sqlite3.connect(DB_PATH)