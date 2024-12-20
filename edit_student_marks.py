import tkinter as tk
import sv_ttk
from tkinter import ttk, messagebox
import mysql.connector

# DATABASE CONNECTION SETUP
try:
    #db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_QI3ZZve-eNqFc8_bsLQ', database='scholarmate_db') #aiven conn.
    db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
except:
    messagebox.showerror(title="Error", message="No internet connection. Please connect to internet")

# Gracefully close the application and the database connection
def on_close():
    try:
        db.close()
    except Exception as e:
        print(f"Error closing database: {e}")
    root.destroy()

# Fetch available tables excluding unwanted ones
def get_tables():
    try:
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        filtered_tables = [table[0] for table in tables if table[0] not in ('credentials', 'student_details', 'teacher_details')]
        cursor.close()
        return filtered_tables
    except mysql.connector.Error as err:
        print(f"Error fetching tables: {err}")
        return []

# Fetch and return column names and data for the selected table
def fetch_table_data(table_name):
    try:
        cursor = db.cursor()
        query = f"SELECT * FROM `{table_name}` ORDER BY `class`, `student_name`"
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()
        return column_names, data
    except mysql.connector.Error as err:
        print(f"Error fetching table data: {err}")
        return [], []

# Display the fetched table data in Treeview
def display_table_data(column_names, data):
    treeview.delete(*treeview.get_children())  # Clear previous data
    treeview["columns"] = column_names
    treeview["show"] = "headings"

    for col in column_names:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center", width=150)

    for row in data:
        treeview.insert("", "end", values=row)

# Global dictionary to track modified values for batch update
modified_values = {}

# Handle double-click event to allow cell editing
def on_double_click(event):
    selected_item = treeview.focus()
    column = treeview.identify_column(event.x)

    if selected_item and column:
        col_index = int(column[1:]) - 1
        if col_index < 3:
            messagebox.showinfo("Locked Column", "Editing is not allowed for this column.")
            return

        bbox = treeview.bbox(selected_item, column)
        if bbox:
            current_value = treeview.item(selected_item, 'values')[col_index]

            # Create entry widget for editing
            entry = tk.Entry(root)
            entry.place(x=bbox[0] + treeview.winfo_x(), y=bbox[1] + treeview.winfo_y(), width=bbox[2], height=bbox[3])
            entry.insert(0, current_value)
            entry.focus()

            entry.bind("<Return>", lambda e: save_value(selected_item, col_index, entry))
            entry.bind("<FocusOut>", lambda e: entry.destroy())

# Save the edited value and track modifications
def save_value(selected_item, col_index, entry):
    new_value = entry.get()

    if new_value.lower() != "" and (isinstance(new_value, float) or isinstance(new_value,int)):
        messagebox.showerror("Invalid Input", "Please enter valid marks for the student.")
        entry.focus()
        return
    
    values = list(treeview.item(selected_item, 'values'))
    values[col_index] = new_value

    primary_key = values[0]
    column_name = treeview["columns"][col_index]

    if primary_key not in modified_values:
        modified_values[primary_key] = {}
    modified_values[primary_key][column_name] = new_value

    treeview.item(selected_item, values=values)
    entry.destroy()

# Confirm and save all changes to the database
def confirm_changes():
    if not modified_values:
        messagebox.showinfo("No Changes", "There are no changes to save.")
        return

    if messagebox.askyesno("Confirm Update", "Are you sure you want to save all changes?"):
        try:
            cursor = db.cursor()
            for student_id, updates in modified_values.items():
                for column, value in updates.items():
                    query = f"UPDATE `{selected_table}` SET `{column}` = %s WHERE `student_id` = %s"
                    cursor.execute(query, (value, student_id))
            db.commit()
            cursor.close()
            messagebox.showinfo("Success", "Changes have been saved.")
            modified_values.clear()
        except mysql.connector.Error:
            db.rollback()
            messagebox.showerror("ERROR", f"Please enter valid marks for the student")

# Fetch table data based on selected table in the dropdown
def on_table_select(event):
    global selected_table
    selected_table = table_combo.get()
    if selected_table:
        column_names, data = fetch_table_data(selected_table)
        display_table_data(column_names, data)

# Set up the main Tkinter window
root = tk.Tk()
root.title("Edit student marks")
root.geometry("1600x1400")
root.resizable(True, True)

# Frame for the table selection dropdown
table_frame = ttk.Frame(root)
table_frame.pack(pady=10, anchor='center')

table_label = ttk.Label(table_frame, text="Select Examination:", font=('Arial', 12, 'bold'))
table_label.pack(padx=5, pady=5)

# Dropdown list for table selection
table_combo = ttk.Combobox(table_frame, values=get_tables(), state="readonly", width=30, font=('Arial', 12))
table_combo.bind("<<ComboboxSelected>>", on_table_select)
table_combo.pack(padx=5, pady=5)

# Treeview widget to display student marks
treeview = ttk.Treeview(root, show='headings', height=15)
treeview.pack(pady=10, fill=tk.BOTH, expand=True)
treeview.bind("<Double-1>", on_double_click)

# Confirm changes button
confirm_button = ttk.Button(root, text="Confirm Changes", command=confirm_changes)
confirm_button.pack(pady=10)

# Start the Tkinter event loop
root.protocol("WM_DELETE_WINDOW", on_close)
sv_ttk.set_theme("dark")
root.mainloop()
