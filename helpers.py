import pathlib

def print_italic(text):
    print(f'\x1B[3m{text}\x1B[0m')

def validate_file_extension(file_path, expected_file_extension):
    file_extension = pathlib.Path(file_path).suffix
    
    if file_extension == expected_file_extension:
        return True
    
    return False
