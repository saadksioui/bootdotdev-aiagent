import os

MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
    
        if not valid_target_dir:
            raise ValueError("File path is outside the working directory")
    
        with open(target_dir, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f'Error: {str(e)}'