import pandas as pd
import glob
import os
import tkinter as tk
import xlrd
from tkinter import filedialog

# Function to execute the main logic
def execute_script():
    # Get user input from GUI
    files_path = entry_file_path.get()
    text_to_search = entry_text_search.get()
    output_path = entry_output_path.get()

    # Initialize empty lists to store file names and directory names
    file_names = []
    dir_levels = {'level_1': [], 'level_2': [], 'level_3': [], 'level_4': []}

    # Initialize an empty list to store DataFrames for each file
    dfs = []

    # Iterate through each Excel file in the specified directory and subdirectories
    for file in glob.glob(files_path, recursive=True):
        # Skip files that start with ~$
        if os.path.basename(file).startswith('~$'):
            continue

        # Determine the file extension
        file_extension = os.path.splitext(file)[-1].lower()

        # Choose the appropriate engine based on the file extension
        engine = 'openpyxl' if file_extension == '.xlsx' else 'xlrd'

        try:
            df = pd.read_excel(file, engine=engine)

            # Check if any column in the row contains the specified text
            mask = df.apply(lambda row: any(text_to_search in str(cell) for cell in row), axis=1)

            # Extract the rows that meet the condition
            df_selected_rows = df[mask]

            # Append the selected rows to the list
            dfs.append(df_selected_rows)

            # Get the relative path from the input directory and split into parts
            relative_path = os.path.relpath(file, files_path)
            path_parts = os.path.normpath(relative_path).split(os.path.sep)

            # Extract the last four levels of directory names
            levels = path_parts[-4:]

            # Append file name and directory names to the lists
            file_names.extend([os.path.basename(file)] * len(df_selected_rows))
            for i, level in enumerate(levels, start=1):
                dir_levels[f'level_{i}'].extend([level] * len(df_selected_rows))

        except Exception as e:
            print(f"Error reading file {file}: {e}")

    # Concatenate the list of DataFrames into a single DataFrame
    if dfs:
        extracted_data = pd.concat(dfs, ignore_index=True)

        # Add new columns with the file names and directory names
        extracted_data['file_name'] = file_names
        for i in range(1, 5):
            extracted_data[f'level_{i}'] = dir_levels[f'level_{i}']

        # Write the extracted data to a new Excel file
        extracted_data.to_excel(output_path, index=False)
    else:
        print("No data matching the specified condition found.")

# Create a Tkinter window
window = tk.Tk()
window.title("Excel Data Extractor")

# Create and place GUI elements
tk.Label(window, text="File Path:").grid(row=0, column=0)
entry_file_path = tk.Entry(window)
entry_file_path.grid(row=0, column=1)
tk.Button(window, text="Browse", command=lambda: entry_file_path.insert(tk.END, filedialog.askdirectory())).grid(row=0, column=2)

tk.Label(window, text="Text to Search:").grid(row=1, column=0)
entry_text_search = tk.Entry(window)
entry_text_search.grid(row=1, column=1)

tk.Label(window, text="Output Path:").grid(row=2, column=0)
entry_output_path = tk.Entry(window)
entry_output_path.grid(row=2, column=1)
tk.Button(window, text="Browse", command=lambda: entry_output_path.insert(tk.END, filedialog.asksaveasfilename(defaultextension=".xlsx"))).grid(row=2, column=2)

tk.Button(window, text="Run Script", command=execute_script).grid(row=3, column=0, columnspan=3)

# Start the Tkinter event loop
window.mainloop()
