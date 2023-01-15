import tkinter as tk
from tkinter import messagebox as mb
import hashlib
import sqlite3


class LoginSystem:
    def __init__(self):
        self.logged_in = False
        self.con = sqlite3.connect('users.db')
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL,"
                            "password TEXT NOT NULL, highscore INTEGER DEFAULT 0)")
        self.con.commit()
        self.root = tk.Tk()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.registration_frame = None
        self.header = None
        self.widgets()
        self.root.mainloop()

    def widgets(self):
        self.root.title('Registration')
        self.root.geometry('600x300')
        self.root.resizable(False, False)
        self.header = tk.Label(self.root, text='Registration', font=("Arial", 32))
        self.header.pack()
        self.registration_frame = tk.Frame(self.root, padx=40, pady=10)
        tk.Label(self.registration_frame, text='Username:', font=("Arial", 20), padx=40, pady=15).grid()
        tk.Entry(self.registration_frame, textvariable=self.username, bd=5, font=("Arial", 15)).grid(row=0, column=1)
        tk.Label(self.registration_frame, text='Password:', font=("Arial", 20), padx=40, pady=15).grid()
        tk.Entry(self.registration_frame, textvariable=self.password, bd=5, font=("Arial", 15), show='*').grid(row=1, column=1)
        tk.Button(self.registration_frame, text=' Login ', bd=3, font=("Arial", 15), padx=5, pady=5,
                  command=self.login).grid()
        tk.Button(self.registration_frame, text=' Register ', bd=3, font=("Arial", 15), padx=5, pady=5,
                  command=self.register).grid(row=2, column=1)
        self.registration_frame.pack(fill="both", expand=True)

    def login(self):
        username = self.username.get()
        password = self.password.get()
        self.cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        if self.cursor.fetchone():
            self.logged_in = True
            self.root.destroy()
        else:
            if not username or not password:
                mb.showerror("Error", "Username or Password fields are blank.")
            else:
                mb.showerror("Error", "Account details do not exist.")

    def register(self):
        username = self.username.get()
        password = self.password.get()
        if not username or not password:
            mb.showerror("Error", "Username or password fields are blank.")
        else:
            try:
                self.cursor.execute("INSERT INTO users(username,password) VALUES (?,?)", (username, password))
                self.con.commit()
                mb.showinfo("Success", "Account created successfully.")
                self.login()
            except sqlite3.IntegrityError:
                mb.showerror("Error", "Username already exists.")



