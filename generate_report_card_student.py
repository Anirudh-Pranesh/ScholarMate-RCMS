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
import pdfgenerator as pdfg
import pickle

#window and frame set up
window=tkinter.Tk()
window.title('Generate report card')
window.geometry('1000x10000')
common_options_frame=ttk.Frame(window) # main frame to ask for which exam we are generating report for
multiple_student_frame=ttk.Frame(window) # frame if we are generating for multiple students. it asks for the classes we are geenrating for. so in the database we query for the list of students who belong to the selected class from the table for the exam containing students and their marks, and then generate their report cards using their marks
single_student_frame=ttk.Frame(window) # frame if we are generating only for a single student. we get the id of the student based on what the student in the treeview the user has selected. using that we query for their marks from the exam table we select and then generate the report card

#DB conn.
try:
    #db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_QI3ZZve-eNqFc8_bsLQ', database='scholarmate_db') #aiven conn.
    db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
except:
    messagebox.showerror(title="Error", message="No internet connection. Please connect to internet")
cur=db.cursor()

file=open('client_details.dat', 'rb')
dat=pickle.load(file)
student_id = dat[0][1]

def show_common_opt():
    common_options_frame.pack(fill="both", expand=True)

def select_exam_func():
    try:
        global selected_exam 
        selected_exam = exams_trv.selection()[0]# selected exam is declard none first, now we are obtaining the selection made by user and we are updated the selected_exam variable
        generate_single_rc_func()
    except:
        messagebox.showerror(title='ERROR', message='Examination not selected')

def generate_single_rc_func():
    try:
        selected_exam = exams_trv.selection()[0]
        if selected_exam != None:
            sqlstatement=f"SELECT * FROM {selected_exam} WHERE student_id={student_id};"
            cur.execute(sqlstatement)
            res=cur.fetchall()

            get_subj_names=f"DESC {selected_exam};"
            cur.execute(get_subj_names)
            subj_names_sql=cur.fetchall()

            get_names_contacts=f"SELECT teacher_name, teacher_contact, parent_contact FROM {selected_exam} JOIN teacher_details ON {selected_exam}.class = teacher_details.assigned_class JOIN student_details ON {selected_exam}.student_id = student_details.student_id WHERE {selected_exam}.student_id = {student_id};"
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
            messagebox.showwarning(title='WARNING', message='Please confirm you exam selection')
    except:
        messagebox.showerror(title='ERROR', message='Unexpected error, please check whether you have written this exam')

def on_closing():
    # Close the database connection
    if db.is_connected():
        db.close()
    # Destroy the root window
    window.destroy()

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

select_exam_button=ttk.Button(common_options_frame, text='Generate', command=select_exam_func)

#grid
main_label.grid(row=0, column=0,sticky = 'W', pady=10)
select_exam.grid(row=1, column=0,sticky = 'W', pady=10)
exams_trv.grid(row=2, column=0,sticky = 'W', pady=10)
select_exam_button.grid(row=3, column=0,sticky = 'W', pady=10)

show_common_opt()
sv_ttk.set_theme("dark")
window.update_idletasks()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()