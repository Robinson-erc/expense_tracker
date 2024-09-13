import tkinter as tk
from tkinter import messagebox
import database

def add_expense():
    name = entry_name.get()
    amount = entry_amount.get()
    date = entry_date.get()
    category = entry_category.get()
    if name and amount and date and category:
        database.add_expense(name, amount, date, category)
        messagebox.showinfo("Success", "Expense added successfully")
        entry_name.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        display_expenses()
    else:
        messagebox.showwarning("Input Error", "Please fill out all fields")

def clear_expenses():
    for widget in frame_expenses.winfo_children():
        widget.destroy()

def display_expenses():
    for widget in frame_expenses.winfo_children():
        widget.destroy()
    expenses = database.get_expenses()
    for row in expenses:
        tk.Label(frame_expenses, text=row).pack()

def create_ui():
    root = tk.Tk()
    root.title("Expense Tracker")

    tk.Label(root, text="Name").grid(row=0)
    tk.Label(root, text="Amount").grid(row=1)
    tk.Label(root, text="Date").grid(row=2)
    tk.Label(root, text="Category").grid(row=3)

    global entry_name, entry_amount, entry_date, entry_category
    entry_name = tk.Entry(root)
    entry_amount = tk.Entry(root)
    entry_date = tk.Entry(root)
    entry_category = tk.Entry(root)

    entry_name.grid(row=0, column=1)
    entry_amount.grid(row=1, column=1)
    entry_date.grid(row=2, column=1)
    entry_category.grid(row=3, column=1)

    tk.Button(root, text="Add Expense", command=add_expense).grid(row=4, columnspan=2)
    tk.Button(root, text="Clear Expenses", command=clear_expenses).grid(row=6, columnspan=2)

    global frame_expenses
    frame_expenses = tk.Frame(root)
    frame_expenses.grid(row=5, columnspan=2)

    display_expenses()

    return root

