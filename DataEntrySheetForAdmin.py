import tkinter as tk
from tkinter import ttk, messagebox;
import sv_ttk
import mysql.connector
from mysql.connector import Error

def tablecreation():
    try:
        # Connect to the database
        vighneshdb=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
        #vighneshdb=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
        cursor1 = vighneshdb.cursor()
        
        # Retrieve values from entries and checkbuttons
        examname = exam_entry.get()
        sub1 = subject1_entry.get()
        sub2 = subject2_entry.get()
        sub3 = subject3_entry.get()
        sub4 = subject4_entry.get()
        sub5 = subject5_entry.get()
        
        # Create SQL statement with proper spacing and quotes
        str = (
        f"CREATE TABLE IF NOT EXISTS {examname} ("
        "student_id INT, "
        "student_name VARCHAR(30) NOT NULL, "
        "class VARCHAR(3) NOT NULL, "
        f"{sub1} DECIMAL(4,1), "
        f"{sub2} DECIMAL(4,1), "
        f"{sub3} DECIMAL(4,1), "
        f"{sub4} DECIMAL(4,1), "
        f"{sub5} DECIMAL(4,1), "
        f"CHECK({sub1} <= 100.0 AND {sub1} >= 0), "
        f"CHECK({sub2} <= 100.0 AND {sub2} >= 0), "
        f"CHECK({sub3} <= 100.0 AND {sub3} >= 0), "
        f"CHECK({sub4} <= 100.0 AND {sub4} >= 0), "
        f"CHECK({sub5} <= 100.0 AND {sub5} >= 0), "
        "FOREIGN KEY(student_id) REFERENCES student_details(student_id)"
        ");"
        )

        cursor1.execute(str)
        vighneshdb.commit()

        available_classes={'9':class9var.get(),'10':class10var.get(), '11':class11var.get(), '12':class12var.get()}
        selected_classes=[]
        for i in available_classes:
            if available_classes[i] == 1:
                selected_classes.append(i)
        for i in selected_classes:
            str=(
            f"INSERT INTO {examname}(student_id, student_name, class) "
            "SELECT student_id, student_name, class "
            "FROM student_details "
            f"WHERE class LIKE '{i}%';"
            )
            cursor1.execute(str)
        vighneshdb.commit()
        # Close the connection
        vighneshdb.close()
        messagebox.showinfo("Info", f"Table '{examname}' created successfully.")
    except Error as e:
        messagebox.showerror("ERROR", f"Error: {e}")

# Initialize the Tkinter window
root = tk.Tk()
root.geometry('800x500')
root.title('Data Entry Sheet For Admin')

# Create and place widgets
title_label = ttk.Label(root, text='Data Entry Sheet for Admin', font=('Arial', 28, 'bold'))
exam_label = ttk.Label(root, text='1. Enter exam name here:', font=('calibre', 14, 'bold'))
exam_entry = ttk.Entry(root)
subject1_label = ttk.Label(root, text='a. Enter subject 1 here:', font=('calibre', 14, 'bold'))
subject1_entry = ttk.Entry(root)
subject2_label = ttk.Label(root, text='b. Enter subject 2 here:', font=('calibre', 14, 'bold'))
subject2_entry = ttk.Entry(root)
subject3_label = ttk.Label(root, text='c. Enter subject 3 here:', font=('calibre', 14, 'bold'))
subject3_entry = ttk.Entry(root)
subject4_label = ttk.Label(root, text='d. Enter subject 4 here:', font=('calibre', 14, 'bold'))
subject4_entry = ttk.Entry(root)
subject5_label = ttk.Label(root, text='e. Enter subject 5 here:', font=('calibre', 14, 'bold'))
subject5_entry = ttk.Entry(root)
class_label = ttk.Label(root, text='2. Click on the classes for which the exam was held for:', font=('calibre', 14, 'bold'))

# Checkbox variables
class9var = tk.IntVar()
class10var = tk.IntVar()
class11var = tk.IntVar()
class12var = tk.IntVar()

# Checkbuttons for classes
class9 = ttk.Checkbutton(root, text='Class 9', onvalue=1, offvalue=0, variable=class9var)
class10 = ttk.Checkbutton(root, text='Class 10', onvalue=1, offvalue=0, variable=class10var)
class11 = ttk.Checkbutton(root, text='Class 11', onvalue=1, offvalue=0, variable=class11var)
class12 = ttk.Checkbutton(root, text='Class 12', onvalue=1, offvalue=0, variable=class12var)

# Button to create table
button1 = ttk.Button(root, text='Create data entry sheet', command=tablecreation)

# Empty Labels for spacing
emptylabel1 = ttk.Label(root, text='')
emptylabel2 = ttk.Label(root, text='')
emptylabel3 = ttk.Label(root, text='')
emptylabel4 = ttk.Label(root, text='')
emptylabel5 = ttk.Label(root, text='')
emptylabel6 = ttk.Label(root, text='')

# Positioning of Widgets
emptylabel1.grid(row=0, column=2, columnspan=5)
emptylabel3.grid(row=1, column=2, columnspan=2)
title_label.grid(row=1, column=4, columnspan=2)
emptylabel2.grid(row=2, column=0, columnspan=2)
exam_label.grid(row=3, column=4)
exam_entry.grid(row=3, column=5)
subject1_label.grid(row=5, column=4)
subject1_entry.grid(row=5, column=5)
subject2_label.grid(row=6, column=4)
subject2_entry.grid(row=6, column=5)
subject3_label.grid(row=7, column=4)
subject3_entry.grid(row=7, column=5)
subject4_label.grid(row=8, column=4)
subject4_entry.grid(row=8, column=5)
subject5_label.grid(row=9, column=4)
subject5_entry.grid(row=9, column=5)
emptylabel4.grid(row=10, column=4)
class_label.grid(row=11, column=4)
emptylabel5.grid(row=12, column=4)
class9.grid(row=13, column=4)
class10.grid(row=14, column=4)
class11.grid(row=15, column=4)
class12.grid(row=16, column=4)
emptylabel6.grid(row=17, column=4, columnspan=2)
button1.grid(row=18, column=4)

# Custom Theme
sv_ttk.set_theme('dark')

# Start the Tkinter main loop
root.mainloop()
