import tkinter as tk
from tkinter import Entry, Label, Button, font, IntVar, Checkbutton, Text, END, Toplevel
from datetime import datetime
from plyer import notification
import pygame
import os

class TaskScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Scheduler")
        self.root.configure(bg="#000000")  # Set background color to black

        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)
        self.entry_font = font.Font(family="Helvetica", size=12, weight="bold")

        self.birthday_var = IntVar()
        self.event_var = IntVar()
        self.recurring_var = IntVar()
        self.exam_var = IntVar()
        self.projectsubmission_var = IntVar()

        self.completed_tasks = []  # Store completed tasks

        self.create_label_main("Enter the task:").grid(row=0, column=0, sticky='w', pady=(10, 0), padx=10)
        self.entry_task_main = Entry(self.root, bg="#333333", fg="white", insertbackground="white", font=self.entry_font)
        self.entry_task_main.grid(row=0, column=1, pady=(10, 0), padx=10)

        self.create_label_main("Enter the date (dd/mm/yy):").grid(row=1, column=0, sticky='w', pady=5, padx=10)
        self.entry_date_main = Entry(self.root, bg="#333333", fg="white", insertbackground="white", font=self.entry_font)
        self.entry_date_main.grid(row=1, column=1, pady=5, padx=10)

        self.create_label_main("Enter the time (HH:MM):").grid(row=2, column=0, sticky='w', pady=5, padx=10)
        self.entry_time_main = Entry(self.root, bg="#333333", fg="white", insertbackground="white", font=self.entry_font)
        self.entry_time_main.grid(row=2, column=1, pady=5, padx=10)

        self.create_label_main("Select task type:").grid(row=3, column=0, sticky='w', pady=5, padx=10)

        self.checkbox_birthday = Checkbutton(self.root, text="Birthday", variable=self.birthday_var, bg="#000000", fg="white", font=self.label_font, selectcolor="#000000")
        self.checkbox_birthday.grid(row=4, column=0, sticky='w', pady=5, padx=10)

        self.checkbox_event = Checkbutton(self.root, text="Event", variable=self.event_var, bg="#000000", fg="white", font=self.label_font, selectcolor="#000000")
        self.checkbox_event.grid(row=5, column=0, sticky='w', pady=5, padx=10)

        self.checkbox_recurring = Checkbutton(self.root, text="Recurring", variable=self.recurring_var, bg="#000000", fg="white", font=self.label_font, selectcolor="#000000")
        self.checkbox_recurring.grid(row=6, column=0, sticky='w', pady=5, padx=10)

        self.checkbox_exam = Checkbutton(self.root, text="Exam", variable=self.exam_var, bg="#000000", fg="white", font=self.label_font, selectcolor="#000000")
        self.checkbox_exam.grid(row=7, column=0, sticky='w', pady=5, padx=10)

        self.checkbox_projectsubmission = Checkbutton(self.root, text="Project Submission", variable=self.projectsubmission_var, bg="#000000", fg="white", font=self.label_font, selectcolor="#000000")
        self.checkbox_projectsubmission.grid(row=8, column=0, sticky='w', pady=5, padx=10)

        self.button_schedule_task = Button(self.root, text="Schedule Task", command=self.schedule_task,
                                           bg="#E74C3C", fg="black", activebackground="#C0392B", activeforeground="black", font=self.label_font)
        self.button_schedule_task.grid(row=9, column=0, columnspan=2, pady=10)

        self.completed_button = Button(self.root, text="Completed", command=self.show_completed_tasks, bg="#3498db", fg="black", font=self.label_font)
        self.completed_button.grid(row=10, column=0, columnspan=2, pady=10)

    def create_label_main(self, text, font=None):
        return Label(self.root, text=text, bg="#000000", fg="white", font=font)

    def show_error(self, message):
        error_label = Label(self.root, text=message, bg="#000000", fg="red", font=self.label_font)
        error_label.grid(row=12, column=0, columnspan=2, pady=5)

    def schedule_task(self):
        task = self.entry_task_main.get()
        date_str = self.entry_date_main.get()
        time_str = self.entry_time_main.get()

        try:
            datetime_str = f"{date_str} {time_str}"
            execution_datetime = datetime.strptime(datetime_str, "%d/%m/%y %H:%M")
            now = datetime.now()

            if execution_datetime <= now:
                self.show_error("The specified time has already passed.")
                return

            time_until_execution = (execution_datetime - now).total_seconds()

            task_type = []
            if self.birthday_var.get():
                task_type.append("Birthday")
            if self.event_var.get():
                task_type.append("Event")
            if self.recurring_var.get():
                task_type.append("Recurring")
            if self.exam_var.get():
                task_type.append("Exam")
            if self.projectsubmission_var.get():
                task_type.append("Project Submission")

            task_type_str = ", ".join(task_type)

            self.root.after(int(time_until_execution * 1000), lambda: self.notify_user(task, task_type_str))
            print("Task scheduled:", task)

        except ValueError:
            self.show_error("Invalid date and time format. Please use 'dd/mm/yy' for date and 'HH:MM' for time.")

    def notify_user(self, completed_task, task_type):
        notification.notify(
            title="Scheduled Task",
            message=f"Task completed: {completed_task} ({task_type})",
            app_icon=None,
            timeout=10
        )

        # Play sound using pygame
        sound_file = "/Users/shejo/Desktop/Ringtone.mp3"
        if os.path.exists(sound_file):
            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()

        # Store completed task with timestamp
        completed_task_with_time = f"{completed_task} ({task_type}) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.completed_tasks.append(completed_task_with_time)

    def show_completed_tasks(self):
        completed_window = Toplevel(self.root)
        completed_window.title("Completed Tasks")

        completed_text = Text(completed_window, height=10, width=40, bg="#333333", fg="white", font=self.label_font)
        completed_text.pack(pady=10)

        back_button = Button(completed_window, text="Back", command=lambda: [completed_window.destroy(), self.root.deiconify()], bg="#E74C3C", fg="black", font=self.label_font)
        back_button.pack(pady=10)

        completed_text.insert(END, "Completed Tasks:\n")

        for task in self.completed_tasks:
            completed_text.insert(END, f"{task}\n")

# Create the main window
root = tk.Tk()
app = TaskScheduler(root)
root.mainloop()
