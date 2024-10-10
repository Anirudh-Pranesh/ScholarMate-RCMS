import tkinter as tk
from tkinter import ttk
import sv_ttk
import mysql.connector


# DATABASE CONNECTION
db = mysql.connector.connect(
    host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', 
    port=13426, 
    user='avnadmin', 
    password='AVNS_1UgkIMxSzsCWt0D-3cB', 
    database='scholarmate_db'
)  # Aiven connection


def get_tables():
    # Fetch list of tables in the database
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    res = cursor.fetchall()
    res = list(filter(lambda x: x not in [('credentials',), ('student_details',), ('teacher_details',)], res))
    cursor.close()
    return res


def fetch_table_data(table_name):
    # Fetch all data from the selected table
    cursor = db.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]  # Get column names
    cursor.close()
    return column_names, data


def display_table_data(column_names, data):
    # Clear existing Treeview content
    for row in tree.get_children():
        tree.delete(row)

    # Update Treeview with new data
    tree["columns"] = column_names
    tree["show"] = "headings"

    # Configure column headings
    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)  # Adjust width as needed

    # Insert rows into Treeview
    for row in data:
        tree.insert("", "end", values=row)


def on_table_select(event):
    selected_table = table_combo.get()
    column_names, data = fetch_table_data(selected_table)
    display_table_data(column_names, data)


# Create window
window = tk.Tk()
window.title('Database Table Viewer')
window.geometry('800x600')

# Welcome label
welcome_label = ttk.Label(window, text='Select a table to view:', font=('Arial', 16))
welcome_label.pack(pady=20)

# Dropdown for table selection
tables = get_tables()
table_combo = ttk.Combobox(window, values=tables, font=('Arial', 14), state='readonly')
table_combo.pack(pady=10)
table_combo.bind("<<ComboboxSelected>>", on_table_select)

# Scrollable frame
tree_frame = ttk.Frame(window)
tree_frame.pack(pady=10, padx=10, fill='both', expand=True)

# Treeview (table) widget
tree = ttk.Treeview(tree_frame)
tree.pack(side="left", fill="both", expand=True)

# Scrollbar for Treeview
tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_scrollbar.set)
tree_scrollbar.pack(side="right", fill="y")

# Set dark theme
sv_ttk.set_theme("dark")

# Run the application
window.mainloop()

# Close the database connection when done
db.close()
