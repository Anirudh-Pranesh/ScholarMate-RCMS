import tkinter as tk
import sv_ttk
from tkinter import ttk, messagebox
import mysql.connector
import pickle

# DATABASE CONNECTION
try:
    #db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_QI3ZZve-eNqFc8_bsLQ', database='scholarmate_db') #aiven conn.
    db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
except:
    messagebox.showerror(title="Error", message="No internet connection. Please connect to internet")
cur=db.cursor()
file=open('client_details.dat', 'rb')
dat=pickle.load(file)
teacher_id = dat[0][0]
get_assgn_class=f"SELECT assigned_class FROM teacher_details WHERE teacher_id = {teacher_id}"
cur.execute(get_assgn_class)
assgn_class=cur.fetchall()[0][0]

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
        query = f"SELECT * FROM `{table_name}` WHERE class = '{assgn_class}' ORDER BY `class`, `student_name`"
        cursor.execute(query)
        data = cursor.fetchall()
        if data != []:
            column_names = [i[0] for i in cursor.description]
            cursor.close()
            return column_names, data
        else:
            messagebox.showinfo(title='Info', message=f"{assgn_class} has not written this exam")    
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

# Store modified values for bulk update
modified_values = {}

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

            # Create Entry widget and position it over the cell
            entry = tk.Entry(root)
            entry.place(x=bbox[0] + treeview.winfo_x(), y=bbox[1] + treeview.winfo_y(), width=bbox[2], height=bbox[3])
            entry.insert(0, current_value)
            entry.focus()

            # Bind events to save or cancel
            entry.bind("<Return>", lambda e: save_value(selected_item, col_index, entry))
            entry.bind("<FocusOut>", lambda e: entry.destroy())

def save_value(selected_item, col_index, entry):
    new_value = entry.get()
    values = list(treeview.item(selected_item, 'values'))
    values[col_index] = new_value

    primary_key_column = "student_id"  # Foreign key column name
    primary_key = values[0]  # Adjust this index based on the position of student_id in your treeview
    column_name = treeview["columns"][col_index]

    # Store or update modified values
    if primary_key not in modified_values:
        modified_values[primary_key] = {}
    modified_values[primary_key][column_name] = new_value

    treeview.item(selected_item, values=values)
    entry.destroy()

def confirm_changes():
    if not modified_values:
        messagebox.showinfo("No Changes", "There are no changes to save.")
        return

    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to save all changes?")
    if confirm:
        try:
            cursor = db.cursor()
            for student_id, updates in modified_values.items():
                for column, value in updates.items():
                    query = f"UPDATE `{selected_table}` SET `{column}` = %s WHERE `student_id` = %s"
                    cursor.execute(query, (value, student_id))
            db.commit()
            cursor.close()
            messagebox.showinfo("Success", "Changes have been saved.")
            modified_values.clear()  # Clear modified values after saving
        except mysql.connector.Error:
            db.rollback()
            messagebox.showerror("ERROR", f"Please enter valid marks for the student")

def on_table_select(event):
    global selected_table
    selected_table = table_combo.get()
    if selected_table:
        column_names, data = fetch_table_data(selected_table)
        display_table_data(column_names, data)

# GUI SETUP
root = tk.Tk()
root.title("Edit student marks")
root.geometry("1600x1400")
root.resizable(True, True)

# Table selection frame
table_frame = ttk.Frame(root)
table_frame.pack(pady=10, anchor='center')

table_label = ttk.Label(table_frame, text="Select Examination:", font=('Arial', 12, 'bold'))
table_label.pack(padx=5, pady=5)

table_combo = ttk.Combobox(table_frame, values=get_tables(), state="readonly", width=30, font=('Arial', 12))
table_combo.bind("<<ComboboxSelected>>", on_table_select)
table_combo.pack(padx=5, pady=5)

# Student marks table
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
