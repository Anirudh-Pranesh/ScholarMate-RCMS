import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle

# DATABASE CONNECTION
try:
    try:
        db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_QI3ZZve-eNqFc8_bsLQ', database='scholarmate_db') #aiven conn.
        #db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
    except:
        messagebox.showerror(title="Error", message="No internet connection. Please connect to internet")

    cur = db.cursor()
    file = open('client_details.dat', 'rb')
    dat = pickle.load(file)
    std_id = dat[0][1]
    get_assgn_class = f"SELECT class, student_name FROM student_details WHERE student_id = {std_id}"
    cur.execute(get_assgn_class)
    classandname=cur.fetchall()
    std_class = classandname[0][0]
    std_name = classandname[0][1]
except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")
    exit(1)
    
selected_table = 'semester2'
prev_table ='Sem3'

# Handle window close event to release Matplotlib resources
def on_close():
    try:
        db.close()  # Close the database connection
    except Exception as e:
        print(f"Error closing database: {e}")
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
'''res2=get_tables()
index=res2.index(selected_table)
prev_table=res2[index-1]'''
def fetch_subject_names(selected_table):
    try:
        cursor = db.cursor()
        get_subj_names = f"DESC `{selected_table}`;"
        cursor.execute(get_subj_names)
        subj_names_sql = cursor.fetchall()
        subj_names_useable = []
        for idx, item in enumerate(subj_names_sql):
            if idx > 2:  # Assuming first three columns are not subjects
                subj_names_useable.append(item[0])
        cursor.close()
        return tuple(subj_names_useable)
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message='Select examination')
        return ()

def on_table_select(event):
    global selected_table
    global prev_table
    selected_table = table_combo.get()
    '''index=res2.index(selected_table)
    res2=get_tables()
    prev_table=res2[index-1]'''



def fetch_table_data(selected_table):
    try:
        cursor = db.cursor()
        query = f"SELECT * FROM `{selected_table}` ORDER BY `class`, `student_name`"
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        cursor.close()
        return column_names, data
    except mysql.connector.Error as err:
        print(f"Error fetching table data: {err}")
        return [], []

def fetch_prevtable_data(prev_table):
    try:
        cursor = db.cursor()
        query = f"SELECT * FROM `{prev_table}` ORDER BY `class`, `student_name`"
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        cursor.close()
        return column_names, data
    except mysql.connector.Error as err:
        print(f"Error fetching table data: {err}")
        return [], []
    
def calculate_class_average(selected_table, subject_names):
    try:
        cursor = db.cursor()
        avg_columns = ", ".join([f"AVG(`{sub}`) AS `{sub}_avg`" for sub in subject_names])
        query = f"SELECT {avg_columns} FROM `{selected_table}`"
        cursor.execute(query)
        class_averages = cursor.fetchone()
        cursor.close()
        return class_averages
    except mysql.connector.Error as err:
        print(f"Error calculating class average: {err}")
        return ()
def top_score(selected_table, subject_names):
    try:
        cursor = db.cursor()
        top_columns = ", ".join([f"MAX(`{sub}`) AS `{sub}_max`" for sub in subject_names])
        query = f"SELECT {top_columns} FROM `{selected_table}`"
        cursor.execute(query)
        top_scores = cursor.fetchone()
        cursor.close()
        top_scores = top_scores + top_scores
        return top_scores
    except mysql.connector.Error as err:
        print(f"Error fetching top scores: {err}")
        return ()


def show_student_and_class_avg():
    subject_names = fetch_subject_names(selected_table)
    prevexamsubnames=fetch_subject_names(prev_table)
    if not subject_names:
        print("No subjects found.")
        return
    elif not prevexamsubnames:
        print('No subjects in the previous exam')

    statement = f"SELECT * FROM `{selected_table}` WHERE student_id = {std_id}"
    cur.execute(statement)
    res = cur.fetchall()

    statement2 = f"SELECT * FROM `{prev_table}`  where student_id= {std_id}"
    cur.execute(statement2)
    res2 = cur.fetchall()
    # Extract student marks starting from the 4th column
    if res == [] or res2 == []:
        messagebox.showinfo(title="Error", message="You have not written this/prev exam")
    else:
        student_marks_current = res[0][3:8]
        student_marks_prev = res2[0][3:8]
        student_marks = student_marks_current + student_marks_prev
        class_averages = calculate_class_average(selected_table, subject_names)
        class_averages2  = calculate_class_average(prev_table, subject_names)
        
        class_averages = [float(avg) if avg is not None else 0 for avg in class_averages]
        class_averages2 = [float(avg) if avg is not None else 0 for avg in class_averages2]
        class_averages = class_averages + class_averages2
        statement = f"SELECT * FROM `{selected_table}` WHERE student_id = {std_id}"
        cur.execute(statement)
        res = cur.fetchall()

        statement2 = f"SELECT * FROM `{prev_table}` WHERE student_id = {std_id}"
        cur.execute(statement2)
        res2 = cur.fetchall()


        # Create a new window for the graph
        graph_window = tk.Toplevel(root)
        graph_window.title(f"Marks for {std_name}")
        graph_window.geometry("1400x1200")  # Increased size for better layout
        graph_window.resizable(True, True)  # Prevent resizing

        # Function to handle graph window close
        def on_graph_close():
            plt.close(fig)
            graph_window.destroy()

        graph_window.protocol("WM_DELETE_WINDOW", on_graph_close)

        # Create frames within the graph window
        info_frame = ttk.Frame(graph_window)
        info_frame.pack(pady=10, padx=10,anchor='w')
        marks_frame_graph = ttk.Frame(graph_window)
        marks_frame_graph.pack(pady=10, padx=10,anchor='w')
        
        # Student Information Labels
        student_name_label = ttk.Label(info_frame, text=f"Name: {std_name}", font=('Arial', 14, 'bold'))
        student_name_label.pack(anchor='w')
        student_class_label = ttk.Label(info_frame, text=f"Class: {std_class}", font=('Arial', 14, 'bold'))
        student_class_label.pack(anchor='w')
        extralabel=ttk.Label(info_frame,text='Current Exam Results: ',font=('Arial',14,'bold'))
        extralabel.pack(anchor='w')

        # Marks Treeview
        marks_tree = ttk.Treeview(marks_frame_graph, columns=("Subject", "Mark"), show='headings', height=len(subject_names))
        marks_tree.heading("Subject", text="Subject (Current Exam)")
        marks_tree.heading("Mark", text="Mark (Current Exam)")
        marks_tree.column("Subject", anchor="w", width=300)
        marks_tree.column("Mark", anchor="w", width=300)
        for subject, mark in zip(subject_names, student_marks):
            marks_tree.insert("", "end", values=(subject, mark if mark != 0 else "Absent"))
        marks_tree.pack(anchor='w',pady=10)

        # Calculate total and percentage
        total_marks = sum(student_marks_current)
        num_subjects = len(subject_names)
        percentage = (total_marks / (num_subjects * 100)) * 100 if num_subjects > 0 else 0
        low_subject, low = min(zip(subject_names, student_marks), key=lambda x: x[1])
        best_subject, best = max(zip(subject_names, student_marks), key=lambda x: x[1])

        # Display total marks, percentage, and subject performance
        total_label = ttk.Label(info_frame, text=f"Total Marks: {total_marks}", font=('Arial', 12, 'bold'))
        total_label.pack(anchor='w')
        percentage_label = ttk.Label(info_frame, text=f"Overall Aggregate: {percentage:.2f}%", font=('Arial', 12, 'bold'))
        percentage_label.pack(anchor='w')
        low_label = ttk.Label(info_frame, text=f"Worst Performing Subject: {low_subject} ({low:.2f})", font=('Arial', 12, 'bold'))
        low_label.pack(anchor='w')
        best_label = ttk.Label(info_frame, text=f"Best Performing Subject: {best_subject} ({best:.2f})", font=('Arial', 12, 'bold'))
        best_label.pack(anchor='w')

        # Plotting student marks, class averages, and top scores
        fig, ax = plt.subplots(figsize=(12.1, 12))  # Adjusted size for better fit
        bar_width = 0.2
        index = range(len(subject_names)*2)

        # Positions for each set of bars
        student_pos = [i - bar_width for i in index]
        average_pos = index
        top_pos = [i + bar_width for i in index]
        
        # Plotting the bars
        bars1 = ax.bar(student_pos, student_marks, bar_width, label=std_name, color='skyblue')
        bars2 = ax.bar(average_pos, class_averages, bar_width, label="Class Average", color='lightgreen')
        bars3 = ax.bar(top_pos, top_score(selected_table,subject_names), bar_width, label="Top Score", color='salmon')

        # Labels and Title
        ax.set_xlabel("Subjects")
        ax.set_ylabel("Marks")
        ax.set_xticks(index)
        subject_names  = subject_names + subject_names
        ax.set_xticklabels(subject_names, rotation=0, ha='right', fontsize=10)
        ax.set_ylim(0, max(max(student_marks), max(class_averages), max(top_score(selected_table,subject_names)), 100) + 10)
        ax.legend()
        
        # Adding bar value labels
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.annotate(f'{height:.1f}',
                                xy=(bar.get_x() + bar.get_width() /2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

        add_labels(bars1)
        add_labels(bars2)
        add_labels(bars3)

        

        plt.tight_layout()

        # Add graph to window
        canvas = FigureCanvasTkAgg(fig, master=marks_frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(anchor='w') 
        ax.axvline(4.5, color='black', linestyle='-')  
        text_x = 1.5
        text_y = 105
        text_str = "Current Exam"
        fontdict = {'family': 'serif', 'size': 14, 'weight': 'bold'}
        ax.text(text_x, text_y, text_str,fontdict=fontdict)
        text_x = 7
        text_y = 105
        text_str = "Previous Exam"
        fontdict = {'family': 'serif', 'size': 14, 'weight': 'bold'}
        ax.text(text_x, text_y, text_str,fontdict=fontdict)

        

# MAIN WINDOW
root = tk.Tk()
root.geometry("600x250")
root.title("Examination Marks")
sv_ttk.set_theme("light")

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_close)

# SCROLLABLE FRAME
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
second_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=second_frame, anchor="nw")

# TABLE SELECTION FRAME
table_frame = ttk.Frame(second_frame)
table_frame.pack(pady=10, anchor='center')

# Center-align the label and combobox using grid
table_label = ttk.Label(table_frame, text="Select Examination:", font=('Arial', 12, 'bold'))
table_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

table_combo = ttk.Combobox(table_frame, values=get_tables(), state="readonly", width=30, font=('Arial', 12))
table_combo.grid(row=0, column=1, padx=5, pady=5)
table_combo.current(0)  # Select the first exam by default
table_combo.set('')
table_combo.bind("<<ComboboxSelected>>", on_table_select)  # Bind event here

# BUTTON to show class-wise averages
avg_button = ttk.Button(table_frame, text="View marks", command=show_student_and_class_avg)
avg_button.grid(row=1, column=0, columnspan=2, pady=10)
sv_ttk.set_theme("dark")
root.mainloop()


