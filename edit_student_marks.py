import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# DATABASE CONNECTION
db = mysql.connector.connect(
    host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com',
    port=13426,
    user='avnadmin',
    password='AVNS_1UgkIMxSzsCWt0D-3cB',
    database='scholarmate_db'
)

# Handle window close event to release Matplotlib resources and close DB connection
def on_close():
    try:
        db.close()  # Close the database connection
    except:
        pass
    root.destroy()

def get_tables():
    try:
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        res = cursor.fetchall()
        # Filter out specific tables
        res = list(filter(lambda x: x not in [('credentials',), ('student_details',), ('teacher_details',)], res))
        cursor.close()
        return [table[0] for table in res]
    except mysql.connector.Error as err:
        print(f"Error fetching tables: {err}")
        return []

def fetch_subject_names(table_name):
    try:
        cursor = db.cursor()
        get_subj_names = f"DESC `{table_name}`;"
        cursor.execute(get_subj_names)
        subj_names_sql = cursor.fetchall()
        subj_names_useable = []
        for idx, item in enumerate(subj_names_sql):
            if idx > 2:  # Assuming first three columns are not subjects
                subj_names_useable.append(item[0])
        cursor.close()
        return tuple(subj_names_useable)
    except mysql.connector.Error as err:
        print(f"Error fetching subject names: {err}")
        return ()

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

def display_table_data(column_names, data):
    for row in tree.get_children():
        tree.delete(row)
    tree["columns"] = column_names
    tree["show"] = "headings"
    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)
    for row in data:
        tree.insert("", "end", values=row)

def update_student_marks(student_id, subject_marks):
    try:
        cursor = db.cursor()
        set_clause = ", ".join([f"`{subject}` = %s" for subject in subject_marks.keys()])
        values = list(subject_marks.values())
        values.append(student_id)
        query = f"UPDATE `{selected_table}` SET {set_clause} WHERE `student_id` = %s"
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        messagebox.showinfo("Success", "Marks updated successfully!")
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error updating marks: {err}")
        messagebox.showerror("Error", f"Failed to update marks: {err}")

def show_edit_marks_window(selected_student):
    subject_names = fetch_subject_names(selected_table)
    if not subject_names:
        print("No subjects found.")
        return

    # Extract student marks starting from the 4th column (assuming first three are ID, Name, Class)
    student_marks = {}
    student_id = selected_student[0]  # Assuming first column is student_id
    for subject, mark in zip(subject_names, selected_student[3:]):
        if mark is not None and isinstance(mark, (int, float, str)) and str(mark).replace('.', '', 1).isdigit():
            student_marks[subject] = str(mark)
        else:
            student_marks[subject] = ""

    # Create a new window for editing marks
    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit Marks for {selected_student[1]}")
    edit_window.geometry("400x600")
    edit_window.resizable(False, False)

    # Function to handle window close
    def on_edit_close():
        edit_window.destroy()

    edit_window.protocol("WM_DELETE_WINDOW", on_edit_close)

    # Frame for form
    form_frame = ttk.Frame(edit_window)
    form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Dictionary to hold entry widgets
    entries = {}

    # Create labels and entries for each subject
    for idx, subject in enumerate(subject_names):
        lbl = ttk.Label(form_frame, text=f"{subject}:", font=('Arial', 12))
        lbl.grid(row=idx, column=0, pady=10, sticky='w')

        entry = ttk.Entry(form_frame, font=('Arial', 12))
        entry.insert(0, student_marks[subject])
        entry.grid(row=idx, column=1, pady=10, padx=10, sticky='w')
        entries[subject] = entry

    # Function to submit the updated marks
    def submit_marks():
        updated_marks = {}
        for subject, entry in entries.items():
            value = entry.get().strip()
            if value == "":
                updated_marks[subject] = None  # Treat empty as NULL
            else:
                try:
                    float_val = float(value)
                    if float_val < 0 or float_val > 100:
                        raise ValueError
                    updated_marks[subject] = float_val
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Please enter a valid mark between 0 and 100 for {subject}.")
                    return
        # Confirm update
        confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update the marks?")
        if confirm:
            update_student_marks(student_id, updated_marks)
            # Refresh the main table
            column_names, data = fetch_table_data(selected_table)
            display_table_data(column_names, data)
            edit_window.destroy()

    # Submit button
    submit_btn = ttk.Button(form_frame, text="Submit", command=submit_marks)
    submit_btn.grid(row=len(subject_names)+1, column=0, columnspan=2, pady=20)

def on_table_select(event):
    global selected_table
    selected_table = table_combo.get()
    if selected_table:
        column_names, data = fetch_table_data(selected_table)
        display_table_data(column_names, data)
        tree.selection_remove(tree.selection())
        clear_student_info()

def clear_student_info():
    # No longer needed as we removed class-wise averages
    pass

def on_student_select(event):
    selected_item = tree.focus()
    if selected_item:
        selected_student = tree.item(selected_item)["values"]
        show_edit_marks_window(selected_student)

# GUI SETUP
root = tk.Tk()
root.title("Student Marks Viewer")
root.geometry("1200x800")
root.resizable(True, True)
sv_ttk.set_theme("dark")
root.protocol("WM_DELETE_WINDOW", on_close)

# Add a scrollbar for the whole window
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

main_canvas = tk.Canvas(main_frame)
main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create another frame inside the canvas
second_frame = ttk.Frame(main_canvas)
main_canvas.create_window((0, 0), window=second_frame, anchor="nw")

def on_frame_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

second_frame.bind("<Configure>", on_frame_configure)

# TABLE SELECTION FRAME
table_frame = ttk.Frame(second_frame)
table_frame.pack(pady=10, anchor='center')  # Center the frame

table_label = ttk.Label(table_frame, text="Select Table:", font=('Arial', 12, 'bold'))
table_label.pack(padx=5, pady=5)

table_combo = ttk.Combobox(table_frame, values=get_tables(), state="readonly", width=30, font=('Arial', 12))
table_combo.bind("<<ComboboxSelected>>", on_table_select)
table_combo.pack(padx=5, pady=5)

# Remove the "Show Class-wise Averages" button as it's no longer needed
# avg_button = ttk.Button(table_frame, text="Show Class-wise Averages", command=show_class_average_window)
# avg_button.pack(padx=5, pady=5)

# STUDENT MARKS TABLE
tree = ttk.Treeview(main_frame, show='headings', height=20)
tree.pack(pady=10, fill=tk.BOTH, expand=True)
tree.bind("<ButtonRelease-1>", on_student_select)

# Start the Tkinter event loop
root.mainloop()
