#IMPORT STATEMENTS
import tkinter
from tkinter import ttk
import sv_ttk
from tkinter import messagebox

#WINDOW SETUP
window=tkinter.Tk()
window.title('Edit School Directory')
window.geometry('800x800')

#USER DEFINED FUNCTIONS
def onclick_teach_stu():
    opt1=teach_stu_var.get()
def onclick_add_remove():
    opt2=add_remove_var.get()

#WIDGET SETUP
teach_stu_var=tkinter.StringVar() #value will be stored in opt1
add_remove_var=tkinter.StringVar() #value will be stored in opt2'
opt1=''
opt2=''

main_label=ttk.Label(window, text='Edit School Directory - Add/Remove - Teachers/Students', font=('Arial', '20'))
teacher_student_label=ttk.Label(window, text='Would you like to Add/Remove a Teacher or Student ? ', font=('Arial', '13'), justify="left", anchor="w")
teacher_radiobutton=ttk.Radiobutton(window, text='Teacher', value='teacher_details', variable=teach_stu_var, command=onclick_teach_stu)
student_radiobutton=ttk.Radiobutton(window, text='Student', value='student_details', variable=teach_stu_var, command=onclick_teach_stu)
action_label=ttk.Label(window, text='What action would you like to perform ? ', font=('Arial', '13'), justify="left", anchor="w")
add_radiobutton=ttk.Radiobutton(window, text='Add', value='add', variable=add_remove_var, command=onclick_add_remove)
remove_radiobutton=ttk.Radiobutton(window, text='Remove', value='remove', variable=add_remove_var, command=onclick_add_remove)

main_label.grid(row=0, column=0, columnspan=1)
teacher_student_label.grid(row=1, column=0, pady=20, sticky='w')
teacher_radiobutton.grid(row=2,column=0, sticky='w')
student_radiobutton.grid(row=3, column=0, sticky='w')
action_label.grid(row=4, column=0, pady=20, sticky='w')
add_radiobutton.grid(row=5, column=0, sticky='w')
remove_radiobutton.grid(row=6, column=0, sticky='w')



sv_ttk.set_theme("dark")
window.mainloop()