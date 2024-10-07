# generate_report_card.py

# Import statements
import tkinter
from tkinter import ttk
import sv_ttk
from tkinter import messagebox
import time
import threading
import pdfgenerator as pdfg  # Ensure pdfgenerator.py is in the same directory

# Window and frame setup
window = tkinter.Tk()
window.title('Generate Report Card')
window.geometry('1000x800')  # Adjusted to a reasonable size

common_options_frame = ttk.Frame(window)       # Main frame to select exam and options
multiple_student_frame = ttk.Frame(window)     # Frame for multiple students
single_student_frame = ttk.Frame(window)       # Frame for single student

def show_common_opt():
    common_options_frame.pack(fill="both", expand=True)

def show_multiple_student():
    multiple_student_frame.pack(fill="both", expand=True)

def show_single_student():
    single_student_frame.pack(fill="both", expand=True)

def update_window():
    opt = selected_option.get()
    if opt == 'multiple':
        single_student_frame.pack_forget()
        show_multiple_student()
    elif opt == 'single':
        multiple_student_frame.pack_forget()
        show_single_student()
    else:
        show_common_opt()

def start_generating_multiple():
    generating_text_multiple.grid(row=4, column=0, sticky='W', pady=10)
    # Start the generation in a separate thread to keep UI responsive
    threading.Thread(target=generate_multiple_rc_func, daemon=True).start()

def generate_multiple_rc_func():
    try:
        # Collect selected classes
        selected_classes = []
        if class9var.get() == 1:
            selected_classes.append('9')
        if class10var.get() == 1:
            selected_classes.append('10')
        if class11var.get() == 1:
            selected_classes.append('11')
        if class12var.get() == 1:
            selected_classes.append('12')

        if selected_classes and selected_exam:
            # Sample student data (replace with actual data retrieval logic)
            sample_students = [
                {'std_id': 'S001', 'std_name': 'Alice Johnson', 'std_class': '10A', 'scores': [85, 90, 78, 92, 88]},
                {'std_id': 'S002', 'std_name': 'Bob Smith', 'std_class': '10A', 'scores': [75, 80, 68, 82, 78]},
                # Add more sample students as needed
            ]

            # Sample subject names
            subj_names_useable = ['Math', 'Science', 'English', 'History', 'Art']

            # Sample top scores and average scores
            top_score = [95, 93, 88, 90, 85]
            avg_score = [80, 82, 75, 78, 80]

            for student in sample_students:
                pdfg.generate_report_card(
                    student['std_name'],
                    "Mr. Anderson",          # Sample teacher name
                    "parent@example.com",    # Sample parent contact
                    "123-456-7890",          # Sample teacher contact
                    student['std_class'],
                    selected_exam,
                    student['scores'],
                    top_score,
                    avg_score,
                    student['std_id'],
                    subj_names_useable
                )
            generating_text_multiple.grid_forget()
            messagebox.showinfo(title='Info', message='PDFs for report cards generated. Please check in the script directory.')
        else:
            messagebox.showwarning(title='WARNING', message='Please select at least one class and confirm your exam selection.')
    except Exception as e:
        generating_text_multiple.grid_forget()
        messagebox.showerror(title='ERROR', message=f'Unexpected error encountered: {str(e)}')

def select_exam_func():
    global selected_exam
    try:
        selected_item = exams_trv.selection()[0]
        selected_exam = exams_trv.item(selected_item)['values'][0]
    except IndexError:
        messagebox.showerror(title='ERROR', message='Examination not selected')
        selected_exam = None
        return
    messagebox.showinfo(title='Examination Selected', message=f'{selected_exam} has been selected')

def generate_single_rc_func():
    try:
        selected_student = students_trv.selection()[0]
        if selected_student and selected_exam:
            # Sample student data (replace with actual data retrieval logic)
            sample_student = {
                'std_id': selected_student,
                'std_name': 'Alice Johnson',
                'std_class': '10A',
                'scores': [85, 90, 78, 92, 88]
            }

            # Sample subject names
            subj_names_useable = ['Math', 'Science', 'English', 'History', 'Art']

            # Sample top scores and average scores
            top_score = [95, 93, 88, 90, 85]
            avg_score = [80, 82, 75, 78, 80]

            pdfg.generate_report_card(
                sample_student['std_name'],
                "Mr. Anderson",          # Sample teacher name
                "parent@example.com",    # Sample parent contact
                "123-456-7890",          # Sample teacher contact
                sample_student['std_class'],
                selected_exam,
                sample_student['scores'],
                top_score,
                avg_score,
                sample_student['std_id'],
                subj_names_useable
            )
            messagebox.showinfo(title='Info', message='PDF for report card generated. Please check in the script directory.')
        else:
            messagebox.showwarning(title='WARNING', message='Please select a student and confirm your exam selection.')
    except IndexError:
        messagebox.showerror(title='ERROR', message='Please select a student to generate the report card.')
    except Exception as e:
        messagebox.showerror(title='ERROR', message=f'Unexpected error: {str(e)}')

selected_option = tkinter.StringVar()
class9var = tkinter.IntVar()
class10var = tkinter.IntVar()
class11var = tkinter.IntVar()
class12var = tkinter.IntVar()
selected_exam = None

# MAIN FRAME and widget setup
main_label = ttk.Label(common_options_frame, text='Generate Student Report Card', font=('Arial', '20'), justify="left", anchor="w")
select_exam_label = ttk.Label(common_options_frame, text='Select the examination you want to generate report card for:', font=('Arial', '15'), justify="left", anchor="w")

# Sample exams data
sample_exams = ['Midterm 2024', 'Final 2024', 'Quiz 1', 'Quiz 2']

# Treeview for examinations
exams_trv = ttk.Treeview(common_options_frame, selectmode='browse', columns=('Examinations',), height=5, show='headings')
exams_trv.column('Examinations', anchor='c', width=200)
exams_trv.heading('Examinations', text='Examinations')
for exam in sample_exams:
    exams_trv.insert("", 'end', iid=exam, text=exam, values=(exam,))

select_exam_button = ttk.Button(common_options_frame, text='Confirm Examination', command=select_exam_func)
option_label = ttk.Label(common_options_frame, text='Generate for:', font=('Arial', '15'), justify="left", anchor="w")
multiple_student_radiobutton = ttk.Radiobutton(common_options_frame, text='Multiple Students', value='multiple', variable=selected_option, command=update_window)
single_student_radiobutton = ttk.Radiobutton(common_options_frame, text='Single Student', value='single', variable=selected_option, command=update_window)

# Grid placement for MAIN FRAME
main_label.grid(row=0, column=0, sticky='W', pady=10, padx=10)
select_exam_label.grid(row=1, column=0, sticky='W', pady=10, padx=10)
exams_trv.grid(row=2, column=0, sticky='W', pady=10, padx=10)
select_exam_button.grid(row=3, column=0, sticky='W', pady=10, padx=10)
option_label.grid(row=4, column=0, sticky='W', pady=10, padx=10)
multiple_student_radiobutton.grid(row=5, column=0, sticky='W', pady=5, padx=20)
single_student_radiobutton.grid(row=6, column=0, sticky='W', pady=5, padx=20)

# MULTIPLE STUDENT FRAME and widget setup
grade_selection_label = ttk.Label(multiple_student_frame, text='Select classes to generate for:', font=('Arial', '15'), justify="left", anchor="w")
class9 = ttk.Checkbutton(multiple_student_frame, text='Class 9', onvalue=1, offvalue=0, variable=class9var)
class10 = ttk.Checkbutton(multiple_student_frame, text='Class 10', onvalue=1, offvalue=0, variable=class10var)
class11 = ttk.Checkbutton(multiple_student_frame, text='Class 11', onvalue=1, offvalue=0, variable=class11var)
class12 = ttk.Checkbutton(multiple_student_frame, text='Class 12', onvalue=1, offvalue=0, variable=class12var)
generate_multiple_rc = ttk.Button(multiple_student_frame, text='Generate', command=start_generating_multiple)
generating_text_multiple = ttk.Label(multiple_student_frame, text='Generating, please wait ....', font=('Arial', '15'), justify="left", anchor="w")

# Grid placement for MULTIPLE STUDENT FRAME
grade_selection_label.grid(row=0, column=0, sticky='W', pady=10, padx=10)
class9.grid(row=1, column=0, sticky='W', padx=10)
class10.grid(row=1, column=1, sticky='W', padx=10)
class11.grid(row=1, column=2, sticky='W', padx=10)
class12.grid(row=1, column=3, sticky='W', padx=10)
generate_multiple_rc.grid(row=2, column=0, sticky='W', pady=10, padx=10)
generating_text_multiple.grid(row=3, column=0, sticky='W', pady=10, padx=10)
generating_text_multiple.grid_forget()

# SINGLE STUDENT FRAME and widget setup
student_label = ttk.Label(single_student_frame, text='Select a student to generate report card for:', font=('Arial', '15'), justify="left", anchor="w")

# Sample students data
sample_students = [
    ('S001', 'Alice Johnson', '10A'),
    ('S002', 'Bob Smith', '10B'),
    ('S003', 'Charlie Lee', '11A'),
    # Add more sample students as needed
]

# Treeview for students
students_trv = ttk.Treeview(single_student_frame, selectmode='browse', columns=('Student ID', 'Name', 'Class'), height=5, show='headings')
for col in ['Student ID', 'Name', 'Class']:
    students_trv.column(col, anchor='c', width=150)
    students_trv.heading(col, text=col)
for student in sample_students:
    students_trv.insert("", 'end', iid=student[0], values=student)

generate_single_rc = ttk.Button(single_student_frame, text='Confirm Selection and Generate', command=generate_single_rc_func)

# Grid placement for SINGLE STUDENT FRAME
student_label.grid(row=0, column=0, sticky='W', pady=10, padx=10)
students_trv.grid(row=1, column=0, sticky='W', pady=10, padx=10)
generate_single_rc.grid(row=2, column=0, sticky='W', pady=10, padx=10)

# Initialize UI
show_common_opt()
sv_ttk.set_theme("dark")  # Ensure sv_ttk is installed
window.mainloop()
