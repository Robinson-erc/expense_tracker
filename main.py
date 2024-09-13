import database
import ui

def main():
    database.create_table()  # Ensure the database table exists
    root = ui.create_ui()
    root.mainloop()

if __name__ == "__main__":
    main()
