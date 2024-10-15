import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from subprocess import call
import sys
import pickle
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector  # Import mysql connector

class AdminPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Welcome Student")
        self.geometry("850x700")

        # Initialize Sun Valley theme with the "dark" theme
        sv_ttk.set_theme("dark")

        # Access User details
        try:
            with open('client_details.dat', 'rb') as file:
                details = pickle.load(file)
            details = list(details[0])
            self.student_name = details[2]  # Store user name for fetching marks
        except (FileNotFoundError, EOFError, IndexError) as e:
            messagebox.showerror("Error", "Failed to load user details.")
            self.destroy()
            return

        # Main content frame
        self.main_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar with a blue background
        self.sidebar = ttk.Frame(self.main_frame, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.sidebar_color = tk.Frame(self.sidebar, bg="#3B82F6", width=200, height=600)
        self.sidebar_color.pack(fill=tk.Y, side=tk.LEFT, expand=True)

        self.user_details = ttk.Label(
            self.sidebar_color,
            text="Welcome\n" + self.student_name,
            font=('Helvetica', 14, 'bold'),
            background="#3B82F6",
            foreground="white"
        )
        self.user_details.pack(pady=20, padx=10)

        try:
            image = Image.open("usericon.png")
            image = image.resize((150, 90), Image.Resampling.LANCZOS)
            self.new_img = ImageTk.PhotoImage(image)
            self.button = tk.Button(
                self.sidebar_color,
                image=self.new_img,
                command=self.changepassword,
                borderwidth=0
            )
            self.button.pack()
        except Exception as e:
            messagebox.showerror("Error", "Failed to load user icon.")

        self.logout_button = ttk.Button(
            self.sidebar_color,
            text="Log out",
            command=self.logout,
            style='Sidebar.TButton'
        )
        self.logout_button.pack(side=tk.BOTTOM, pady=20, padx=10)

        # Main content
        self.content_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.title_label = ttk.Label(self.content_frame, text="Student Portal", font=('Helvetica', 24, 'bold'))
        self.title_label.pack(pady=20)

        # Buttons frame
        self.buttons_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.buttons_frame.pack(pady=20)

        # View Student Marks Button
        self.view_student_marks_button = ttk.Button(
            self.buttons_frame,
            text="View your marks",
            command=self.open_marks_window,
            style='TButton'
        )
        self.view_student_marks_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.view_student_marks_button.bind("<Enter>", lambda event: self.on_enter(event, self.view_student_marks_button, "#2563EB"))
        self.view_student_marks_button.bind("<Leave>", lambda event: self.on_leave(event, self.view_student_marks_button))

        # Generate Report Card Button
        self.generate_report_button = ttk.Button(
            self.buttons_frame,
            text="Generate Your Report Card",
            command=self.generate_report_card,
            style='TButton'
        )
        self.generate_report_button.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.generate_report_button.bind("<Enter>", lambda event: self.on_enter(event, self.generate_report_button, "#2563EB"))
        self.generate_report_button.bind("<Leave>", lambda event: self.on_leave(event, self.generate_report_button))

    def on_enter(self, event, widget, color):
        widget.configure(style="Hover.TButton")

    def on_leave(self, event, widget):
        widget.configure(style="TButton")

    def logout(self):
        self.destroy()
        call([sys.executable, 'login_page.py'])

    def open_marks_window(self):
        self.marks_window = tk.Toplevel(self)
        self.marks_window.title("View Student Marks")
        self.marks_window.geometry("600x400")

        # Dropdown for selecting table
        self.table_var = tk.StringVar()
        self.table_dropdown = ttk.Combobox(self.marks_window, textvariable=self.table_var)
        self.table_dropdown.pack(pady=20)

        # Fetch table names from the database
        self.fetch_table_names()

        # Button to load marks
        self.load_marks_button = ttk.Button(self.marks_window, text="Load Marks", command=self.load_marks)
        self.load_marks_button.pack(pady=20)

        # Treeview for displaying marks
        self.tree = ttk.Treeview(self.marks_window, columns=("Subject", "Marks"), show='headings')
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Marks", text="Marks")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Canvas for plotting graph
        self.canvas = FigureCanvasTkAgg(plt.figure(), master=self.marks_window)
        self.canvas.get_tk_widget().pack()

    def fetch_table_names(self):
        try:
            connection = mysql.connector.connect(
                host="mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com",
                port=13426,
                user="avnadmin",
                password="AVNS_1UgkIMxSzsCWt0D-3cB",
                database="scholarmate_db"
            )
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            self.table_dropdown['values'] = table_names
            if table_names:
                self.table_dropdown.current(0)  # Select the first table by default
            cursor.close()
            connection.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch tables: {e}")

    def load_marks(self):
        selected_table = self.table_var.get()
        try:
            connection = mysql.connector.connect(
                host="mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com",
                port=13426,
                user="avnadmin",
                password="AVNS_1UgkIMxSzsCWt0D-3cB",
                database="scholarmate_db"
            )
            cursor = connection.cursor()

            # Query to fetch only the selected student's marks
            query = f"SELECT * FROM {selected_table} WHERE student_name = %s"
            cursor.execute(query, (self.student_name,))
            rows = cursor.fetchall()

            # Clear previous data in the Treeview
            self.tree.delete(*self.tree.get_children())

            if not rows:
                messagebox.showinfo("No Data", "No marks found for this student.")
                return

            # Get subject names from the table's column names
            column_names = [desc[0] for desc in cursor.description]
            subjects = [col for col in column_names if col not in ['student_id', 'student_name', 'class']]  # Exclude ID, Name, Class

            marks = rows[0]  # Get the first row of marks since there should only be one student

            for subject, mark in zip(subjects, marks):
                self.tree.insert("", tk.END, values=(subject, mark if mark is not None else 'Absent'))

            # Generate and display the graph
            self.plot_graph(marks, subjects)

            cursor.close()
            connection.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch marks: {e}")

    def plot_graph(self, marks, subjects):
        marks_values = [mark if mark is not None else 0 for mark in marks]  # Replace None with 0

        plt.clf()  # Clear the current figure
        plt.bar(subjects, marks_values, color='blue')
        plt.xlabel('Subjects')
        plt.ylabel('Marks')
        plt.title('Student Marks')
        plt.ylim(0, 100)  # Assuming marks are out of 100
        plt.grid(axis='y')

        self.canvas.draw()  # Refresh the canvas with the new graph

    def generate_report_card(self):
        call([sys.executable, 'generate_report_card_student.py'])

    def changepassword(self):
        call([sys.executable, 'changepassword.py'])

if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()
