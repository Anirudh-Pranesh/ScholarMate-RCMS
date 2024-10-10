import pickle
import tkinter
from tkinter import ttk
import sv_ttk

#DATABASE CONN.
#db=mysql.connector.connect(host='localhost', user='root', password='Admin@1122', database='scholarmate_db') #local host conn.
#db=mysql.connector.connect(host='mysql-336e5914-anirudhpranesh-be68.f.aivencloud.com', port=13426, user='avnadmin', password='AVNS_1UgkIMxSzsCWt0D-3cB', database='scholarmate_db') #aiven conn.

# Load student details
with open('client_details.dat', 'rb') as file:
    details = pickle.load(file)

details = list(details[0])
window = tkinter.Tk()
window.title('Student')
window.geometry('650x650')

# Welcome label
welcome_label = ttk.Label(window, text='Welcome ' + details[2], font=('Arial', 20))
welcome_label.pack(pady=20)

# Table for class and marks (for now, it's empty)
table_frame = ttk.Frame(window)
table_frame.pack(pady=20)

# Add headers
ttk.Label(table_frame, text='Subject', font=('Arial', 15), width=15).grid(row=0, column=0, padx=10)
ttk.Label(table_frame, text='Marks', font=('Arial', 15), width=15).grid(row=0, column=1, padx=10)

# Placeholder rows for future marks
for i in range(5):
    ttk.Label(table_frame, text='Subject ' + str(i+1), font=('Arial', 12)).grid(row=i+1, column=0, padx=10)
    ttk.Label(table_frame, text='-', font=('Arial', 12)).grid(row=i+1, column=1, padx=10)

# Placeholder for future graph
graph_frame = ttk.Frame(window)
graph_frame.pack(pady=20)
ttk.Label(graph_frame, text='[Bar Graph Placeholder]', font=('Arial', 12)).pack(pady=10)

# Set dark theme
sv_ttk.set_theme("dark")

# Run the application
window.mainloop()
