import tkinter as tk
from tkinter import messagebox
import database
from tkinter import ttk

budget = 0  # Global variable to store the budget

def set_budget():
    global budget
    budget = entry_budget.get()
    if budget:
        try:
            budget = float(budget)
            total_expenses = sum(expense[2] for expense in database.get_expenses())  # Assuming amount is the third element
            remaining_budget = budget - total_expenses
            messagebox.showinfo("Success", f"Budget set successfully. Remaining budget: {remaining_budget}")
            entry_budget.config(state=tk.DISABLED)
            button_set_budget.config(state=tk.DISABLED)
            enable_expense_entries()
            label_remaining_budget.config(text=f"Remaining Budget: {remaining_budget}")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for the budget")
    else:
        messagebox.showwarning("Input Error", "Please enter a budget")

def enable_expense_entries():
    entry_name.config(state=tk.NORMAL)
    entry_amount.config(state=tk.NORMAL)
    entry_date.config(state=tk.NORMAL)
    entry_category.config(state="readonly")  # Ensure the combobox is enabled
    button_add_expense.config(state=tk.NORMAL)

def add_expense():
    global budget
    name = entry_name.get()
    amount = entry_amount.get()
    date = entry_date.get()
    category = entry_category.get()
    if name and amount and date and category:
        try:
            amount = float(amount)
            total_expenses = sum(expense[2] for expense in database.get_expenses())  # Assuming amount is the third element
            remaining_budget = budget - total_expenses
            if amount > remaining_budget:
                messagebox.showwarning("Budget Exceeded", "Expense exceeds the remaining budget")
                return
            database.add_expense(name, amount, date, category)
            remaining_budget -= amount
            messagebox.showinfo("Success", "Expense added successfully")
            entry_name.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            entry_date.delete(0, tk.END)
            entry_category.set('')  # Clear category selection
            display_expenses()
            label_remaining_budget.config(text=f"Remaining Budget: {remaining_budget}")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for the amount")
    else:
        messagebox.showwarning("Input Error", "Please fill out all fields")

def clear_expenses():
    for widget in frame_expenses.winfo_children():
        widget.destroy()

def delete_expense():
    selected_expense = listbox_expenses.curselection()
    if selected_expense:
        expense_id = listbox_expenses.get(selected_expense).split()[0]  # Assuming the ID is the first element
        database.delete_expense(expense_id)
        messagebox.showinfo("Success", "Expense deleted successfully")
        display_expenses()
    else:
        messagebox.showwarning("Input Error", "Please select an expense to delete")

def display_expenses():
    listbox_expenses.delete(0, tk.END)
    expenses = database.get_expenses()
    for row in expenses:
        listbox_expenses.insert(tk.END, f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}")  # Adjust format as needed

def create_ui():
    root = tk.Tk()
    root.title("Expense Tracker")

    global entry_budget, button_set_budget, frame_expenses, entry_name, entry_amount, entry_date, entry_category, listbox_expenses, label_remaining_budget, button_add_expense

    # Budget Entry
    tk.Label(root, text="Budget").grid(row=0)
    entry_budget = tk.Entry(root)
    entry_budget.grid(row=0, column=1)
    button_set_budget = tk.Button(root, text="Set Budget", command=set_budget)
    button_set_budget.grid(row=0, column=2)

    # Expense Entry
    tk.Label(root, text="Name").grid(row=1)
    tk.Label(root, text="Amount").grid(row=2)
    tk.Label(root, text="Date").grid(row=3)
    tk.Label(root, text="Category").grid(row=4)

    entry_name = tk.Entry(root, state=tk.DISABLED)
    entry_amount = tk.Entry(root, state=tk.DISABLED)
    entry_date = tk.Entry(root, state=tk.DISABLED)

    entry_name.grid(row=1, column=1)
    entry_amount.grid(row=2, column=1)
    entry_date.grid(row=3, column=1)

    # Category Combobox
    categories = ['Housing', 'Entertainment', 'Food', 'Transportation', 'Utilities', 'Insurance', 'Healthcare', 'Miscellaneous']
    entry_category = ttk.Combobox(root, values=categories, state="readonly")
    entry_category.grid(row=4, column=1)

    # Add and Clear Expense buttons
    button_add_expense = tk.Button(root, text="Add Expense", command=add_expense, state=tk.DISABLED)
    button_add_expense.grid(row=5, columnspan=2)
    tk.Button(root, text="Delete Expense", command=delete_expense).grid(row=6, columnspan=2)
    tk.Button(root, text="Clear Expenses", command=clear_expenses).grid(row=8, columnspan=2)

    # Expense Listbox
    frame_expenses = tk.Frame(root)
    frame_expenses.grid(row=7, columnspan=2)

    listbox_expenses = tk.Listbox(frame_expenses, width=50, height=10)
    listbox_expenses.pack()

    # Remaining Budget Label
    label_remaining_budget = tk.Label(root, text="Remaining Budget: 0")
    label_remaining_budget.grid(row=9, columnspan=2)

    display_expenses()

    return root

if __name__ == "__main__":
    app = create_ui()
    app.mainloop()
