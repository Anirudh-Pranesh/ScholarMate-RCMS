'''
login_page.py

Simple GUI setup consisiting of an image, 2 entry fields, and 3 labels.
Python extracts data inputted in entry field and communicates this data with MySQL with the help of login() functions.
Depending on what is returned by MySQL, python verifies and checks if the login can be authorised.
SQL injections can't take place.

Once logged in, the details are stored in a binary file, named client_details. Python will check the authorisation of the client and send them to the required window.
The program for that window reads the binary file, and displays required information based one that.
Once the whole program is closed, the main login page pops up again, and the binary file is overwritten with data of person who has logged in next and the process repeats.
'''
# IMPORT STATEMENTS
import mysql.connector
from mysql.connector import Error
import tkinter
from tkinter import ttk
import sv_ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import pickle
from subprocess import call
import webbrowser

#MySQL connection
db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
#db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
cur=db.cursor()

#User defined functions
def callback(url):
   webbrowser.open_new_tab(url)
def login():
    try:
        file=open('client_details.dat', 'wb')
        username=username_entry.get()
        password=password_entry.get()
        s="SELECT * FROM credentials WHERE username='%s' AND passkey='%s'" % (username, password)
        cur.execute(s)
        res=cur.fetchall()
        if res!=[]:
            pickle.dump(res,file)
            file.close()
            db.close()
            if res[0][4]=='S':
                window.destroy()
                call(['python', 'student_page.py']) # INSERT DAVE'S GUI HERE
            elif res[0][4]=='A':
                window.destroy()
                call(['python', 'Admin_Page.py']) # INSERT DAVE'S GUI HERE
            elif res[0][4]=='T':
                window.destroy()
                call(['python', 'teacher_page.py']) # INSERT DAVE'S GUI HERE      
        elif username=='' or password=='':
            messagebox.showwarning(title='Invalid input', message='Please enter a username and password')
        else:
            messagebox.showerror(title='Invalid credentials', message='Please enter correct username/password')
    except Error as e:
        messagebox.showerror(title='RUNTIME ERROR', message=f'Unexpected error : {e}')

#Window Setup
window=tkinter.Tk()
window.title('ScholarMate - Login')
window.geometry('1000x650')
frame=ttk.Frame()
#window.attributes('-fullscreen',True) -> Activate for full screen

#Widget setup
img = ImageTk.PhotoImage(Image.open("logo.png"))
panel=ttk.Label(frame, image=img)
login_label = ttk.Label(frame, text='Enter Your Login Details : ', font=('Arial', 23))
username_label = ttk.Label(frame, text='Username : ', font=('Arial', 20))
username_entry = ttk.Entry(frame)
password_label = ttk.Label(frame, text='Password : ', font=('Arial', 20))
password_entry = ttk.Entry(frame, show='*')
login_button = ttk.Button(frame, text='Login', command=login)
helptext=ttk.Label(window, text='Having issues ? ', font=("Arial", 15))
link = tkinter.Label(window, text="Click here", fg="blue", cursor="hand2", font=("Arial", 15))
link.bind("<Button-1>", lambda e:
callback("https://github.com/Anirudh-Pranesh/ScholarMate-RCMS/issues"))

panel.grid(row=0, column=0, columnspan=10)
login_label.grid(row=1, column=4, columnspan=2, pady=10, sticky='news')
username_label.grid(row=2, column=4)
username_entry.grid(row=2, column=5, pady=20)
password_label.grid(row=3, column=4)
password_entry.grid(row=3, column=5)
login_button.grid(row=4, column=4, columnspan=2, ipady=4, ipadx=8, pady=30)
helptext.place(relx=1.0, rely=1.0, anchor="se", x=-130, y=-10)
link.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-7)
frame.pack()


sv_ttk.set_theme("dark")
frame.mainloop()