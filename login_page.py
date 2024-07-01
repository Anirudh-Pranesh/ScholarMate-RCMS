# IMPORT STATEMENTS
import mysql.connector
import tkinter
from tkinter import ttk
import sv_ttk
from PIL import ImageTk, Image
from tkinter import messagebox

#MySQL connection
db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db')
cur=db.cursor()

#User defined functions
def login():
    try:
        username=username_entry.get()
        password=password_entry.get()
        s="SELECT * FROM credentials WHERE username='%s' AND passkey='%s'" % (username, password)
        cur.execute(s)
        res=cur.fetchall()
        if res!=[]:
            messagebox.showinfo(title='Login success', message='You successfully logged in')
        elif username=='' or password=='':
            messagebox.showwarning(title='Invalid input', message='Please enter a username and password')
        else:
            messagebox.showerror(title='Invalid credentials', message='Please enter correct username/password')
    except:
        messagebox.showerror(title='RUNTIME ERROR', message='Unexpected error')

#Window Setup
window=tkinter.Tk()
window.title('ScholarMate - Login')
window.geometry('650x650')
frame=ttk.Frame()

#Widget setup
img = ImageTk.PhotoImage(Image.open("logo.png"))
panel=ttk.Label(frame, image=img)
login_label = ttk.Label(frame, text='Enter Your Login Details : ', font=('Arial', 23))
username_label = ttk.Label(frame, text='Username : ', font=('Arial', 20))
username_entry = ttk.Entry(frame)
password_label = ttk.Label(frame, text='Password : ', font=('Arial', 20))
password_entry = ttk.Entry(frame, show='*')
login_button = ttk.Button(frame, text='Login', command=login)

panel.grid(row=0, column=0, columnspan=10)
login_label.grid(row=1, column=4, columnspan=2, pady=10, sticky='news')
username_label.grid(row=2, column=4)
username_entry.grid(row=2, column=5, pady=20)
password_label.grid(row=3, column=4)
password_entry.grid(row=3, column=5)
login_button.grid(row=4, column=4, columnspan=2, ipady=4, ipadx=8, pady=30)
frame.pack()

sv_ttk.set_theme("dark")
frame.mainloop()