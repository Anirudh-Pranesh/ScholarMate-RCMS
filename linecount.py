import os

s = 0

def count_lines_in_py_files(folder_path):
    global s
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file has a .py extension and is not named 'linecount.py'
        if filename.endswith(".py") and filename != "linecount.py":
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                inside_multiline_comment = False
                line_count = 0
                for line in file:
                    stripped_line = line.strip()
                    # Check for single-line comments or empty lines
                    if stripped_line.startswith("#") or not stripped_line:
                        continue
                    
                    # Handle multiline comments (''' or """)
                    if inside_multiline_comment:
                        # Check if the current line ends the multiline comment
                        if stripped_line.endswith(("'''", '"""')):
                            inside_multiline_comment = False
                        continue
                    
                    # Check if a new multiline comment starts
                    if stripped_line.startswith(("'''", '"""')):
                        # If it also ends on the same line, skip it
                        if not (stripped_line.endswith("'''") or stripped_line.endswith('"""')) or len(stripped_line) < 6:
                            inside_multiline_comment = True
                        continue
                    
                    # Count the line if it's not a comment or empty
                    line_count += 1

            print(f"{filename}: {line_count} lines")
            s += line_count

# Replace with the path to the folder you want to check
count_lines_in_py_files('C:\\Users\\aniru\\OneDrive\\Documents\\GitHub\\ScholarMate-RCMS')
print("total lines:", s)
