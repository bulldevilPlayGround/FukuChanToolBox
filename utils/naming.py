import os

def add_suffix(filename, suffix):
    file_name = '.'.join(filename.split('.')[:-1])
    file_type = filename.split('.')[-1]
    return file_name + suffix + '.' + file_type

def change_file_type(filename, new_type):
    file_name = '.'.join(filename.split('.')[:-1])
    return file_name + '.' + new_type

def refine_file_name(filename):
    # Split the path into directory and filename
    directory, base_name = os.path.split(filename)
    print(f"dir is{directory} and name is {base_name}")

    # Replace invalid Windows filename characters in the base name only
    invalid_chars = '<>:"*?|\\/'
    for char in invalid_chars:
        base_name = base_name.replace(char, '_')

    # Reconstruct the full path
    return os.path.join(directory, base_name)
