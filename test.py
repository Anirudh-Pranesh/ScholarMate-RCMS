import tkinter as tk
from tkinter import ttk

# Dictionary to keep track of all the entry widgets for multiple rows
edit_entries = {}

def on_double_click(event):
    global edit_entries
    
    # Identify the clicked row and column
    selected_item = treeview.identify_row(event.y)
    column = treeview.identify_column(event.x)

    if selected_item and column:
        # Get the bounds of the selected cell
        bbox = treeview.bbox(selected_item, column)
        
        if bbox:
            # Place an Entry widget over the selected cell if not already present
            if (selected_item, column) not in edit_entries:
                entry = tk.Entry(root)
                entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

                # Pre-fill the entry with the current value
                value = treeview.item(selected_item, 'values')[int(column[1]) - 1]
                entry.insert(0, value)
                entry.focus()

                # Store the entry widget in the dictionary for future reference
                edit_entries[(selected_item, column)] = entry

def confirm_changes():
    global edit_entries
    
    # Loop over all entries and update the Treeview with new values
    for (item, column), entry in edit_entries.items():
        new_value = entry.get()
        col_index = int(column[1]) - 1  # Convert column "#1", "#2", etc. to 0-based index
        values = list(treeview.item(item, 'values'))
        values[col_index] = new_value
        treeview.item(item, values=values)
        
        # Destroy the entry widget after applying changes
        entry.destroy()
    
    # Clear the dictionary after confirming changes
    edit_entries.clear()

root = tk.Tk()
root.geometry("400x200")

# Create a Treeview widget
columns = ("Name", "Age", "Grade")
treeview = ttk.Treeview(root, columns=columns, show="headings")
treeview.pack(fill=tk.BOTH, expand=True)

# Define column headings
for col in columns:
    treeview.heading(col, text=col)

# Add sample data
treeview.insert("", "end", values=("Alice", 14, "A"))
treeview.insert("", "end", values=("Bob", 15, "B"))

# Bind double-click event to start editing
treeview.bind("<Double-1>", on_double_click)

# Create a confirm button to update all rows at once
confirm_button = tk.Button(root, text="Confirm Changes", command=confirm_changes)
confirm_button.pack(pady=10)

root.mainloop()
