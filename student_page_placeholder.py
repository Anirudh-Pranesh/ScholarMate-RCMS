#REPLACE WITH REAL STUDENT PAGE
import pickle
import tkinter
from tkinter import ttk
import sv_ttk
file=open('client_details.dat','rb')
details=pickle.load(file)
file.close()
details=list(details[0])
window=tkinter.Tk()
window.title('Student')
window.geometry('650x650')
s='Welcome '+details[2]
label=ttk.Label(text=s)
label.pack()
sv_ttk.set_theme("dark")
window.mainloop()