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
    db.close()  # Close the database connection
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

def calculate_class_average(table_name, subject_names):
    try:
        cursor = db.cursor()
        avg_columns = ", ".join([f"AVG(`{sub}`) AS `{sub}_avg`" for sub in subject_names])
        query = f"SELECT {avg_columns} FROM `{table_name}`"
        cursor.execute(query)
        class_averages = cursor.fetchone()
        cursor.close()
        return class_averages
    except mysql.connector.Error as err:
        print(f"Error calculating class average: {err}")
        return ()

def top_score(table_name, subject_names):
    try:
        cursor = db.cursor()
        top_columns = ", ".join([f"MAX(`{sub}`) AS `{sub}_max`" for sub in subject_names])
        query = f"SELECT {top_columns} FROM `{table_name}`"
        cursor.execute(query)
        top_scores = cursor.fetchone()
        cursor.close()
        return top_scores
    except mysql.connector.Error as err:
        print(f"Error fetching top scores: {err}")
        return ()

def create_class_average_treeview(parent, subject_names):
    """Creates and returns a Treeview widget for displaying class-wise averages."""
    # Create a labeled frame for clarity
    class_avg_frame = ttk.LabelFrame(parent, text="Class-wise Averages")
    class_avg_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    # Define columns: 'Class' followed by average of each subject
    columns = ["Class"] + [f"{sub} Avg" for sub in subject_names]
    
    class_average_tree = ttk.Treeview(class_avg_frame, columns=columns, show='headings', height=10)
    
    for col in columns:
        class_average_tree.heading(col, text=col)
        class_average_tree.column(col, anchor="center", width=100)
    
    # Add a vertical scrollbar
    vsb = ttk.Scrollbar(class_avg_frame, orient="vertical", command=class_average_tree.yview)
    class_average_tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side=tk.RIGHT, fill='y')
    
    class_average_tree.pack(fill=tk.BOTH, expand=True)
    
    return class_average_tree

def show_student_and_class_avg(selected_student):
    subject_names = fetch_subject_names(selected_table)
    if not subject_names:
        print("No subjects found.")
        return

    # Extract student marks starting from the 4th column
    student_marks = []
    for mark in selected_student[3:]:
        if mark is not None and isinstance(mark, (int, float, str)) and str(mark).replace('.', '', 1).isdigit():
            student_marks.append(float(mark))
        else:
            student_marks.append(0)

    class_averages = calculate_class_average(selected_table, subject_names)
    class_averages = [float(avg) if avg is not None else 0 for avg in class_averages]

    top_scores = top_score(selected_table, subject_names)
    top_scores = [float(score) if score is not None else 0 for score in top_scores]

    # Create a new window for the graph
    graph_window = tk.Toplevel(root)
    graph_window.title(f"Marks for {selected_student[1]}")
    graph_window.geometry("1000x700")  # Increased size for better layout
    graph_window.resizable(False, False)  # Prevent resizing

    # Function to handle graph window close
    def on_graph_close():
        plt.close(fig)
        graph_window.destroy()

    graph_window.protocol("WM_DELETE_WINDOW", on_graph_close)

    # Create frames within the graph window
    info_frame = ttk.Frame(graph_window)
    info_frame.pack(pady=10, padx=10, anchor='center', fill='x')
    marks_frame_graph = ttk.Frame(graph_window)
    marks_frame_graph.pack(pady=10, padx=10, anchor='center')

    # Student Information Labels
    student_name_label = ttk.Label(info_frame, text=f"Name: {selected_student[1]}", font=('Arial', 14, 'bold'))
    student_name_label.pack(anchor='w')
    student_class_label = ttk.Label(info_frame, text=f"Class: {selected_student[2]}", font=('Arial', 14, 'bold'))
    student_class_label.pack(anchor='w')

    # Marks Treeview
    marks_tree = ttk.Treeview(marks_frame_graph, columns=("Subject", "Mark"), show='headings', height=len(subject_names))
    marks_tree.heading("Subject", text="Subject")
    marks_tree.heading("Mark", text="Mark")
    marks_tree.column("Subject", anchor="w", width=300)
    marks_tree.column("Mark", anchor="w", width=300)
    for subject, mark in zip(subject_names, student_marks):
        marks_tree.insert("", "end", values=(subject, mark if mark != 0 else "Absent"))
    marks_tree.pack(fill='x', expand=True)

    # Calculate total and percentage
    total_marks = sum(student_marks)
    num_subjects = len(subject_names)
    percentage = (total_marks / (num_subjects * 100)) * 100 if num_subjects > 0 else 0
    low_subject, low = min(zip(subject_names, student_marks), key=lambda x: x[1])
    best_subject, best = max(zip(subject_names, student_marks), key=lambda x: x[1])

    # Display total marks, percentage, and subject performance
    total_label = ttk.Label(info_frame, text=f"Total Marks: {total_marks}", font=('Arial', 12, 'bold'))
    total_label.pack(anchor='w', pady=(10, 0))
    percentage_label = ttk.Label(info_frame, text=f"Percentage: {percentage:.2f}%", font=('Arial', 12, 'bold'))
    percentage_label.pack(anchor='w')
    low_label = ttk.Label(info_frame, text=f"Worst Performing Subject: {low_subject} ({low:.2f})", font=('Arial', 12, 'bold'))
    low_label.pack(anchor='w')
    best_label = ttk.Label(info_frame, text=f"Best Performing Subject: {best_subject} ({best:.2f})", font=('Arial', 12, 'bold'))
    best_label.pack(anchor='w')

    # Plotting student marks, class averages, and top scores
    fig, ax = plt.subplots(figsize=(8, 6))  # Adjusted size for better fit
    bar_width = 0.2
    index = range(len(subject_names))

    # Positions for each set of bars
    student_pos = [i - bar_width for i in index]
    average_pos = index
    top_pos = [i + bar_width for i in index]

    # Plotting the bars
    bars1 = ax.bar(student_pos, student_marks, bar_width, label=selected_student[1], color='skyblue')
    bars2 = ax.bar(average_pos, class_averages, bar_width, label="Class Average", color='lightgreen')
    bars3 = ax.bar(top_pos, top_scores, bar_width, label="Top Score", color='salmon')

    # Labels and Title
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Marks")
    ax.set_xticks(index)
    ax.set_xticklabels(subject_names, rotation=0, ha='right', fontsize=10)
    ax.set_ylim(0, max(max(student_marks), max(class_averages), max(top_scores), 100) + 10)
    ax.legend()

    # Adding bar value labels
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.annotate(f'{height:.1f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8)

    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)

    plt.tight_layout(pad=2.0)  # Adjust layout to prevent clipping

    # Display graph in the graph window
    graph_canvas = FigureCanvasTkAgg(fig, master=graph_window)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

def show_class_average_window():
    global selected_table
    if not selected_table:
        print("No table selected.")
        return

    subject_names = fetch_subject_names(selected_table)
    if not subject_names:
        print("No subjects found.")
        return
    
    class_wise_averages = calculate_class_wise_average(selected_table, subject_names)

    # Create a new window for class-wise averages
    avg_window = tk.Toplevel(root)
    avg_window.title(f"Class-wise Averages for {selected_table}")
    avg_window.geometry("1000x600")
    avg_window.resizable(True, True)

    # Function to handle averages window close
    def on_avg_close():
        plt.close(fig_avg)
        avg_window.destroy()

    avg_window.protocol("WM_DELETE_WINDOW", on_avg_close)

    # Create frames for Treeview and Graph
    tree_frame = ttk.Frame(avg_window)
    tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    graph_frame = ttk.Frame(avg_window)
    graph_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create Treeview for class-wise averages
    class_average_tree = create_class_average_treeview(tree_frame, subject_names)

    # Insert data into Treeview
    for avg in class_wise_averages:
        # Convert all float averages to 2 decimal places for better readability
        avg_formatted = [avg[0]] + [f"{value:.2f}" for value in avg[1:]]
        class_average_tree.insert("", "end", values=avg_formatted)

    # Plotting class-wise averages
    fig_avg, ax_avg = plt.subplots(figsize=(10, 6))
    index = range(len(subject_names))
    bar_width = 0.15

    num_classes = len(class_wise_averages)
    colors = plt.cm.get_cmap('tab10', num_classes)

    for i, (avg) in enumerate(class_wise_averages):
        class_name = avg[0]
        averages = [float(value) if value is not None else 0 for value in avg[1:]]
        positions = [x + (i * bar_width) for x in index]
        ax_avg.bar(positions, averages, bar_width, label=f"Class {class_name}", color=colors(i))

    # Labels and Title
    ax_avg.set_xlabel("Subjects")
    ax_avg.set_ylabel("Average Marks")
    ax_avg.set_title(f"Class-wise Averages for {selected_table}")
    ax_avg.set_xticks([x + bar_width * (num_classes / 2) for x in index])
    ax_avg.set_xticklabels(subject_names, rotation=45, ha='right', fontsize=10)
    ax_avg.set_ylim(0, 100)
    ax_avg.legend()

    # Adding bar value labels
    def add_labels_to_bars(bars):
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax_avg.annotate(f'{height:.1f}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=8)

    # Add labels to each set of bars
    for container in ax_avg.containers:
        add_labels_to_bars(container)

    plt.tight_layout(pad=2.0)

    # Display graph in the averages window
    avg_graph_canvas = FigureCanvasTkAgg(fig_avg, master=graph_frame)
    avg_graph_canvas.draw()
    avg_graph_canvas.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

def calculate_class_wise_average(table_name, subject_names):
    try:
        cursor = db.cursor()
        # Construct AVG columns for each subject
        avg_columns = ", ".join([f"AVG(`{sub}`) AS `{sub}_avg`" for sub in subject_names])
        query = f"SELECT `class`, {avg_columns} FROM `{table_name}` GROUP BY `class`"
        cursor.execute(query)
        class_wise_averages = cursor.fetchall()
        cursor.close()
        return class_wise_averages  # List of tuples: (class, subj1_avg, subj2_avg, ...)
    except mysql.connector.Error as err:
        print(f"Error calculating class-wise averages: {err}")
        return []

# Table selection handler
def on_table_select(event):
    global selected_table
    selected_table = table_combo.get()
    if selected_table:
        column_names, data = fetch_table_data(selected_table)
        display_table_data(column_names, data)
        tree.selection_remove(tree.selection())
        clear_student_info()

# Clear student info when a new table is selected
def clear_student_info():
    # Since we manage graph canvases locally within their functions,
    # there's no global graph_canvas to clear here.
    pass

# Student selection handler
def on_student_select(event):
    selected_item = tree.focus()
    if selected_item:
        selected_student = tree.item(selected_item)["values"]
        show_student_and_class_avg(selected_student)

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

# BUTTON to show class-wise averages
avg_button = ttk.Button(table_frame, text="Show Class-wise Averages", command=show_class_average_window)
avg_button.pack(padx=5, pady=5)

# STUDENT MARKS TABLE
tree = ttk.Treeview(main_frame, show='headings', height=20)
tree.pack(pady=10, fill=tk.BOTH, expand=True)
tree.bind("<ButtonRelease-1>", on_student_select)

# Start the Tkinter event loop
root.mainloop()
