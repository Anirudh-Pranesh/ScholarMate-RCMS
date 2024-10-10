import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from subprocess import call
import sys  # Imported sys module
import pickle
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AdminPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Welcome Admin")
        self.geometry("850x700")  # Increased height for the graph

        # Initialize Sun Valley theme with the "dark" theme
        sv_ttk.set_theme("dark")

        # Access User details
        try:
            with open('client_details.dat', 'rb') as file:
                details = pickle.load(file)
            details = list(details[0])
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

        # Main content
        self.content_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.title_label = ttk.Label(self.content_frame, text="Admin Page", font=('Helvetica', 24, 'bold'))
        self.title_label.pack(pady=20)

        # Table (Placeholder for class averages)
        self.table_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.table_frame.pack(pady=20)

        table_label = ttk.Label(self.table_frame, text="Class Averages Table (Placeholder)", font=('Helvetica', 14))
        table_label.pack(pady=10)

        # Buttons frame
        self.buttons_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.buttons_frame.pack(pady=20)

        # Create Entry Sheet Button
        self.create_data_button = ttk.Button(
            self.buttons_frame, 
            text="Create entry sheet for new exam", 
            command=self.create_data, 
            style='TButton'
        )
        self.create_data_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.create_data_button.bind("<Enter>", lambda event: self.on_enter(event, self.create_data_button, "#2563EB"))
        self.create_data_button.bind("<Leave>", lambda event: self.on_leave(event, self.create_data_button))

        # Edit School Directory Button
        self.edit_school_directory_button = ttk.Button(
            self.buttons_frame, 
            text="Edit School Directory", 
            command=self.edit_school_directory, 
            style='TButton'
        )
        self.edit_school_directory_button.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.edit_school_directory_button.bind("<Enter>", lambda event: self.on_enter(event, self.edit_school_directory_button, "#2563EB"))
        self.edit_school_directory_button.bind("<Leave>", lambda event: self.on_leave(event, self.edit_school_directory_button))

        # Generate Report Card Button
        self.generate_report_button = ttk.Button(
            self.buttons_frame, 
            text="Generate Report Card", 
            command=self.generate_report_card, 
            style='TButton'
        )
        self.generate_report_button.grid(row=0, column=2, padx=20, pady=10, sticky="ew")
        self.generate_report_button.bind("<Enter>", lambda event: self.on_enter(event, self.generate_report_button, "#2563EB"))
        self.generate_report_button.bind("<Leave>", lambda event: self.on_leave(event, self.generate_report_button))

        # View Student Marks Button
        self.view_marks_button = ttk.Button(
            self.buttons_frame, 
            text="View student Marks", 
            command=self.view_marks, 
            style='TButton'
        )
        self.view_marks_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.view_marks_button.bind("<Enter>", lambda event: self.on_enter(event, self.view_marks_button, "#2563EB"))
        self.view_marks_button.bind("<Leave>", lambda event: self.on_leave(event, self.view_marks_button))

        # Edit Student Marks Button
        self.edit_marks_button = ttk.Button(
            self.buttons_frame, 
            text="Edit student Marks", 
            command=self.edit_marks, 
            style='TButton'
        )
        self.edit_marks_button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.edit_marks_button.bind("<Enter>", lambda event: self.on_enter(event, self.edit_marks_button, "#2563EB"))
        self.edit_marks_button.bind("<Leave>", lambda event: self.on_leave(event, self.edit_marks_button))

    def on_enter(self, event, widget, color):
        widget.configure(style="Hover.TButton")

    def on_leave(self, event, widget):
        widget.configure(style="TButton")

    def logout(self):
        self.destroy()
        # Use sys.executable to ensure the same Python interpreter is used
        call([sys.executable, 'login_page.py'])

    def create_data(self):
        call([sys.executable, 'DataEntrySheetForAdmin.py'])

    def view_marks(self):
        call([sys.executable, 'view_student_marks.py'])  # Link Python files here

    def edit_marks(self):
        call([sys.executable, 'edit_student_marks.py'])  # Link Python files here

    def generate_report_card(self):
        call([sys.executable, 'generate_report_card.py'])

    def edit_school_directory(self):
        call([sys.executable, 'edit_school_directory.py'])

    def changepassword(self):
        call([sys.executable, 'changepassword.py'])

if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()
    