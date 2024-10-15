import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# DATABASE CONNECTION
db = mysql.connector.connect(
    host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com',
    port=13426,
    user='avnadmin',
    password='AVNS_1UgkIMxSzsCWt0D-3cB',
    database='scholarmate_db'
)

# Handle window close event to release resources and close DB connection
def on_close():
    try:
        db.close()
    except:
        pass
    root.destroy()

# Fetch tables from the database
def get_tables():
    try:
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        res = cursor.fetchall()
        res = list(filter(lambda x: x not in [('credentials',), ('student_details',), ('teacher_details',)], res))
        cursor.close()
        return [table[0] for table in res]
    except mysql.connector.Error as err:
        print(f"Error fetching tables: {err}")
        return []

# Fetch data from a specified table
def fetch_table_data(table_name):
    try:
        cursor = db.cursor()
        query = f"SELECT * FROM `{table_name}` ORDER BY `class`, `student_name`"
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        cursor.close()
        return column_names, data
    except mysql.connector.Error as err:
        print(f"Error fetching table data: {err}")
        return [], []

# Display data in the Treeview
def display_table_data(column_names, data):
    for row in treeview.get_children():
        treeview.delete(row)
    treeview["columns"] = column_names
    treeview["show"] = "headings"
    for col in column_names:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center", width=150)
    for row in data:
        treeview.insert("", "end", values=row)

# In-place editing on double-click
edit_entries = {}

def on_double_click(event):
    selected_item = treeview.focus()
    column = treeview.identify_column(event.x)

    if selected_item and column:
        # Get the column index (1-based)
        col_index = int(column[1]) - 1  # Convert to zero-based index

        # Lock editing for the first three columns
        if col_index < 3:  # Adjust this condition based on your requirements
            messagebox.showinfo("Locked Column", "Editing is not allowed for this column.")
            return
        
        # Get the bounds of the cell
        bbox = treeview.bbox(selected_item, column)
        if bbox:
            current_value = treeview.item(selected_item, 'values')[col_index]

            # If an entry already exists for this cell, focus on it
            if (selected_item, column) in edit_entries:
                edit_entries[(selected_item, column)].focus()
                return

            # Create Entry widget and position it over the cell
            entry = tk.Entry(root)
            entry.place(x=bbox[0] + treeview.winfo_x(), y=bbox[1] + treeview.winfo_y(), width=bbox[2], height=bbox[3])
            entry.insert(0, current_value)
            entry.focus()

            # Bind events to save or cancel
            entry.bind("<Return>", lambda e: save_value(selected_item, col_index, entry))
            entry.bind("<FocusOut>", lambda e: cancel_edit(selected_item, column))

            edit_entries[(selected_item, column)] = entry

def save_value(selected_item, col_index, entry):
    new_value = entry.get()
    values = list(treeview.item(selected_item, 'values'))
    values[col_index] = new_value

    # Use the correct foreign key
    primary_key_column = "student_id"  # Foreign key column name
    primary_key = values[0]  # Adjust this index based on the position of student_id in your treeview
    column_name = treeview["columns"][col_index]

    # Confirmation dialog
    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update the marks?")
    if confirm:
        try:
            cursor = db.cursor()
            query = f"UPDATE `{selected_table}` SET `{column_name}` = %s WHERE `{primary_key_column}` = %s"
            cursor.execute(query, (new_value, primary_key))
            db.commit()
            cursor.close()
            treeview.item(selected_item, values=values)
            entry.destroy()
        except mysql.connector.Error as err:
            db.rollback()
            messagebox.showerror("Error", f"Failed to update the database: {err}")
            entry.destroy()
    else:
        entry.destroy()

    key = (selected_item, treeview.identify_column(col_index + 1))
    if key in edit_entries:
        del edit_entries[key]

def cancel_edit(selected_item, column):
    if (selected_item, column) in edit_entries:
        entry = edit_entries[(selected_item, column)]
        entry.destroy()
        del edit_entries[(selected_item, column)]

def on_table_select(event):
    global selected_table
    selected_table = table_combo.get()
    if selected_table:
        column_names, data = fetch_table_data(selected_table)
        display_table_data(column_names, data)

# GUI SETUP
root = tk.Tk()
root.title("Student Marks Viewer")
root.geometry("1600x1400")
root.resizable(True, True)

# Table selection frame
table_frame = ttk.Frame(root)
table_frame.pack(pady=10, anchor='center')

table_label = ttk.Label(table_frame, text="Select Table:", font=('Arial', 12, 'bold'))
table_label.pack(padx=5, pady=5)

table_combo = ttk.Combobox(table_frame, values=get_tables(), state="readonly", width=30, font=('Arial', 12))
table_combo.bind("<<ComboboxSelected>>", on_table_select)
table_combo.pack(padx=5, pady=5)

# Student marks table
treeview = ttk.Treeview(root, show='headings', height=15)
treeview.pack(pady=10, fill=tk.BOTH, expand=True)
treeview.bind("<Double-1>", on_double_click)

# Start the Tkinter event loop
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
