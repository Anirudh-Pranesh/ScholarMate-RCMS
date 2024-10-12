'''To set up this functionality, we obtain the input from the user and destroy the main FRAME and show the respective input fields'''

# Import statements
import tkinter
from tkinter import ttk
import sv_ttk
from tkinter import messagebox
import mysql.connector
from tkinter import messagebox
# endregion

# Window and frame setup
window=tkinter.Tk()
window.title('Edit School Directory')
window.geometry('1000x900')
#These four are the windows where i am displaying the option to perform action
main_menu_frame = ttk.Frame(window)
teacher_delete_frame = ttk.Frame(window)
teacher_add_frame = ttk.Frame(window)
student_add_frame = ttk.Frame(window)
student_delete_frame = ttk.Frame(window)
# endregion

# USER DEFINED FUNCTIONS 
def show_main_menu(): #function displays the main menu
    """Show the main menu and hide other frames."""
    hide_frames()
    main_menu_frame.pack(fill="both", expand=True)

def return_main_menu():#USE TO RETURN TO MAIN MENU FROM ANOTHER FRAME
    """Show the main menu and hide other frames."""
    hide_frames()
    teach_stu_var.set(None)
    add_remove_var.set(None)
    main_menu_frame.pack(fill="both", expand=True)

def teacher_delete():#function to move to teacher delete page
    """Show Page One and hide other frames."""
    hide_frames()
    teacher_delete_frame.pack(fill="both", expand=True)

def teacher_add():#function to move to teacher add page
    """Show Page Two and hide other frames."""
    hide_frames()
    teacher_add_frame.pack(fill="both", expand=True)

def student_delete():#function to move to student delete page
    """Show Page Two and hide other frames."""
    hide_frames()
    student_delete_frame.pack(fill="both", expand=True)

def student_add():#function to move to student add page
    """Show Page Two and hide other frames."""
    hide_frames()
    student_add_frame.pack(fill="both", expand=True)

def hide_frames():
    """Hide all frames."""
    main_menu_frame.pack_forget()
    teacher_add_frame.pack_forget()
    teacher_delete_frame.pack_forget()
    student_delete_frame.pack_forget()
    student_add_frame.pack_forget()

def execute_selection_delete_teacher(): #deletes teacher by sending a query
    #RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
    db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
    #db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
    cur=db.cursor()
    selected_item = trv.selection()  
    if selected_item:
        item_data = trv.item(selected_item)  
        values = item_data['values']
        id=values[0]
        query=f"DELETE FROM teacher_details WHERE teacher_id={id};"
        cur.execute(query)
        db.commit()
        db.close()
        refresh_teacher_list()
        return_main_menu()
        messagebox.showinfo(title='Teacher succssfully removed', message=values[1]+', (teacher_id = '+str(values[0])+') has been removed')
    else:
        messagebox.showwarning(title='WARNING', message='Select a teacher')

def execute_selection_delete_student(): # deletes student by sending a query
    #RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
    db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
    #db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
    cur=db.cursor()
    selected_item = student_trv.selection()  
    if selected_item:
        item_data = student_trv.item(selected_item)  
        values = item_data['values']
        id=values[0]
        print(item_data)
        print(values)
        query=f"DELETE FROM student_details WHERE student_id={id};"
        cur.execute(query)
        db.commit()
        db.close()
        refresh_student_list()
        return_main_menu()
        messagebox.showinfo(title='Student succssfully removed', message=values[1]+', (student_id = '+str(values[0])+') has been removed')
    else:
        messagebox.showwarning(title='WARNING', message='Select a student')

def execute_add_teacher(): #adds teacher by sending a query
    #RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
    db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
    #db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
    cur=db.cursor()
    name=teacher_name_entry.get()
    contact=teacher_contact_entry.get()
    asgnclass=asgn_class_entry.get()
    if name=='' or contact=='' or asgnclass=='':
        messagebox.showwarning(title='WARNING', message='Enter a valid input')
    else:
        try:
            query=f"INSERT INTO teacher_details(teacher_name, teacher_contact, assigned_class) VALUES('{name}', '{contact}', '{asgnclass}');"
            cur.execute(query)
            db.commit()
            db.close()
            #RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
            newdb=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
            #newdb=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
            newcur=newdb.cursor()
            usnamepwd=f"SELECT username, passkey FROM credentials where teacher_id = (SELECT teacher_id FROM teacher_details where teacher_name='{name}' AND teacher_contact='{contact}' AND assigned_class='{asgnclass}');'"
            newcur.execute(usnamepwd)
            res=newcur.fetchall()
            newdb.close()
            username=res[0][0]
            pwd=res[0][1]
            refresh_teacher_list()
            return_main_menu()
            messagebox.showinfo(title="Teacher successfully added", message=name + ' is now a teacher'+f"Username = '{username}', Password = '{pwd}'")
        except:
            messagebox.showerror(title='UNEXPECTED ERROR', message='Unexpected error encountered. Please check details inputted')


def execute_add_student(): # adds studsnt by sending a query
    #RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
    db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
    #db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
    cur=db.cursor()
    name=student_name_entry.get()
    contact=parent_contact_entry.get()
    asgnclass=student_class_entry.get()
    if name=='' or contact=='' or asgnclass=='':
        messagebox.showwarning(title='WARNING', message='Enter a valid input')
    else:
        try:
            query=f"INSERT INTO student_details(student_name, class, parent_contact, class_teacher_id) VALUES('{name}', '{asgnclass}', '{contact}', (SELECT teacher_id FROM teacher_details WHERE assigned_class='{asgnclass}'));"
            cur.execute(query)
            db.commit()
            db.close()
            #RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
            newdb=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
            #newdb=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
            newcur=newdb.cursor()
            usnamepwd=f"SELECT username, passkey FROM credentials where student_id = (SELECT student_id FROM student_details where student_name='{name}' AND parent_contact='{contact}' AND class='{asgnclass}');'"
            newcur.execute(usnamepwd)
            res=newcur.fetchall()
            newdb.close()
            username=res[0][0]
            pwd=res[0][1]
            refresh_student_list()
            return_main_menu()
            messagebox.showinfo(title='Student successfully added', message=name + ' is now a student'+f"Username = '{username}', Password = '{pwd}'")
        except:
            messagebox.showerror(title='UNEXPECTED ERROR', message='Unexpected error encountered. Please check details inputted')

def refresh_teacher_list(): # bug : after adding a teacher, the table showed in teacher delete is not refreshing, this function achieves it
    #RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
    db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
    #db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
    cur = db.cursor()
    remove_t_q = "SELECT * FROM teacher_details ORDER BY teacher_name"
    cur.execute(remove_t_q)
    res = cur.fetchall()
    cur.close()
    db.close()

    # Clear the existing data in the Treeview
    trv.delete(*trv.get_children())

    # Insert updated data
    for row in res:
        trv.insert("", 'end', iid=row[0], text=row[0], values=list(row))

def refresh_student_list(): # same bug here, except for student delete frame
    #RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
    db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
    #db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
    cur = db.cursor()
    remove_s_q = "SELECT * FROM student_details ORDER BY student_name"
    cur.execute(remove_s_q)
    res = cur.fetchall()
    cur.close()
    db.close()

    # Clear the existing data in the Treeview
    student_trv.delete(*student_trv.get_children())

    # Insert updated data
    for row in res:
        student_trv.insert("", 'end', iid=row[0], text=row[0], values=list(row))

#THIS FUNCTION KEEPS UPDATING VALUE OF OPT1 AND 2 AND RESPECITVELY CALLS THE REQUIRED FRAME
def update_frame():
    """Check the selected options and show the respective frame."""
    opt1 = teach_stu_var.get()
    opt2 = add_remove_var.get()

    hide_frames()
    if opt1 == 'teacher_details' and opt2 == 'add':
        teacher_add()
    elif opt1 == 'teacher_details' and opt2 == 'remove':
        teacher_delete()
    elif opt1 == 'student_details' and opt2 == 'add':
        student_add()
    elif opt1 == 'student_details' and opt2 == 'remove':
        student_delete()
    else:
        show_main_menu()
# endregion

# Frame setup and design

teach_stu_var=tkinter.StringVar() #value will be stored in opt1
add_remove_var=tkinter.StringVar() #value will be stored in opt2

# MAIN MENU CONTENT
'''##### MAIN MENU CONTENT #####'''

main_label=ttk.Label(main_menu_frame, text='Edit School Directory - Add/Remove - Teachers/Students', font=('Arial', '20'))
teacher_student_label=ttk.Label(main_menu_frame, text='Would you like to Add/Remove a Teacher or Student ? ', font=('Arial', '13'), justify="left")
teacher_radiobutton=ttk.Radiobutton(main_menu_frame, text='Teacher', value='teacher_details', variable=teach_stu_var, command=update_frame)
student_radiobutton=ttk.Radiobutton(main_menu_frame, text='Student', value='student_details', variable=teach_stu_var, command=update_frame)
action_label=ttk.Label(main_menu_frame, text='What action would you like to perform ? ', font=('Arial', '13'), justify="left", anchor="w")
add_radiobutton=ttk.Radiobutton(main_menu_frame, text='Add', value='add', variable=add_remove_var, command=update_frame)
remove_radiobutton=ttk.Radiobutton(main_menu_frame, text='Remove', value='remove', variable=add_remove_var, command=update_frame)# on click update frame is called, ir dynamically checks the users input

main_label.place(relx=0.5, rely=0.01, anchor='n')
teacher_student_label.place(relx=0.5, rely=0.07, anchor='center')
teacher_radiobutton.place(relx=0.5, rely=0.1, anchor='center')
student_radiobutton.place(relx=0.5, rely=0.135, anchor='center')
action_label.place(relx=0.5, rely=0.18, anchor='center')
add_radiobutton.place(relx=0.5, rely=0.23, anchor='center')
remove_radiobutton.place(relx=0.5, rely=0.27, anchor='center')
# endregion

# REMOVE TEACHER CONTENT
'''##### REMOVE TEACHER CONTENT #####'''

#RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
#db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
cur=db.cursor()
remove_t_q="SELECT * FROM teacher_details ORDER BY teacher_name"
cur.execute(remove_t_q)
res=cur.fetchall()
db.close()
l1=[i[0] for i in cur.description]#column headers


remove_teacher_main_label=ttk.Label(teacher_delete_frame, text='Select teacher you would like to remove : ', font=('Arial', '20'))
trv=ttk.Treeview(teacher_delete_frame, selectmode='browse', columns=l1, height=10, show='headings')
selection_button=ttk.Button(teacher_delete_frame, text='Confirm Selection ? ', command=execute_selection_delete_teacher)
remove_teacher_go_home_button=ttk.Button(teacher_delete_frame, text='Go back to desicion page', command=return_main_menu)

remove_teacher_main_label.place(relx=0.5, rely=0.01, anchor='n')
trv.place(relx=0.5, rely=0.06, anchor='n')
selection_button.place(relx=0.4, rely=0.45, anchor='n')
remove_teacher_go_home_button.place(relx=0.6, rely=0.45, anchor='n')

#filling the table
for i in l1:    
    trv.column(i, anchor='c', width=200)
    trv.heading(i, text=i)
for row in res:
    trv.insert("", 'end', iid=row[0], text=row[0], values=list(row))
# endregion

# REMOVE STUDENT CONTENT


'''##### REMOVE STUDENT CONTENT #####'''

#RESTRICT FOR AIVEN CONN. ------> TRIGGERS NOT SETUP
db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
#db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
cur=db.cursor()
remove_s_q="SELECT * FROM student_details ORDER BY student_name"
cur.execute(remove_s_q)
res=cur.fetchall()
db.close()
l1=[i[0] for i in cur.description]#column headers

student_main_label=ttk.Label(student_delete_frame, text='Select student you would like to remove : ', font=('Arial', '20'))
student_trv=ttk.Treeview(student_delete_frame, selectmode='browse', columns=l1, height=10, show='headings')
student_selection_button=ttk.Button(student_delete_frame, text='Confirm Selection ? ', command=execute_selection_delete_student)
student_remove_go_home_button=ttk.Button(student_delete_frame, text='Go back to desicion page', command=return_main_menu)

student_main_label.place(relx=0.5, rely=0.01, anchor='n')
student_trv.place(relx=0.5, rely=0.06, anchor='n')
student_selection_button.place(relx=0.4, rely=0.45, anchor='n')
student_remove_go_home_button.place(relx=0.6, rely=0.45, anchor='n')

#filling the table
for i in l1:
    student_trv.column(i, anchor='c', width=200)
    student_trv.heading(i, text=i)
for row in res:
    student_trv.insert("", 'end', iid=row[0], text=row[0], values=list(row))

# endregion

# ADD TEACHER CONTENT 
'''##### ADD TEACHER CONTENT #####'''

add_teacher_main_label=ttk.Label(teacher_add_frame, text='Enter details of new teacher : ', font=('Arial', '20'))
teacher_name_label=ttk.Label(teacher_add_frame, text='Teacher name : ', font=('Arial', 15))
teacher_contact_label=ttk.Label(teacher_add_frame, text='Teacher contact details : ', font=('Arial', '15'))
asgn_class_label=ttk.Label(teacher_add_frame, text='Class assigned : ', font=('Arial', '15'))
teacher_name_entry = ttk.Entry(teacher_add_frame)
teacher_contact_entry = ttk.Entry(teacher_add_frame)
asgn_class_entry = ttk.Entry(teacher_add_frame)
teacher_add_button=ttk.Button(teacher_add_frame, text='Add teacher', command=execute_add_teacher)
add_teacher_go_home_button=ttk.Button(teacher_add_frame, text='Go back to desicion page', command=return_main_menu)

add_teacher_main_label.place(relx=0.5, rely=0.01, anchor='n')
teacher_name_label.place(relx=0.4, rely=0.1, anchor='n')
teacher_name_entry.place(relx=0.6, rely=0.1, anchor='n')
teacher_contact_label.place(relx=0.4, rely=0.2, anchor='n')
teacher_contact_entry.place(relx=0.6, rely=0.2, anchor='n')
asgn_class_label.place(relx=0.4, rely=0.3, anchor='n')
asgn_class_entry.place(relx=0.6, rely=0.3, anchor='n')
teacher_add_button.place(relx=0.4, rely=0.45, anchor='n')
add_teacher_go_home_button.place(relx=0.6, rely=0.45, anchor='n')
# endregion

# ADD STUDENT CONTENT
'''##### ADD STUDENT CONTENT #####'''

student_add_main_label=ttk.Label(student_add_frame, text='Enter details of new student : ', font=('Arial', '20'))
student_name_label=ttk.Label(student_add_frame, text='Student name : ', font=('Arial', 15))
parent_contact_label=ttk.Label(student_add_frame, text='Parent contact details : ', font=('Arial', '15'))
class_label=ttk.Label(student_add_frame, text='Class assigned : ', font=('Arial', '15'))
student_name_entry = ttk.Entry(student_add_frame)
parent_contact_entry = ttk.Entry(student_add_frame)
student_class_entry = ttk.Entry(student_add_frame)
student_add_button=ttk.Button(student_add_frame, text='Add student', command=execute_add_student)
go_home_button=ttk.Button(student_add_frame, text='Go back to desicion page', command=return_main_menu)

student_add_main_label.place(relx=0.5, rely=0.01, anchor='n')
student_name_label.place(relx=0.4, rely=0.1, anchor='n')
student_name_entry.place(relx=0.6, rely=0.1, anchor='n')
parent_contact_label.place(relx=0.4, rely=0.2, anchor='n')
parent_contact_entry.place(relx=0.6, rely=0.2, anchor='n')
class_label.place(relx=0.4, rely=0.3, anchor='n')
student_class_entry.place(relx=0.6, rely=0.3, anchor='n')
student_add_button.place(relx=0.4, rely=0.45, anchor='n')
go_home_button.place(relx=0.6, rely=0.45, anchor='n')

# endregion

# endregion

# Main function calls and theme setup
show_main_menu()
sv_ttk.set_theme("dark")
window.update_idletasks()
window.mainloop()
# endregion