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
    
    # Create a new window for the graph
    graph_window = tk.Toplevel(root)
    graph_window.title(f"Marks for {selected_student[1]}")
    
    # Adjusted size for the graph
    fig, ax = plt.subplots(figsize=(8, 7))  # Smaller size
    bar_width = 0.2
    index = range(len(student_marks))
    ax.bar(index, student_marks, bar_width, label=selected_student[1], color='blue')
    ax.bar([i + bar_width for i in index], class_averages, bar_width, label="Class Average", color='green')
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Marks")
    ax.set_title("Student Marks vs Class Average")
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(subject_names, rotation=0, ha='right')
    ax.set_ylim(0, 100)
    ax.legend()
    
    # Display graph in the new window
    graph_canvas = FigureCanvasTkAgg(fig, master=graph_window)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def on_table_select(event):
    global selected_table
    selected_table = table_combo.get()
    column_names, data = fetch_table_data(selected_table)
    display_table_data(column_names, data)
    tree.selection_remove(tree.selection())
    clear_student_info()

def clear_student_info():
    # Clear the student info labels and marks frame
    student_name_label.config(text="")  # Clear name label
    student_class_label.config(text="")  # Clear class label
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
    
    # Display subjects and marks
    subject_header = ttk.Label(marks_frame, text="Subjects", font=('Arial', 14, 'bold'))
    subject_header.grid(row=0, column=0, padx=0, pady=5, sticky='w', columnspan=len(subject_names))
    marks_header = ttk.Label(marks_frame, text="Marks", font=('Arial', 14, 'bold'))
    marks_header.grid(row=1, column=0, padx=0, pady=5, sticky='w', columnspan=len(subject_names))
    
    total_marks = 0
    num_subjects = len(subject_names)
    
    for idx, subject in enumerate(subject_names):
        subject_label = ttk.Label(marks_frame, text=subject, font=('Arial', 12))
        subject_label.grid(row=0, column=idx + 1, padx=0, pady=5, sticky='w')
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
        mark_label.grid(row=1, column=idx + 1, padx=0, pady=5, sticky='w')
    
    # Display total and percentage
    total_label = ttk.Label(marks_frame, text="Total", font=('Arial', 14, 'bold'))
    total_label.grid(row=2, column=0, padx=0, pady=5, sticky='w')
    total_value_label = ttk.Label(marks_frame, text=str(total_marks), font=('Arial', 14, 'bold'))
    total_value_label.grid(row=2, column=1, padx=0, pady=5, sticky='w')
    
    percentage = (total_marks / (num_subjects * 100)) * 100 if num_subjects > 0 else 0
    percentage_label = ttk.Label(marks_frame, text="Percentage", font=('Arial', 14, 'bold'))
    percentage_label.grid(row=3, column=0, padx=0, pady=5, sticky='w')
    percentage_value_label = ttk.Label(marks_frame, text=f"{percentage:.2f}%", font=('Arial', 14, 'bold'))
    percentage_value_label.grid(row=3, column=1, padx=0, pady=5, sticky='w')

# SETUP MAIN WINDOW
root = tk.Tk()
root.title("ScholarMate - Student Marks Viewer")
root.geometry("1200x800")
root.resizable(True, True)
sv_ttk.set_theme("dark")
root.protocol("WM_DELETE_WINDOW", on_close)

# Add a scrollbar for the whole window
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)
main_canvas = tk.Canvas(main_frame)
main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
second_frame = ttk.Frame(main_canvas)
main_canvas.create_window((0, 0), window=second_frame, anchor="nw")

def on_frame_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

second_frame.bind("<Configure>", on_frame_configure)

# TABLE SELECTION FRAME
table_frame = ttk.Frame(second_frame)
table_frame.pack(pady=10, anchor='center')  # Center the frame
table_combo = ttk.Combobox(table_frame, values=get_tables())
table_combo.bind("<<ComboboxSelected>>", on_table_select)
table_combo.pack()

# STUDENT MARKS TABLE
tree = ttk.Treeview(second_frame, show='headings')
tree.pack(pady=20, fill=tk.BOTH, expand=True)
tree.bind("<ButtonRelease-1>", on_student_select)

# STUDENT INFO DISPLAY
info_frame = ttk.Frame(second_frame)
info_frame.pack(pady=10, anchor='center')  # Center the frame

student_name_label = ttk.Label(info_frame, text="", font=('Arial', 12))
student_name_label.grid(row=0, column=0, padx=0, pady=5, sticky='w')
student_class_label = ttk.Label(info_frame, text="", font=('Arial', 12))
student_class_label.grid(row=1, column=0, padx=0, pady=5, sticky='w')

# Marks Frame
marks_frame = ttk.Frame(second_frame)
marks_frame.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
