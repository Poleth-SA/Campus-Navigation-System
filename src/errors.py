import csv
from tkinter import messagebox

# Validates if the CSV contains the required columns
def validate_csv(file_path, required_columns):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            missing_columns = [col for col in required_columns if col not in reader.fieldnames]
            if missing_columns:
                raise ValueError(f"CSV is missing required columns: {missing_columns}")
        return True
    except FileNotFoundError:
        show_error(f"Error: The file '{file_path}' was not found.")
        return False
    except ValueError as e:
        show_error(str(e))
        return False
    except Exception as e:
        show_error(f"An unexpected error occurred: {str(e)}")
        return False

# Formats the path list as a string joined by " -> "
def format_path(path):
    return " -> ".join(path)

# Displays an error message in a pop-up
def show_error(message):
    messagebox.showerror("Error", message)
