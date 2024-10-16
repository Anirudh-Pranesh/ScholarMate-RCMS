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
#!!!!!!!!!!!!!!!PLEASE REFERENCE https://drive.google.com/file/d/1QQCceEJRKtQzwJt2dB5-S4vGCiToQtWy/view?usp=sharing FOR TABLE NAMES, COLUMNS NAMES, ETC. exam-sheet-1 is just a sample table the admin will create for the exam showing how the data will be in it once such an exam table is created, 
#so that teachers can enter the student marks in that table. we have not programmed the part where teachers can enter the student marks yet, but we are obtaining the table name as i said above. the table for an exam can be 
#created by an admin.


#import statemnts
import tkinter
from tkinter import ttk
import sv_ttk
from tkinter import messagebox
import mysql.connector
from tkinter import messagebox
import time
import threading
import pdfgenerator as pdfg

#window and frame set up
window=tkinter.Tk()
window.title('Generate report card')
window.geometry('1000x10000')
common_options_frame=ttk.Frame(window) # main frame to ask for which exam we are generating report for
multiple_student_frame=ttk.Frame(window) # frame if we are generating for multiple students. it asks for the classes we are geenrating for. so in the database we query for the list of students who belong to the selected class from the table for the exam containing students and their marks, and then generate their report cards using their marks
single_student_frame=ttk.Frame(window) # frame if we are generating only for a single student. we get the id of the student based on what the student in the treeview the user has selected. using that we query for their marks from the exam table we select and then generate the report card

#DB conn.
db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
#db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
cur=db.cursor()

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
    generating_text_multiple.grid(row=2, column=0, sticky='W', pady=10)
    time.sleep(0.5)
    threading.Thread(target=generate_multiple_rc_func).start()

def generate_multiple_rc_func():
    # in here, we can get the classes selected by using class9var, class10var, class11var, class12var
    try:
        if (class9var.get() == 1 or class10var.get() == 1 or class11var.get() == 1 or class12var.get() == 1) and selected_exam != None : 
            permitted_classes_get=f"SELECT DISTINCT LEFT(class, LENGTH(class) - 1) FROM {selected_exam};"
            cur.execute(permitted_classes_get)
            res=cur.fetchall()
            get_subj_names=f"DESC {selected_exam};"
            cur.execute(get_subj_names)
            subj_names_sql=cur.fetchall()
            count=0
            subj_names_useable=[]
            for i in subj_names_sql:
                if count<=2:
                    count+=1
                else:
                    subj_names_useable.append(i[0])
            permitted_classes=[i[0] for i in res]
            available_classes={'9':class9var.get(),'10':class10var.get(), '11':class11var.get(), '12':class12var.get()}
            selected_classes=[]
            error_list=[]
            for i in available_classes:
                if available_classes[i] == 1 and i in permitted_classes:
                    selected_classes.append(i)
                elif available_classes[i] == 1 and i not in permitted_classes:
                    error_list.append(i)
            if error_list != [] and selected_classes != []:
                messagebox.showinfo(title='Info', message='This examination was not conducted for classes '+str(error_list)+'. Report card now being generated for '+str(selected_classes))
            elif error_list!=[] and selected_classes == []:
                messagebox.showwarning(title='Select appropriate class', message='This examination was not conducted for classes '+str(error_list))
        else:
            messagebox.showwarning(title='WARNING', message='A class must be selected/confirm your exam selection')
        if selected_classes !=[]:
            for i in selected_classes:
                sqlstatement=f"SELECT * FROM {selected_exam} WHERE class LIKE '{i}%';"
                cur.execute(sqlstatement)
                res=cur.fetchall()
                top_score=[]
                avg_score=[]
                for k in subj_names_useable:
                    statement_top=f"SELECT MAX({k}) FROM {selected_exam} WHERE class LIKE '{i}%'"
                    statement_avg=f"SELECT ROUND(AVG({k}), 1) FROM {selected_exam} WHERE class LIKE '{i}%'"
                    cur.execute(statement_top)
                    top_score.append(cur.fetchall()[0][0])
                    cur.execute(statement_avg)
                    avg_score.append(cur.fetchall()[0][0])
                for j in res:
                    std_id=j[0] #pdf function params
                    std_name=j[1] #pdf function params
                    std_class=j[2] #pdf function params
                    score_list=[j[3], j[4], j[5], j[6], j[7]]
                    get_names_contacts=f"SELECT teacher_name, teacher_contact, parent_contact FROM {selected_exam} JOIN teacher_details ON {selected_exam}.class = teacher_details.assigned_class JOIN student_details ON {selected_exam}.student_id = student_details.student_id WHERE {selected_exam}.student_id = {std_id};"
                    cur.execute(get_names_contacts)
                    contact_name_details=cur.fetchall()
                    contact_name_details=contact_name_details[0]
                    teacher_name, teacher_contact, parent_contact = contact_name_details # pdf function param
                    pdfg.generate_report_card(std_name, teacher_name, parent_contact, teacher_contact, std_class, selected_exam, score_list, top_score, avg_score, std_id, subj_names_useable)
            generating_text_multiple.grid_forget()
            messagebox.showinfo(title='Info', message='PDFs for report cards generated. Please check in downloads folder')
    except:
        messagebox.showerror(title='ERROR', message='Unexpected error encountered. Please check whether the pdf already exists')

def select_exam_func():
    global selected_exam 
    try:
        selected_exam = exams_trv.selection()[0] # selected exam is declard none first, now we are obtaining the selection made by user and we are updated the selected_exam variable
    except:
        messagebox.showerror(title='ERROR', message='Examination not selected')
    messagebox.showinfo(title='Examination selected', message=selected_exam+' has been selected')

def generate_single_rc_func():
    try:
        selected_student=students_trv.selection()[0]
        if selected_student and selected_exam != None:
            values = selected_student

            sqlstatement=f"SELECT * FROM {selected_exam} WHERE student_id={values};"
            cur.execute(sqlstatement)
            res=cur.fetchall()

            get_subj_names=f"DESC {selected_exam};"
            cur.execute(get_subj_names)
            subj_names_sql=cur.fetchall()

            get_names_contacts=f"SELECT teacher_name, teacher_contact, parent_contact FROM {selected_exam} JOIN teacher_details ON {selected_exam}.class = teacher_details.assigned_class JOIN student_details ON {selected_exam}.student_id = student_details.student_id WHERE {selected_exam}.student_id = {res[0][0]};"
            cur.execute(get_names_contacts)
            contact_name_details=cur.fetchall()
            contact_name_details=contact_name_details[0]
            subj_names_useable=[]
            count=0
            for i in subj_names_sql:
                if count<=2:
                    count+=1
                else:
                    subj_names_useable.append(i[0])
            teacher_name, teacher_contact, parent_contact = contact_name_details #pdf function params
            std_id=res[0][0] #pdf function params
            std_name=res[0][1] #pdf function params
            std_class=res[0][2] #pdf function params
            score_list=[res[0][3], res[0][4], res[0][5], res[0][6], res[0][7]] # pdf function param
            top_score=[]
            avg_score=[]
            for i in subj_names_useable:
                statement=f"SELECT MAX({i}), ROUND(AVG({i}), 1) FROM {selected_exam} WHERE class LIKE CONCAT(LEFT('{std_class}', LENGTH('{std_class}')-1), '%');"
                cur.execute(statement)
                dat=cur.fetchall()
                top_score.append(dat[0][0])
                avg_score.append(dat[0][1])
            pdfg.generate_report_card(std_name, teacher_name, parent_contact, teacher_contact, std_class, selected_exam, score_list, top_score, avg_score, std_id, subj_names_useable)
            messagebox.showinfo(title='Info', message='PDF for report card generated. Please check in downloads folder')
        else:
            messagebox.showwarning(title='WARNING', message='Please select a student/confirm you exam selection')
    except:
        messagebox.showerror(title='ERROR', message='Unexpected error, please check whether this student has written this exam')

def on_closing():
    # Close the database connection
    if db.is_connected():
        db.close()
    # Destroy the root window
    window.destroy()

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
show_exams="SHOW TABLES;"
cur.execute(show_exams)
res=cur.fetchall()
res=list(filter(lambda x: x not in [('credentials',), ('student_details',), ('teacher_details',)], res)) # show tables gives all tables, we dont want to show those 3 tables because its not an examination, its for the backend reference
exams_trv=ttk.Treeview(common_options_frame, selectmode='browse', columns='Examinations', height=5, show='headings')
exams_trv.column('Examinations', anchor='c', width=200)
exams_trv.heading('Examinations', text='Examinations')
for row in res:
    exams_trv.insert("", 'end', iid=row[0], text=row[0], values=list(row))

select_exam_button=ttk.Button(common_options_frame, text='Confirm examination ? ', command=select_exam_func)
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
generate_multiple_rc=ttk.Button(multiple_student_frame, text='Generate', command=start_generating_multiple)
generating_text_multiple=ttk.Label(multiple_student_frame, text='Generating, please wait ....', font=('Arial', '15'), justify="left", anchor="w")

#grid
grade_selection_label.grid(row=0, column=0,sticky = 'W')
class9.grid(row=0, column=1,sticky = 'W')
class10.grid(row=0, column=2,sticky = 'W')
class11.grid(row=0, column=3,sticky = 'W')
class12.grid(row=0, column=4,sticky = 'W')
generate_multiple_rc.grid(row=1, column=0,sticky = 'W', pady=10)
generating_text_multiple.grid(row=2, column=0, sticky='W', pady=10)
generating_text_multiple.grid_forget()


#SINGLE STUDENT FRAME, and widget set-up
student_label=ttk.Label(single_student_frame, text='Selected student to generate report card for :  ', font=('Arial', '15'), justify="left", anchor="w")

#treeview
show_students="SELECT * FROM student_details ORDER BY student_name"
cur.execute(show_students)
res=cur.fetchall()
l1=[i[0] for i in cur.description]#column headers
students_trv=ttk.Treeview(single_student_frame, selectmode='browse', columns=l1, height=5, show='headings')
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
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()