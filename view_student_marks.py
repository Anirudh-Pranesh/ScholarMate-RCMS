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
)  # Aiven connection

# Global variable to keep track of the graph window
graph_window = None


def get_tables():
    # Fetch list of tables in the database
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    res = cursor.fetchall()
    res = list(filter(lambda x: x not in [('credentials',), ('student_details',), ('teacher_details',)], res))
    cursor.close()
    return res


def fetch_table_data(table_name):
    # Fetch all data from the selected table, sorted by class and name
    cursor = db.cursor()
    query = f"SELECT * FROM {table_name} ORDER BY class, student_name"  # Add ORDER BY clause
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
        tree.column(col, anchor="center", width=200)  # Adjust width as needed

    # Insert rows into Treeview
    for row in data:
        tree.insert("", "end", values=row)


def calculate_class_average(table_name):
    # Calculate class averages for each subject
    cursor = db.cursor()
    query = f"""
    SELECT AVG(Math), AVG(PE), AVG(SocialScience), AVG(English), AVG(Physics)
    FROM {table_name}
    """
    cursor.execute(query)
    class_averages = cursor.fetchone()
    cursor.close()
    return class_averages


def show_student_and_class_avg(selected_student):
    """Display a bar chart comparing the selected student's marks to the class average."""
    global graph_window  # Use the global variable

    # Check if the graph window is already open
    if graph_window is not None and graph_window.winfo_exists():
        graph_window.focus()  # Bring it to the front
        return  # Exit to prevent opening a new one

    student_marks = [float(mark) if mark is not None else 0 for mark in selected_student[3:]]  # Convert marks to float
    class_averages = calculate_class_average(selected_table)
    class_averages = [float(avg) for avg in class_averages]  # Ensure class averages are float
    subjects = ["Math", "PE", "SocialScience", "English", "Physics"]

    # Create a new window for the plot
    graph_window = tk.Toplevel(window)
    graph_window.title(f"{selected_student[1]} vs Class Average")

    # Plot the graph
    fig, ax = plt.subplots(figsize=(8, 6))
    bar_width = 0.35
    index = range(len(subjects))

    # Bar chart
    ax.bar(index, student_marks, bar_width, label=selected_student[1])  # Fixed label formatting
    ax.bar([i + bar_width for i in index], class_averages, bar_width, label="Class Average")

    # Customizing the plot
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Marks")
    ax.set_title("Student Marks vs Class Average")
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(subjects)
    ax.set_ylim(0, 100)  # Set Y-axis limit to 100
    ax.legend()

    # Embed the plot into the new Tkinter window without showing the "Figure 1" window
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def on_table_select(event):
    global selected_table
    selected_table = table_combo.get()
    column_names, data = fetch_table_data(selected_table)
    display_table_data(column_names, data)

    # Always clear previous selection
    tree.selection_remove(tree.selection())


def on_student_select(event):
    selected_item = tree.focus()
    if selected_item:  # Ensure an item is selected
        selected_student = tree.item(selected_item)["values"]
        show_student_and_class_avg(selected_student)


def on_closing():
    # Close any open Matplotlib figures
    plt.close('all')
    db.close()  # Close database connection
    window.destroy()  # Destroy the Tkinter window


# Create window
window = tk.Tk()
window.title('Database Table Viewer')
window.geometry('1000x800')

# Bind the closing event to the on_closing function
window.protocol("WM_DELETE_WINDOW", on_closing)

# Welcome label
welcome_label = ttk.Label(window, text='Select a table to view:', font=('Arial', 16))
welcome_label.pack(pady=20)

# Dropdown for table selection
tables = get_tables()
table_combo = ttk.Combobox(window, values=tables, font=('Arial', 14), state='readonly')
table_combo.pack(pady=10)
table_combo.bind("<<ComboboxSelected>>", on_table_select)

# Scrollable frame for Treeview
tree_frame = ttk.Frame(window)
tree_frame.pack(pady=10, padx=10, fill='both', expand=True)

# Treeview (table) widget
tree = ttk.Treeview(tree_frame)
tree.pack(side="left", fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_student_select)  # Bind student selection to graph update

# Scrollbar for Treeview
tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_scrollbar.set)

# Place the scrollbar in the frame
tree_scrollbar.pack(side='right', fill='y')

# Set dark theme
sv_ttk.set_theme("dark")

# Run the application
window.mainloop()

# Close the database connection when done
db.close()
