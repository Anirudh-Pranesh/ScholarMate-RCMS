import pickle
import tkinter
from tkinter import ttk
import sv_ttk

# Load teacher details (this would typically be loaded from a binary file or database)
with open('client_details.dat', 'rb') as file:
    details = pickle.load(file)

details = list(details[0])
window = tkinter.Tk()
window.title('Teacher')
window.geometry('650x650')

# Welcome label
welcome_label = ttk.Label(window, text='Welcome ' + details[2], font=('Arial', 20))
welcome_label.pack(pady=20)

# Placeholder for selecting class
class_label = ttk.Label(window, text='Select Class:', font=('Arial', 15))
class_label.pack(pady=10)

class_combobox = ttk.Combobox(window, values=["Class 1", "Class 2", "Class 3", "Class 4"], font=('Arial', 12))
class_combobox.pack(pady=10)

# Button to fetch students (this button will connect to SQL later)
fetch_button = ttk.Button(window, text='Fetch Students', command=lambda: None)  # Replace None with function later
fetch_button.pack(pady=10)

# Table for displaying students and grades (for now, it's empty)
table_frame = ttk.Frame(window)
table_frame.pack(pady=20)

# Add headers for students and grades
ttk.Label(table_frame, text='Student Name', font=('Arial', 15), width=20).grid(row=0, column=0, padx=10)
ttk.Label(table_frame, text='Class', font=('Arial', 15), width=15).grid(row=0, column=1, padx=10)
ttk.Label(table_frame, text='Grade', font=('Arial', 15), width=15).grid(row=0, column=2, padx=10)

# Placeholder rows for future students and grades
for i in range(5):
    ttk.Label(table_frame, text='Student ' + str(i + 1), font=('Arial', 12)).grid(row=i + 1, column=0, padx=10)
    ttk.Label(table_frame, text='Class ' + str(i + 1), font=('Arial', 12)).grid(row=i + 1, column=1, padx=10)
    # Uncomment and connect to SQL later
    # grade_query = "SELECT grade FROM student_grades WHERE student_name='Student {}'".format(i + 1)  # SQL query to fetch grades
    # ttk.Label(table_frame, text=fetch_grade_from_sql(grade_query), font=('Arial', 12)).grid(row=i + 1, column=2, padx=10)
    ttk.Label(table_frame, text='-', font=('Arial', 12)).grid(row=i + 1, column=2, padx=10)  # Placeholder for grades

# Set dark theme
sv_ttk.set_theme("dark")

# Run the application
window.mainloop()
