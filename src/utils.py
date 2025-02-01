import os

def file_exists(file_path):
    "Check if file exists."
    return os.path.isfile(file_path)

def format_list(lst):
    """Format list for better display."""
    return ", ".join(map(str, lst)) if lst else "No records found."

