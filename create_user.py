import sqlite3
import hashlib
import secrets
import getpass
import pathlib

DB_PATH = pathlib.Path(__file__).parent / 'library.db'

def generate_hash(password):
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        100000
        )
    return f"{salt.hex()}:{key.hex()}"

def create_user(username, password):
    password = generate_hash(password)
    
    db_path = pathlib.Path(__file__).parent / 'library.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    
    # Create uauth table for users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uauth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Create uauth_cookies table for multiple cookies per user
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uauth_cookies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            cookie TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES uauth(id)
        )
    """)
    cursor.execute(
        'INSERT INTO uauth (username, password) VALUES (?, ?)', 
        (username, password)
        )

    conn.commit()
    conn.close()
    