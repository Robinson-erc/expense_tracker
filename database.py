import sqlite3

def connect_db():
    conn = sqlite3.connect('expenses.db')
    return conn

def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY, name TEXT, amount REAL, date TEXT, category TEXT)''')
    conn.commit()
    conn.close()

def add_expense(name, amount, date, category):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO expenses (name, amount, date, category) VALUES (?, ?, ?, ?)",
              (name, float(amount), date, category))
    conn.commit()
    conn.close()

def get_expenses():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()
    return expenses
