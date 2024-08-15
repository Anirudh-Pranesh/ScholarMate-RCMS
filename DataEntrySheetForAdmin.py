import tkinter as tk
from tkinter import ttk
import sv_ttk
import mysql.connector
def tablecreation():
    vighneshdb=mysql.connector.connect(host='localhost',user='root',password='whiskeytangofoxtrot',database='RCMS')
    cursor1=vighneshdb.cursor()
    sqlstatement='create table'+examname+'(student_id text,name text,class text,'+sub1 +'text,'+sub2 +'text,'+sub3+'text,'+sub4 +'text,'+sub5+'text )'
    cursor1.execute(sqlstatement)
    vighneshdb.commit()
    vighneshdb.close()
#import pillow
root=tk.Tk()
#Data Entry Window
root.geometry('600x400')
root.title('Data Entry Sheet For Admin')
title_label=ttk.Label(root,text='Data Entry Sheet for Admin',font=('Arial',28,'bold'))
#Data Entry Sheet
#Entry Fields and Text Labels
exam_label=ttk.Label(root,text='1. Enter exam name here :',font=('calibre',14,'bold'))
exam_entry=ttk.Entry(root)
subject1_label=ttk.Label(root,text='2a. Enter subject 1 here :',font=('calibre',14,'bold'))
subject1_entry=ttk.Entry(root)
subject2_label=ttk.Label(root,text='2b. Enter subject 2 here :',font=('calibre',14,'bold'))
subject2_entry=ttk.Entry(root)
subject3_label=ttk.Label(root,text='2c. Enter subject 3 here :',font=('calibre',14,'bold'))
subject3_entry=ttk.Entry(root)
subject4_label=ttk.Label(root,text='2d. Enter subject 4 here :',font=('calibre',14,'bold'))
subject4_entry=ttk.Entry(root)
subject5_label=ttk.Label(root,text='2e. Enter subject 5 here :',font=('calibre',14,'bold'))
subject5_entry=ttk.Entry(root)
class_label=ttk.Label(root,text='''        3. Click on the classes for which
             the exam was held for :''',font=('calibre',14,'bold'))
#Checkboxes for the classes
class9=ttk.Checkbutton(root,text='Class 9',onvalue=1,offvalue=0,variable=class9var)
class10=ttk.Checkbutton(root,text='Class 10',onvalue=1,offvalue=0,variable=class10var)
class11=ttk.Checkbutton(root,text='Class 11',onvalue=1,offvalue=0,variable=class11var)
class12=ttk.Checkbutton(root,text='Class 12',onvalue=1,offvalue=0,variable=class12var)
class9var=ttk.IntVar()
class10var=ttk.IntVar()
class11var=ttk.IntVar()
class12var=ttk.IntVar()
#Input Received
examname=exam_entry.get()
sub1=subject1_entry.get()
sub2=subject2_entry.get()
sub3=subject3_entry.get()
sub4=subject4_entry.get()
sub5=subject5_entry.get()
class9input=class9var.get()
class10input=class9var.get()
class11input=class9var.get()
class12input=class9var.get()
#Button to create table
button1=ttk.Button(root,text='Click   here   to   create   a   table',command=tablecreation)
#Empty Fields
emptylabel1=ttk.Label(root,text='')
emptylabel2=ttk.Label(root,text='')
emptylabel3=ttk.Label(root,text='                                                                                                                               ')
emptylabel4=ttk.Label(root,text='')
emptylabel5=ttk.Label(root,text='')
emptylabel6=ttk.Label(root,text='')
#Positioning of Widgets
emptylabel1.grid(row=0,column=2,columnspan=5)
emptylabel3.grid(row=1,column=2,columnspan=2)
title_label.grid(row=1,column=4,columnspan=2)
emptylabel2.grid(row=2,column=0,columnspan=2)
exam_label.grid(row=3,column=4)
exam_entry.grid(row=3,column=5)
subject1_label.grid(row=5,column=4)
subject1_entry.grid(row=5,column=5)
subject2_label.grid(row=6,column=4)
subject2_entry.grid(row=6,column=5)
subject3_label.grid(row=7,column=4)
subject3_entry.grid(row=7,column=5)
subject4_label.grid(row=8,column=4)
subject4_entry.grid(row=8,column=5)
subject5_label.grid(row=9,column=4)
subject5_entry.grid(row=9,column=5)
emptylabel4.grid(row=10,column=4)
class_label.grid(row=11,column=4)
emptylabel5.grid(row=12,column=4)
class9.grid(row=13,column=4)
class10.grid(row=14,column=4)
class11.grid(row=15,column=4)
class12.grid(row=16,column=4)
emptylabel6.grid(row=17,column=4,columnspan=2)
button1.grid(row=18,column=4)
#Custom Theme
sv_ttk.set_theme('dark')
root.mainloop()

