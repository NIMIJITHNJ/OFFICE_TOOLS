import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Define user credentials
user_credentials = {"nimijith": "nnj0709", "manjeri": "mji676121"}

def authenticate_user():
    # Prompt for username and password
    username = simpledialog.askstring("Login", "Enter username:")
    password = simpledialog.askstring("Login", "Enter password:", show='*')

    # Check if the credentials are valid
    if username in user_credentials and user_credentials[username] == password:
        # If valid, open the main application window
        open_main_application()
    else:
        # If invalid, show an error message and exit
        messagebox.showerror("Error", "Invalid username or password")
        exit()

def open_main_application():
    # Main application code (the rest of your existing code)
    
    def generate_text_file(input_excel, sol_id, transaction_type, transaction_category, user_remark, output_text_file):
        # Read Excel file
        df = pd.read_excel(input_excel)

        # Convert to text file
        with open(output_text_file, 'w') as txt_file:
            for index, row in df.iterrows():
                account_number = str(row['AccountNumber'])
                amount = '{:.2f}'.format(row['Amount'])
                remark = row['Remark'][:30]  # Limit to 30 characters

                if len(account_number) in [10, 12]:
                    txt_line = f"{account_number}\tINR{sol_id}{transaction_type[0]}\t\t{amount}{remark}{user_remark}\n"
                    txt_file.write(txt_line)

            # Add summary line
            summary_line = f"{sol_id}0407\tINR{sol_id}{'D' if transaction_type == 'Credit' else 'C'}\t\t{df['Amount'].sum():.2f}\t{transaction_category}{user_remark}\n"
            txt_file.write(summary_line)

    def browse_excel_file():
        file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx;*.xls")])
        excel_file_entry.delete(0, tk.END)
        excel_file_entry.insert(0, file_path)

    def browse_output_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_path)

    def generate_file():
        input_excel = excel_file_entry.get()
        sol_id = sol_id_entry.get()
        transaction_type = transaction_type_var.get()
        transaction_category = transaction_category_var.get()
        user_remark = user_remark_entry.get()
        output_text_file = output_file_entry.get()

        generate_text_file(input_excel, sol_id, transaction_type, transaction_category, user_remark, output_text_file)
        result_label.config(text="Conversion successful! Output saved to {}".format(output_text_file))
    
    # Create the main application window
    app = tk.Tk()
    app.title("HTTUM FINACLE UPLOAD FILE GENERATOR")

    # Customize the background color of the main window
    app.configure(bg="lightblue")

    # Excel File Entry
    excel_file_label = tk.Label(app, text="Select Excel File:", font=("Arial", 10), pady=5, padx=10, bg="lightblue") 
    excel_file_label.grid(row=0, column=0, pady=5, padx=10)
    excel_file_entry = tk.Entry(app, width=50)
    excel_file_entry.grid(row=0, column=1, pady=5)
    excel_file_button = tk.Button(app, text="Browse", command=browse_excel_file, font=("Arial", 10), bg="green", fg="white")
    excel_file_button.grid(row=0, column=2, pady=5, padx=10)

    # SOL ID Entry
    sol_id_label = tk.Label(app, text="Enter SOL ID:", font=("Arial", 10), pady=5, padx=10, bg="lightblue")
    sol_id_label.grid(row=1, column=0, pady=5, padx=10)
    sol_id_entry = tk.Entry(app)
    sol_id_entry.grid(row=1, column=1, pady=5)

    # Transaction Type Dropdown
    transaction_type_label = tk.Label(app, text="Select Transaction Type:", font=("Arial", 10), pady=5, padx=10, bg="lightblue")
    transaction_type_label.grid(row=2, column=0, pady=5, padx=10)
    transaction_type_options = ["Credit", "Debit"]
    transaction_type_var = tk.StringVar(app)
    transaction_type_var.set(transaction_type_options[0])  # Default value
    transaction_type_dropdown = tk.OptionMenu(app, transaction_type_var, *transaction_type_options)
    transaction_type_dropdown.grid(row=2, column=1, pady=5)

    # Transaction Category Dropdown
    transaction_category_label = tk.Label(app, text="Select Transaction Category:", font=("Arial", 10), pady=5, padx=10, bg="lightblue")
    transaction_category_label.grid(row=3, column=0, pady=5, padx=10)
    transaction_category_options = ["Salary", "Pension"]
    transaction_category_var = tk.StringVar(app)
    transaction_category_var.set(transaction_category_options[0])  # Default value
    transaction_category_dropdown = tk.OptionMenu(app, transaction_category_var, *transaction_category_options)
    transaction_category_dropdown.grid(row=3, column=1, pady=5)

    # User Remark Entry
    user_remark_label = tk.Label(app, text="Enter User Remark:", font=("Arial", 10), pady=5, padx=10, bg="lightblue")
    user_remark_label.grid(row=4, column=0, pady=5, padx=10)
    user_remark_entry = tk.Entry(app)
    user_remark_entry.grid(row=4, column=1, pady=5)

    # Output File Entry
    output_file_label = tk.Label(app, text="Save As:", font=("Arial", 10), pady=5, padx=10, bg="lightblue")
    output_file_label.grid(row=5, column=0, pady=5, padx=10)
    output_file_entry = tk.Entry(app, width=50)
    output_file_entry.grid(row=5, column=1, pady=5)
    output_file_button = tk.Button(app, text="Browse", command=browse_output_file, font=("Arial", 10), bg="green", fg="white")
    output_file_button.grid(row=5, column=2, pady=5, padx=10)

    # Generate Button
    generate_button = tk.Button(app, text="Generate Finacle File", command=generate_file, font=("Arial", 10), bg="green", fg="white")
    generate_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Result Label
    result_label = tk.Label(app, text="", font=("Arial", 10), pady=5, padx=10, bg="lightblue")
    result_label.grid(row=7, column=0, columnspan=2, pady=10)

    # Start the main loop
    app.mainloop()

# Authenticate the user before opening the main application
authenticate_user()


