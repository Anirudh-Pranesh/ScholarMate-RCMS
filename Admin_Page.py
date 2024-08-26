import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from subprocess import call

class AdminPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Welcome Admin")
        self.geometry("800x600")

        # Initialize Sun Valley theme with the "dark" theme
        sv_ttk.set_theme("dark")

        # Main content frame
        self.main_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar with a blue background
        self.sidebar = ttk.Frame(self.main_frame, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.sidebar_color = tk.Frame(self.sidebar, bg="#3B82F6", width=200, height=600)
        self.sidebar_color.pack(fill=tk.Y, side=tk.LEFT, expand=True)

        self.user_details = ttk.Label(self.sidebar_color, text="User details", font=('Helvetica', 14, 'bold'), background="#3B82F6", foreground="white")
        self.user_details.pack(pady=20, padx=10)

        self.logout_button = ttk.Button(self.sidebar_color, text="Click here to log out", command=self.logout, style='Sidebar.TButton')
        self.logout_button.pack(side=tk.BOTTOM, pady=20, padx=10)

        # Main content
        self.content_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.title_label = ttk.Label(self.content_frame, text="Admin Page", font=('Helvetica', 24, 'bold'))
        self.title_label.pack(pady=20)

        self.buttons_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.buttons_frame.pack(pady=20)

        # Buttons with hover effect
        self.create_data_button = ttk.Button(self.buttons_frame, text="Create New Data", command=self.create_data, style='TButton')
        self.create_data_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.create_data_button.bind("<Enter>", lambda event: self.on_enter(event, self.create_data_button, "#2563EB"))
        self.create_data_button.bind("<Leave>", lambda event: self.on_leave(event, self.create_data_button))

        self.view_edit_button = ttk.Button(self.buttons_frame, text="View/Edit Data", command=self.view_edit_data, style='TButton')
        self.view_edit_button.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.view_edit_button.bind("<Enter>", lambda event: self.on_enter(event, self.view_edit_button, "#2563EB"))
        self.view_edit_button.bind("<Leave>", lambda event: self.on_leave(event, self.view_edit_button))

        self.generate_report_button = ttk.Button(self.buttons_frame, text="Generate Report Card", command=self.generate_report_card, style='TButton')
        self.generate_report_button.grid(row=0, column=2, padx=20, pady=10, sticky="ew")
        self.generate_report_button.bind("<Enter>", lambda event: self.on_enter(event, self.generate_report_button, "#2563EB"))
        self.generate_report_button.bind("<Leave>", lambda event: self.on_leave(event, self.generate_report_button))

        self.edit_school_directory_button = ttk.Button(self.buttons_frame, text="Edit School Directory", command=self.edit_school_directory, style='TButton')
        self.edit_school_directory_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.edit_school_directory_button.bind("<Enter>", lambda event: self.on_enter(event, self.edit_school_directory_button, "#2563EB"))
        self.edit_school_directory_button.bind("<Leave>", lambda event: self.on_leave(event, self.edit_school_directory_button))

        self.quit_button = ttk.Button(self.buttons_frame, text="Quit", command=self.quit, style='TButton')
        self.quit_button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.quit_button.bind("<Enter>", lambda event: self.on_enter(event, self.quit_button, "#2563EB"))
        self.quit_button.bind("<Leave>", lambda event: self.on_leave(event, self.quit_button))

    def on_enter(self, event, widget, color):
        widget.configure(style="Hover.TButton")

    def on_leave(self, event, widget):
        widget.configure(style="TButton")

    def logout(self):
        self.destroy()
        call(['python', 'DataEntrySheetForAdmin.py'])

    def create_data(self):
        call(['python', 'login_page.py'])

    def view_edit_data(self):
        messagebox.showinfo("View/Edit Data", "View/Edit data function")

    def generate_report_card(self):
        messagebox.showinfo("Generate Report Card", "Generate report card function")

    def edit_school_directory(self):
        call(['python', 'edit_school_directory.py'])

if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()
