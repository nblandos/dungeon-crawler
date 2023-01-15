import pygame
import hashlib
import sqlite3


class LoginSystem:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''')
        self.conn.commit()

    def encrypt_password(self, password):
        # Encrypt the password using SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password):
        password = self.encrypt_password(password)
        try:
            self.cursor.execute("INSERT INTO users (username,password) VALUES (?,?)", (username, password))
            self.conn.commit()
            print(f"{username} added to the system!")
            return True
        except sqlite3.IntegrityError as e:
            print("Error: User already exists")
            return False

    def check_user(self, username, password):
        password = self.encrypt_password(password)
        self.cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        if self.cursor.fetchone():
            return True
        return False
