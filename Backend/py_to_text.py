import os

def get_all_py_files(directory):
    """Return a list of all .py files in a given directory, excluding __pycache__ directories and py_to_text.py itself."""
    py_files = []
    for root, _, files in os.walk(directory):
        if '__pycache__' in root:
            continue
        for file in files:
            if file.endswith(".py") and file != "py_to_text.py":
                py_files.append(os.path.join(root, file))
    return py_files

def write_py_files_to_notepad(directory, output_file):
    """Write the contents of all .py files in a given directory to a notepad file."""
    py_files = get_all_py_files(directory)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for py_file in py_files:
            relative_path = os.path.relpath(py_file, directory)
            f.write(f"[{relative_path}]\n")
            
            with open(py_file, 'r', encoding='utf-8') as pf:
                f.write(pf.read())
            
            f.write("\n\n")

if __name__ == "__main__":
    directory = "./"  # Replace with your directory
    output_file = "py_files_contents.txt"
    write_py_files_to_notepad(directory, output_file)
    print(f"Contents written to {output_file}")
