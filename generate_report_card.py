#generate_report_card.py
#in this porgram, we are asking for the user to select the examination we are generating the report card for. using treeview we are showing all the exam tables being stored in the database
#the user then selects an exam from the table and confirms the exam. we then store what exam they selected in a varaible selected_exam. we set the examination selected in a function select_exam_func()
#by declaring the variable as global. We will use this information later. Now the user selects if we are egenrating for a single student or multiple students. if we are generating for multiple students 
#then we know the table name(exam name)(selected_exam) and directly query all the students who belong in that grade from that table and we will get a list of students and their marks. 
#now using this information we go row by row in the list and generate the report card for them in a pdf format. we will show other statistics like average marks, top mark in the class, grade (A,B,C,D,F)
# graph showing their performance vs class average performance. the class aeverage performace can again be queried from the table.
#if we are generating only for a single student, then the user will select a student, we gather their student id, refer to the examination table, gather their marks, top marks, grade, and average perofmrance 
#of class again and generate the report card again.
#Don't worry about the UI or anything else in this script, its only setting up the UI, we only need to write the functions, SQL statements and actually generate a pdf. all you NEED TO KNOW is to extract selected row from treeview do this : 
'''
item_data = student_trv.item(selected_item)       #student_trv is the treeview object that we want to get the selected data from 
values = item_data['values']                      # this will store exactly how MySQL stored it, in order. so for example if student_trv contained data from student_details, then values[0] will be student_id because the first column in student_details is student_id
'''
#!!!!!!!!!!!!!!!PLEASE REFERNCE https://drive.google.com/file/d/1QQCceEJRKtQzwJt2dB5-S4vGCiToQtWy/view?usp=sharing FOR TABLE NAMES, COLUMNS NAMES, ETC. exam-sheet-1 is just a sample table the admin will create for the exam showing how the data will be in it once such an exam table is created, 
#so that teachers can enter the student marks in that table. we have not programmed the part where teachers can enter the student marks yet, but we are obtaining the table name as i said above. the table for an exam can be 
#created by an admin.


#import statemnts
import tkinter
from tkinter import ttk
import sv_ttk
from tkinter import messagebox
import mysql.connector
from tkinter import messagebox

#window and frame set up
window=tkinter.Tk()
window.title('Generate report card')
window.geometry('800x700')
common_options_frame=ttk.Frame(window) # main frame to ask for which exam we are generating report for
multiple_student_frame=ttk.Frame(window) # frame if we are generating for multiple students. it asks for the classes we are geenrating for. so in the database we query for the list of students who belong to the selected class from the table for the exam containing students and their marks, and then generate their report cards using their marks
single_student_frame=ttk.Frame(window) # frame if we are generating only for a single student. we get the id of the student based on what the student in the treeview the user has selected. using that we query for their marks from the exam table we select and then generate the report card

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

#NEED TO PROGRAM THESE FUNCTIONS 

def generate_multiple_rc_func():
    a=1 # write function here, ove written a=1 here because i cant leave it empty with only a comment, python gives an error
    # in here, we can get the classes selected by using class9var, class10var, class11var, class12var

def select_exam_func():
    global selected_exam 
    selected_exam = exams_trv.selection() # selected exam is declard none first, now we are obtaining the selection made by user and we are updated the selected_exam variable

def generate_single_rc_func():
    selected_student=students_trv.selection()
    if selected_student:
        a=1 # write function here, ove written a=1 here because i cant leave it empty with only a comment, python gives an error
    else:
        messagebox.showwarning(title='WARNING', message='Select a student')


selected_option=tkinter.StringVar()
class9var = tkinter.IntVar()
class10var = tkinter.IntVar()
class11var = tkinter.IntVar()
class12var = tkinter.IntVar()
selected_exam = None

#MAIN FRAME, and widget setup
main_label=ttk.Label(common_options_frame, text='Generate student report card', font=('Arial', '20'), justify="left", anchor="w")
select_exam=ttk.Label(common_options_frame, text='Select the examination you want to generate report card for : ', font=('Arial', '15'), justify="left", anchor="w")

#treeview
db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db')
cur=db.cursor()
show_exams="SHOW TABLES;"
cur.execute(show_exams)
res=cur.fetchall()
db.close()
res=list(filter(lambda x: x not in [('credentials',), ('student_details',), ('teacher_details',)], res)) # show tables gives all tables, we dont want to show those 3 tables because its not an examination, its for the backend reference
exams_trv=ttk.Treeview(common_options_frame, selectmode='browse', columns='Examinations', height=5, show='headings')
exams_trv.column('Examinations', anchor='c', width=200)
exams_trv.heading('Examinations', text='Examinations')
for row in res:
    exams_trv.insert("", 'end', iid=row[0], text=row[0], values=list(row))

select_exam_button=ttk.Button(common_options_frame, text='Confirm Selection ? ', command=select_exam_func)
option_label=ttk.Label(common_options_frame, text='Generate for : ', font=('Arial', '15'), justify="left", anchor="w")
multiple_student_radiobutton=ttk.Radiobutton(common_options_frame, text='Multiple students', value='multiple', variable=selected_option, command=update_window)
single_student_radiobutton=ttk.Radiobutton(common_options_frame, text='Single student', value='single', variable=selected_option, command=update_window)

#grid
main_label.grid(row=0, column=0,sticky = 'W', pady=10)
select_exam.grid(row=1, column=0,sticky = 'W', pady=10)
exams_trv.grid(row=2, column=0,sticky = 'W', pady=10)
select_exam_button.grid(row=3, column=0,sticky = 'W', pady=10)
option_label.grid(row=4, column=0,sticky = 'W', pady=10)
multiple_student_radiobutton.grid(row=5, column=0,sticky = 'W', pady=10)
single_student_radiobutton.grid(row=6, column=0,sticky = 'W', pady=10)


#MULTIPLE STUDENT FRAME, and widget setup
grade_selection_label=ttk.Label(multiple_student_frame, text='Select classes to generate for : ', font=('Arial', '15'), justify="left", anchor="w")
class9 = ttk.Checkbutton(multiple_student_frame, text='Class 9', onvalue=1, offvalue=0, variable=class9var)
class10 = ttk.Checkbutton(multiple_student_frame, text='Class 10', onvalue=1, offvalue=0, variable=class10var)
class11 = ttk.Checkbutton(multiple_student_frame, text='Class 11', onvalue=1, offvalue=0, variable=class11var)
class12 = ttk.Checkbutton(multiple_student_frame, text='Class 12', onvalue=1, offvalue=0, variable=class12var)
generate_multiple_rc=ttk.Button(multiple_student_frame, text='Generate', command=generate_multiple_rc_func)

#grid
grade_selection_label.grid(row=0, column=0,sticky = 'W')
class9.grid(row=0, column=1,sticky = 'W')
class10.grid(row=0, column=2,sticky = 'W')
class11.grid(row=0, column=3,sticky = 'W')
class12.grid(row=0, column=4,sticky = 'W')
generate_multiple_rc.grid(row=1, column=0,sticky = 'W', pady=10)


#SINGLE STUDENT FRAME, and widget set-up
student_label=ttk.Label(single_student_frame, text='Selected student to generate report card for :  ', font=('Arial', '15'), justify="left", anchor="w")

#treeview
db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db')
cur=db.cursor()
show_students="SELECT * FROM student_details ORDER BY student_name"
cur.execute(show_students)
res=cur.fetchall()
db.close()
l1=[i[0] for i in cur.description]#column headers
students_trv=ttk.Treeview(single_student_frame, selectmode='browse', columns=l1, height=10, show='headings')
for i in l1:    
    students_trv.column(i, anchor='c', width=200)
    students_trv.heading(i, text=i)
for row in res:
    students_trv.insert("", 'end', iid=row[0], text=row[0], values=list(row))

generate_single_rc=ttk.Button(single_student_frame, text='Confirm selection and genrate', command=generate_single_rc_func)


student_label.grid(row=0, column=0,sticky = 'W')
students_trv.grid(row=1, column=0,sticky = 'W', pady=10)
generate_single_rc.grid(row=3, column=0,sticky = 'W', pady=10)



show_common_opt()
sv_ttk.set_theme("dark")
window.update_idletasks()
window.mainloop()