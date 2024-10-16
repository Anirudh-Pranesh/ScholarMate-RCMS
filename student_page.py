import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from subprocess import call
import sys
import pickle
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector  # Ensure you have the MySQL connector installed

class AdminPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Welcome Student")
        self.geometry("850x700")

        sv_ttk.set_theme("dark")

        try:
            with open('client_details.dat', 'rb') as file:
                details = pickle.load(file)
            details = list(details[0])
        except (FileNotFoundError, EOFError, IndexError) as e:
            messagebox.showerror("Error", "Failed to load user details.")
            self.destroy()
            return

        self.main_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar = ttk.Frame(self.main_frame, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.sidebar_color = tk.Frame(self.sidebar, bg="#3B82F6", width=200, height=600)
        self.sidebar_color.pack(fill=tk.Y, side=tk.LEFT, expand=True)

        self.user_details = ttk.Label(
            self.sidebar_color,
            text="Welcome\n" + details[2],
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

        self.content_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.title_label = ttk.Label(self.content_frame, text="Student Portal", font=('Helvetica', 24, 'bold'))
        self.title_label.pack(pady=20)

        self.buttons_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.buttons_frame.pack(pady=20)

        self.create_data_button = ttk.Button(
            self.buttons_frame,
            text="View your marks",
            command=self.view_student_marks,
            style='TButton'
        )
        
        self.create_data_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.create_data_button.bind("<Enter>", lambda event: self.on_enter(event, self.create_data_button, "#2563EB"))
        self.create_data_button.bind("<Leave>", lambda event: self.on_leave(event, self.create_data_button))

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

    def view_student_marks(self):
        # Create a new window for viewing student marks
        marks_window = tk.Toplevel(self)
        marks_window.title("View Student Marks")
        marks_window.geometry("600x400")

        # Dropdown for selecting tables
        self.selected_table = tk.StringVar()
        table_label = ttk.Label(marks_window, text="Select Table:")
        table_label.pack(pady=10)

        # Example list of tables; replace this with actual table names from your database
        table_names = ['semester1', 'semester2', 'semester3']
        table_dropdown = ttk.Combobox(marks_window, textvariable=self.selected_table, values=table_names)
        table_dropdown.pack(pady=10)
        table_dropdown.bind("<<ComboboxSelected>>", self.load_student_marks)

        self.marks_text = tk.Text(marks_window, width=70, height=10)
        self.marks_text.pack(pady=10)

        # Button to load marks
        load_button = ttk.Button(marks_window, text="Load Marks", command=self.load_student_marks)
        load_button.pack(pady=10)

        self.graph_canvas = FigureCanvasTkAgg(plt.figure(), marks_window)
        self.graph_canvas.get_tk_widget().pack(pady=20)

    def load_student_marks(self, event=None):
        selected_table = self.selected_table.get()
        student_id = '1'  # Replace with the actual student ID to filter marks

        try:
            connection = mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db')
            cursor = connection.cursor()

            # Query to fetch marks and average
            cursor.execute(f"SELECT * FROM {selected_table} WHERE student_id = %s", (student_id,))
            student_marks = cursor.fetchone()

            cursor.execute(f"SELECT AVG(mark) FROM {selected_table}")
            class_average = cursor.fetchone()[0]

            # Display marks in text widget
            self.marks_text.delete(1.0, tk.END)
            if student_marks:
                self.marks_text.insert(tk.END, f"Marks: {student_marks}\nClass Average: {class_average}\n")
            else:
                self.marks_text.insert(tk.END, "No marks found for this student.")

            # Create graph
            subjects = ['Subject 1', 'Subject 2', 'Subject 3']  # Replace with actual subjects
            marks = student_marks[1:]  # Skip the first column (student_id) if necessary
            plt.clf()  # Clear previous figures
            plt.bar(subjects, marks, label='Your Marks')
            plt.axhline(y=class_average, color='r', linestyle='--', label='Class Average')
            plt.title(f"Marks vs Class Average")
            plt.xlabel('Subjects')
            plt.ylabel('Marks')
            plt.legend()
            plt.xticks(rotation=45)
            self.graph_canvas.draw()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def generate_report_card(self):
        call([sys.executable, 'generate_report_card_student.py'])

    def changepassword(self):
        call([sys.executable, 'changepassword.py'])

if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()
