#REPLACE WITH REAL TEACHER PAGE
import pickle
import tkinter
from tkinter import ttk
import sv_ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
#db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.
cur=db.cursor()

def save():
    try:
        file=open('client_details.dat','rb')
        details=pickle.load(file)
        file.close()
        details=list(details[0])
        old_username=details[2]
        old_pwd=details[3]
        new_username=username_entry.get()
        new_pwd=password_entry.get()
        confirm_pwd=passwordconfirm_entry.get()
        if new_pwd == confirm_pwd:
            sql = (
    "UPDATE credentials SET username=%s, passkey=%s "
    "WHERE username=%s AND passkey=%s;"
)
            cur.execute(sql, (new_username, new_pwd, old_username, old_pwd))
            db.commit()
            db.close()
            details[2]=new_username
            details[3]=new_pwd
            file=open('client_details.dat','wb')
            pickle.dump(details, file)
            file.close()
            messagebox.showinfo('Password and username changed', 'Sucessfully changed username and password')
        else:
            messagebox.showwarning('Incorrect password', 'Password entered is incorrect')
    except Error as e:
        messagebox.showerror('ERROR', f'Unexpected error : {e}')
    

window=tkinter.Tk()
frame=ttk.Frame()
window.title('Password Change')
window.geometry('650x650')
login_label = ttk.Label(frame, text='Change your username/password : ', font=('Arial', 23))
username_label = ttk.Label(frame, text='New username : ', font=('Arial', 20))
username_entry = ttk.Entry(frame)
password_label = ttk.Label(frame, text='New password : ', font=('Arial', 20))
password_entry = ttk.Entry(frame)
passwordconfirm_label = ttk.Label(frame, text='Confirm new password : ', font=('Arial', 20))
passwordconfirm_entry = ttk.Entry(frame, show='*')
save_button = ttk.Button(frame, text='Save changes', command=save)

login_label.grid(row=1, column=4, columnspan=2, pady=10, sticky='news')
username_label.grid(row=2, column=4)
username_entry.grid(row=2, column=5, pady=10)
password_label.grid(row=3, column=4)
password_entry.grid(row=3, column=5, pady=20)
passwordconfirm_label.grid(row=4, column=4)
passwordconfirm_entry.grid(row=4, column=5)
save_button.grid(row=5, column=4, columnspan=2, ipady=4, ipadx=8, pady=30)
frame.pack()

sv_ttk.set_theme("dark")
frame.mainloop()