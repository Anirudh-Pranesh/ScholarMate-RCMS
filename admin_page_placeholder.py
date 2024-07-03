#REPLACE WITH REAL ADMIN PAGE
import pickle
import tkinter
from tkinter import ttk
import sv_ttk
from subprocess import call

def edit_school_directory(): # function to assign as action command for editing school directory (list of teachers and students)
    call(['python', 'edit_school_directory.py'])
    
file=open('client_details.dat','rb')
details=pickle.load(file)
file.close()
details=list(details[0])
window=tkinter.Tk()
window.title('Admin')
window.geometry('650x650')
s='Welcome '+details[2]
label=ttk.Label(text=s)
edit_school_directory_button=ttk.Button(window, text='Edit School Directory', command=edit_school_directory)
label.pack()
edit_school_directory_button.pack()
sv_ttk.set_theme("dark")
window.mainloop()