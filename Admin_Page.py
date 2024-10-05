import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from subprocess import call
import pickle
from PIL import ImageTk
from PIL import Image
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
        file = open('client_details.dat', 'rb')
        details = pickle.load(file)
        file.close()
        details = list(details[0])

        # Main content frame
        self.main_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar with a blue background
        self.sidebar = ttk.Frame(self.main_frame, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.sidebar_color = tk.Frame(self.sidebar, bg="#3B82F6", width=200, height=600)
        self.sidebar_color.pack(fill=tk.Y, side=tk.LEFT, expand=True)

        self.user_details = ttk.Label(self.sidebar_color, text="Welcome\n"+details[2], font=('Helvetica', 14, 'bold'), background="#3B82F6", foreground="white")
        self.user_details.pack(pady=20, padx=10)

        image = Image.open("usericon.png")
        image = image.resize((150, 90), Image.Resampling.LANCZOS)
        self.new_img = ImageTk.PhotoImage(image)
        self.button = tk.Button(self.sidebar_color, image=self.new_img, command=self.changepassword, borderwidth=0)
        self.button.pack()

        self.logout_button = ttk.Button(self.sidebar_color, text="Log out", command=self.logout, style='Sidebar.TButton')
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

        self.create_data_button = ttk.Button(self.buttons_frame, text="Create entry sheet for new exam", command=self.create_data, style='TButton')
        self.create_data_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.create_data_button.bind("<Enter>", lambda event: self.on_enter(event, self.create_data_button, "#2563EB"))
        self.create_data_button.bind("<Leave>", lambda event: self.on_leave(event, self.create_data_button))

        self.edit_school_directory_button = ttk.Button(self.buttons_frame, text="Edit School Directory", command=self.edit_school_directory, style='TButton')
        self.edit_school_directory_button.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.edit_school_directory_button.bind("<Enter>", lambda event: self.on_enter(event, self.edit_school_directory_button, "#2563EB"))
        self.edit_school_directory_button.bind("<Leave>", lambda event: self.on_leave(event, self.edit_school_directory_button))

        self.generate_report_button = ttk.Button(self.buttons_frame, text="Generate Report Card", command=self.generate_report_card, style='TButton')
        self.generate_report_button.grid(row=0, column=2, padx=20, pady=10, sticky="ew")
        self.generate_report_button.bind("<Enter>", lambda event: self.on_enter(event, self.generate_report_button, "#2563EB"))
        self.generate_report_button.bind("<Leave>", lambda event: self.on_leave(event, self.generate_report_button))

        self.view_edit_button = ttk.Button(self.buttons_frame, text="View student Marks", command=self.view_marks, style='TButton')
        self.view_edit_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.view_edit_button.bind("<Enter>", lambda event: self.on_enter(event, self.view_edit_button, "#2563EB"))
        self.view_edit_button.bind("<Leave>", lambda event: self.on_leave(event, self.view_edit_button))

        self.view_edit_button = ttk.Button(self.buttons_frame, text="Edit student Marks", command=self.edit_marks, style='TButton')
        self.view_edit_button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.view_edit_button.bind("<Enter>", lambda event: self.on_enter(event, self.view_edit_button, "#2563EB"))
        self.view_edit_button.bind("<Leave>", lambda event: self.on_leave(event, self.view_edit_button))

        # Empty Bar Graph below the table
        self.graph_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Create an empty figure for the bar graph with dark theme
        self.create_empty_bar_graph()

    def create_empty_bar_graph(self):
        fig, ax = plt.subplots(figsize=(6, 3))

        # Customize bar graph for dark theme
        fig.patch.set_facecolor('#212121')  # Background color of the graph
        ax.set_facecolor('#303030')  # Background color inside the plot area

        ax.bar([], [])  # Empty bar graph
        ax.set_title('Class Averages', color='white', fontsize=14)  # White text for the title
        ax.set_xlabel('Subjects', color='white', fontsize=12)  # White text for X-axis
        ax.set_ylabel('Average Marks', color='white', fontsize=12)  # White text for Y-axis

        # Customize ticks, grid, and labels for dark theme
        ax.tick_params(colors='white')  # White ticks
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.grid(color='gray', linestyle='--', linewidth=0.5)

        # Create a canvas to place the figure inside the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_enter(self, event, widget, color):
        widget.configure(style="Hover.TButton")

    def on_leave(self, event, widget):
        widget.configure(style="TButton")

    def logout(self):
        self.destroy()
        call(['python', 'login_page.py'])

    def create_data(self):
        call(['python', 'DataEntrySheetForAdmin.py'])

    def view_marks(self):
        messagebox.showinfo("View/Edit Data", "View/Edit data function")  # link python files here

    def edit_marks(self):
        messagebox.showinfo("View/Edit Data", "View/Edit data function")  # link python files here

    def generate_report_card(self):
        call(['python', 'generate_report_card.py'])

    def edit_school_directory(self):
        call(['python', 'edit_school_directory.py'])

    def changepassword(self):
        call(['python', 'changepassword.py'])

if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()




