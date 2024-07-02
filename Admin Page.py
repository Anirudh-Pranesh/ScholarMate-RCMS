import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
from datetime import datetime

# Function to connect to MySQL
def connect_to_mysql():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',              # Replace with your MySQL server host
            database='school_info_registration',
            user='eneter user name',                   # Replace with your MySQL username
            password='enter password'      # Replace with your MySQL password
        )
        if connection.is_connected():
            print('Connected to MySQL database')

        return connection

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Function to insert student data into the students table
def insert_student(connection, first_name, last_name, email, password, date_of_birth, gender, enrollment_date):
    try:
        cursor = connection.cursor()

        # Convert date of birth to MySQL format 'YYYY-MM-DD'
        date_of_birth = datetime.strptime(date_of_birth, '%d/%m/%Y').strftime('%Y-%m-%d')

        # SQL query to insert a new student record
        insert_query = """
        INSERT INTO students (first_name, last_name, email, password, date_of_birth, gender, enrollment_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Data to insert
        data = (first_name, last_name, email, password, date_of_birth, gender, enrollment_date)

        # Execute the query
        cursor.execute(insert_query, data)
        connection.commit()

        print(f"Inserted {cursor.rowcount} row into students table")

        # Show success message
        messagebox.showinfo("Insertion Successful", f"Inserted {cursor.rowcount} row into students table")

    except Error as e:
        connection.rollback()
        print(f"Error inserting data into MySQL table: {e}")

        # Show error message
        messagebox.showerror("Insertion Error", f"Error inserting data into MySQL table:\n{e}")

    finally:
        cursor.close()

# Function to insert teacher data into the teachers table
def insert_teacher(connection, first_name, last_name, email, password):
    try:
        cursor = connection.cursor()

        # SQL query to insert a new teacher record
        insert_query = """
        INSERT INTO teachers (first_name, last_name, email, password)
        VALUES (%s, %s, %s, %s)
        """

        # Data to insert
        data = (first_name, last_name, email, password)

        # Execute the query
        cursor.execute(insert_query, data)
        connection.commit()

        print(f"Inserted {cursor.rowcount} row into teachers table")

        # Show success message
        messagebox.showinfo("Insertion Successful", f"Inserted {cursor.rowcount} row into teachers table")

    except Error as e:
        connection.rollback()
        print(f"Error inserting data into MySQL table: {e}")

        # Show error message
        messagebox.showerror("Insertion Error", f"Error inserting data into MySQL table:\n{e}")

    finally:
        cursor.close()

# Function to delete student or teacher record by email
def delete_record(connection, table_name, email):
    try:
        cursor = connection.cursor()

        # SQL query to delete a record
        delete_query = f"DELETE FROM {table_name} WHERE email = %s"

        # Execute the query
        cursor.execute(delete_query, (email,))
        connection.commit()

        print(f"Deleted {cursor.rowcount} row from {table_name} table")

        # Show success message
        messagebox.showinfo("Deletion Successful", f"Deleted {cursor.rowcount} row from {table_name} table")

    except Error as e:
        connection.rollback()
        print(f"Error deleting data from MySQL table: {e}")

        # Show error message
        messagebox.showerror("Deletion Error", f"Error deleting data from MySQL table:\n{e}")

    finally:
        cursor.close()

# Function to handle submit student button click event
def submit_student():
    # Retrieve values from student registration form
    first_name = entry_student_first_name.get()
    last_name = entry_student_last_name.get()
    email = entry_student_email.get()
    password = entry_student_password.get()
    date_of_birth = entry_student_date_of_birth.get()
    gender = entry_student_gender.get()
    enrollment_date = entry_student_enrollment_date.get()

    # Connect to MySQL
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        # Insert student record
        insert_student(connection, first_name, last_name, email, password, date_of_birth, gender, enrollment_date)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print('MySQL connection closed')

    # Clear input fields
    entry_student_first_name.delete(0, tk.END)
    entry_student_last_name.delete(0, tk.END)
    entry_student_email.delete(0, tk.END)
    entry_student_password.delete(0, tk.END)
    entry_student_date_of_birth.delete(0, tk.END)
    entry_student_gender.delete(0, tk.END)
    entry_student_enrollment_date.delete(0, tk.END)

    # Update student table display
    display_students()

# Function to handle submit teacher button click event
def submit_teacher():
    # Retrieve values from teacher registration form
    first_name = entry_teacher_first_name.get()
    last_name = entry_teacher_last_name.get()
    email = entry_teacher_email.get()
    password = entry_teacher_password.get()

    # Connect to MySQL
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        # Insert teacher record
        insert_teacher(connection, first_name, last_name, email, password)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print('MySQL connection closed')

    # Clear input fields
    entry_teacher_first_name.delete(0, tk.END)
    entry_teacher_last_name.delete(0, tk.END)
    entry_teacher_email.delete(0, tk.END)
    entry_teacher_password.delete(0, tk.END)

    # Update teacher table display
    display_teachers()

# Function to delete student button click event
def delete_student():
    # Retrieve email from entry box
    email = entry_delete_student.get()

    # Connect to MySQL
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        # Delete student record
        delete_record(connection, 'students', email)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print('MySQL connection closed')

    # Clear input field
    entry_delete_student.delete(0, tk.END)

    # Update student table display
    display_students()

# Function to delete teacher button click event
def delete_teacher():
    # Retrieve email from entry box
    email = entry_delete_teacher.get()

    # Connect to MySQL
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        # Delete teacher record
        delete_record(connection, 'teachers', email)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print('MySQL connection closed')

    # Clear input field
    entry_delete_teacher.delete(0, tk.END)

    # Update teacher table display
    display_teachers()

# Function to display students in a table
def display_students():
    # Connect to MySQL
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Select all students
        cursor.execute("SELECT first_name, last_name, email, password, date_of_birth, gender, enrollment_date FROM students")
        students = cursor.fetchall()

        # Clear previous items in treeview
        for item in treeview_students.get_children():
            treeview_students.delete(item)

        # Insert data into treeview
        for student in students:
            treeview_students.insert('', 'end', values=student)

    except Error as e:
        print(f"Error fetching data from MySQL table: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print('MySQL connection closed')

# Function to display teachers in a table
def display_teachers():
    # Connect to MySQL
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Select all teachers
        cursor.execute("SELECT first_name, last_name, email, password FROM teachers")
        teachers = cursor.fetchall()

        # Clear previous items in treeview
        for item in treeview_teachers.get_children():
            treeview_teachers.delete(item)

        # Insert data into treeview
        for teacher in teachers:
            treeview_teachers.insert('', 'end', values=teacher)

    except Error as e:
        print(f"Error fetching data from MySQL table: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print('MySQL connection closed')

# GUI
root = tk.Tk()
root.title("School Information Registration")

# Student Registration Section
frame_student_registration = ttk.LabelFrame(root, text="Student Registration")
frame_student_registration.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

# Labels and Entry Boxes for Student Registration
label_student_first_name = ttk.Label(frame_student_registration, text="First Name:")
label_student_first_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_student_first_name = ttk.Entry(frame_student_registration, width=30)
entry_student_first_name.grid(row=0, column=1, padx=5, pady=5)

label_student_last_name = ttk.Label(frame_student_registration, text="Last Name:")
label_student_last_name.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_student_last_name = ttk.Entry(frame_student_registration, width=30)
entry_student_last_name.grid(row=1, column=1, padx=5, pady=5)

label_student_email = ttk.Label(frame_student_registration, text="Email:")
label_student_email.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_student_email = ttk.Entry(frame_student_registration, width=30)
entry_student_email.grid(row=2, column=1, padx=5, pady=5)

label_student_password = ttk.Label(frame_student_registration, text="Password:")
label_student_password.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_student_password = ttk.Entry(frame_student_registration, width=30, show='*')
entry_student_password.grid(row=3, column=1, padx=5, pady=5)

label_student_date_of_birth = ttk.Label(frame_student_registration, text="Date of Birth (DD/MM/YYYY):")
label_student_date_of_birth.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
entry_student_date_of_birth = ttk.Entry(frame_student_registration, width=30)
entry_student_date_of_birth.grid(row=4, column=1, padx=5, pady=5)

label_student_gender = ttk.Label(frame_student_registration, text="Gender:")
label_student_gender.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
entry_student_gender = ttk.Entry(frame_student_registration, width=30)
entry_student_gender.grid(row=5, column=1, padx=5, pady=5)

label_student_enrollment_date = ttk.Label(frame_student_registration, text="Enrollment Date:")
label_student_enrollment_date.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
entry_student_enrollment_date = ttk.Entry(frame_student_registration, width=30)
entry_student_enrollment_date.grid(row=6, column=1, padx=5, pady=5)

# Submit Student Button
button_submit_student = ttk.Button(frame_student_registration, text="Submit", command=submit_student)
button_submit_student.grid(row=7, columnspan=2, padx=5, pady=5)

# Entry Box for deleting a student
label_delete_student = ttk.Label(root, text="Enter Student Email to Delete:")
label_delete_student.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
entry_delete_student = ttk.Entry(root, width=30)
entry_delete_student.grid(row=0, column=1, padx=150, pady=10, sticky=tk.W)

# Delete Student Button
button_delete_student = ttk.Button(root, text="Delete Student", command=delete_student)
button_delete_student.grid(row=0, column=1, padx=280, pady=10, sticky=tk.W)

# Teacher Registration Section
frame_teacher_registration = ttk.LabelFrame(root, text="Teacher Registration")
frame_teacher_registration.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

# Labels and Entry Boxes for Teacher Registration
label_teacher_first_name = ttk.Label(frame_teacher_registration, text="First Name:")
label_teacher_first_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_teacher_first_name = ttk.Entry(frame_teacher_registration, width=30)
entry_teacher_first_name.grid(row=0, column=1, padx=5, pady=5)

label_teacher_last_name = ttk.Label(frame_teacher_registration, text="Last Name:")
label_teacher_last_name.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_teacher_last_name = ttk.Entry(frame_teacher_registration, width=30)
entry_teacher_last_name.grid(row=1, column=1, padx=5, pady=5)

label_teacher_email = ttk.Label(frame_teacher_registration, text="Email:")
label_teacher_email.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_teacher_email = ttk.Entry(frame_teacher_registration, width=30)
entry_teacher_email.grid(row=2, column=1, padx=5, pady=5)

label_teacher_password = ttk.Label(frame_teacher_registration, text="Password:")
label_teacher_password.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_teacher_password = ttk.Entry(frame_teacher_registration, width=30, show='*')
entry_teacher_password.grid(row=3, column=1, padx=5, pady=5)

# Submit Teacher Button
button_submit_teacher = ttk.Button(frame_teacher_registration, text="Submit", command=submit_teacher)
button_submit_teacher.grid(row=4, columnspan=2, padx=5, pady=5)

# Entry Box for deleting a teacher
label_delete_teacher = ttk.Label(root, text="Enter Teacher Email to Delete:")
label_delete_teacher.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
entry_delete_teacher = ttk.Entry(root, width=30)
entry_delete_teacher.grid(row=1, column=1, padx=150, pady=10, sticky=tk.W)

# Delete Teacher Button
button_delete_teacher = ttk.Button(root, text="Delete Teacher", command=delete_teacher)
button_delete_teacher.grid(row=1, column=1, padx=280, pady=10, sticky=tk.W)

# Treeview for displaying students
treeview_students = ttk.Treeview(root, columns=('First Name', 'Last Name', 'Email', 'Password', 'Date of Birth', 'Gender', 'Enrollment Date'), show='headings')
treeview_students.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NSEW)
treeview_students.heading('First Name', text='First Name')
treeview_students.heading('Last Name', text='Last Name')
treeview_students.heading('Email', text='Email')
treeview_students.heading('Password', text='Password')
treeview_students.heading('Date of Birth', text='Date of Birth')
treeview_students.heading('Gender', text='Gender')
treeview_students.heading('Enrollment Date', text='Enrollment Date')

# Treeview for displaying teachers
treeview_teachers = ttk.Treeview(root, columns=('First Name', 'Last Name', 'Email', 'Password'), show='headings')
treeview_teachers.grid(row=1, column=2, padx=10, pady=10, sticky=tk.NSEW)
treeview_teachers.heading('First Name', text='First Name')
treeview_teachers.heading('Last Name', text='Last Name')
treeview_teachers.heading('Email', text='Email')
treeview_teachers.heading('Password', text='Password')

# Function to display initial data in tables
def display_initial_data():
    # Display initial students and teachers data
    display_students()
    display_teachers()

# Initialize display of data
display_initial_data()

# Start GUI main loop
root.mainloop()
