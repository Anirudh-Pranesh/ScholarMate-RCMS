import tkinter as tk
from tkinter import ttk
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

# Handle window close event to release Matplotlib resources
def on_close():
    if graph_canvas:
        plt.close()
    root.destroy()

# Global variables to keep track of the graph canvas
graph_canvas = None

def get_tables():
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    res = cursor.fetchall()
    res = list(filter(lambda x: x not in [('credentials',), ('student_details',), ('teacher_details',)], res))
    cursor.close()
    return res

def fetch_subject_names(table_name):
    cursor = db.cursor()
    get_subj_names = f"DESC {table_name};"
    cursor.execute(get_subj_names)
    subj_names_sql = cursor.fetchall()
    subj_names_useable = []
    for idx, item in enumerate(subj_names_sql):
        if idx > 2:
            subj_names_useable.append(item[0])
    cursor.close()
    return tuple(subj_names_useable)

def fetch_table_data(table_name):
    cursor = db.cursor()
    query = f"SELECT * FROM {table_name} ORDER BY class, student_name"
    cursor.execute(query)
    data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    return column_names, data

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

def calculate_class_average(table_name, subject_names):
    cursor = db.cursor()
    avg_columns = ", ".join([f"AVG(`{sub}`)" for sub in subject_names])
    query = f"SELECT {avg_columns} FROM `{table_name}`"
    cursor.execute(query)
    class_averages = cursor.fetchone()
    cursor.close()
    return class_averages

def show_student_and_class_avg(selected_student):
    global graph_canvas
    if graph_canvas:
        graph_canvas.get_tk_widget().destroy()
    subject_names = fetch_subject_names(selected_table)
    student_marks = [float(mark) if mark is not None and mark.replace('.', '', 1).isdigit() else 0 for mark in selected_student[3:]]
    class_averages = calculate_class_average(selected_table, subject_names)
    class_averages = [float(avg) if avg is not None else 0 for avg in class_averages]
    fig, ax = plt.subplots(figsize=(8, 4))
    bar_width = 0.35
    index = range(len(student_marks))
    ax.bar(index, student_marks, bar_width, label=selected_student[1], color='blue')
    ax.bar([i + bar_width for i in index], class_averages, bar_width, label="Class Average", color='green')
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Marks")
    ax.set_title("Student Marks vs Class Average")
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(subject_names, rotation=45, ha='right')
    ax.set_ylim(0, 100)
    ax.legend()
    graph_canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def on_table_select(event):
    global selected_table
    selected_table = table_combo.get()
    column_names, data = fetch_table_data(selected_table)
    display_table_data(column_names, data)
    tree.selection_remove(tree.selection())
    student_name_label.config(text="Name: ")
    student_class_label.config(text="Class: ")
    for widget in marks_frame.winfo_children():
        widget.destroy()
    if graph_canvas:
        graph_canvas.get_tk_widget().destroy()

def on_student_select(event):
    selected_item = tree.focus()
    if selected_item:
        selected_student = tree.item(selected_item)["values"]
        update_student_info(selected_student)
        display_student_marks(selected_student)
        show_student_and_class_avg(selected_student)

def update_student_info(selected_student):
    student_name_label.config(text=f"Name: {selected_student[1]}")
    student_class_label.config(text=f"Class: {selected_student[2]}")

def display_student_marks(selected_student):
    for widget in marks_frame.winfo_children():
        widget.destroy()
    subject_names = fetch_subject_names(selected_table)
    subject_header = ttk.Label(marks_frame, text="Subjects", font=('Arial', 14, 'bold'))
    subject_header.grid(row=0, column=0, padx=10, pady=5, sticky='w', columnspan=len(subject_names))
    marks_header = ttk.Label(marks_frame, text="Marks", font=('Arial', 14, 'bold'))
    marks_header.grid(row=1, column=0, padx=10, pady=5, sticky='w', columnspan=len(subject_names))
    total_marks = 0
    num_subjects = len(subject_names)
    for idx, subject in enumerate(subject_names):
        subject_label = ttk.Label(marks_frame, text=subject, font=('Arial', 12))
        subject_label.grid(row=0, column=idx + 1, padx=10, pady=5, sticky='w')
        mark = selected_student[3 + idx]
        if mark is not None:
            try:
                mark_float = float(mark)
                mark_text = str(mark_float)
                total_marks += mark_float
            except ValueError:
                mark_text = "Absent"
        else:
            mark_text = "Absent"
        mark_label = ttk.Label(marks_frame, text=mark_text, font=('Arial', 12))
        mark_label.grid(row=1, column=idx + 1, padx=10, pady=5, sticky='w')
    total_label = ttk.Label(marks_frame, text="Total", font=('Arial', 14, 'bold'))
    total_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
    total_value_label = ttk.Label(marks_frame, text=str(total_marks), font=('Arial', 14, 'bold'))
    total_value_label.grid(row=2, column=1, padx=10, pady=5, sticky='w')
    percentage = (total_marks / (num_subjects * 100)) * 100 if num_subjects > 0 else 0
    percentage_label = ttk.Label(marks_frame, text="Percentage", font=('Arial', 14, 'bold'))
    percentage_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
    percentage_value_label = ttk.Label(marks_frame, text=f"{percentage:.2f}%", font=('Arial', 14, 'bold'))
    percentage_value_label.grid(row=3, column=1, padx=10, pady=5, sticky='w')

# SETUP MAIN WINDOW
root = tk.Tk()
root.title("ScholarMate - Student Marks Viewer")
root.geometry("1200x800")
root.resizable(True, True)
sv_ttk.set_theme("dark")
root.protocol("WM_DELETE_WINDOW", on_close)

# TABLE SELECTION FRAME
table_frame = ttk.Frame(root)
table_frame.pack(pady=10)
table_combo = ttk.Combobox(table_frame, values=get_tables())
table_combo.bind("<<ComboboxSelected>>", on_table_select)
table_combo.pack(pady=5)

# TREEVIEW FOR STUDENT DATA
tree_frame = ttk.Frame(root)
tree_frame.pack(pady=10)
tree = ttk.Treeview(tree_frame, show='headings')
tree.pack(side=tk.LEFT)
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
tree.configure(yscrollcommand=scrollbar.set)
tree.bind("<<TreeviewSelect>>", on_student_select)

# Student Info Frame
info_frame = ttk.Frame(root)
info_frame.pack(pady=10)
student_name_label = ttk.Label(info_frame, text="Name: ", font=('Arial', 16))
student_name_label.pack(side=tk.LEFT, padx=10)
student_class_label = ttk.Label(info_frame, text="Class: ", font=('Arial', 16))
student_class_label.pack(side=tk.LEFT, padx=10)

# Marks Frame
marks_frame = ttk.Frame(root)
marks_frame.pack(pady=10)

# Graph Frame
graph_frame = ttk.Frame(root)
graph_frame.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
