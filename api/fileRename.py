import os
import hashlib

def md5_hash_file(filepath):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def rename_media_files(folder_path):
    """Recursively rename media files in the given folder to their MD5 hash."""
    media_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webm', '.mp4', '.avi', '.mkv')  # Add more extensions as needed

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(media_extensions):
                file_path = os.path.join(root, filename)
                file_hash = md5_hash_file(file_path)
                new_filename = f"md5_{file_hash}{os.path.splitext(filename)[1]}"
                new_file_path = os.path.join(root, new_filename)

                # Rename the file
                os.rename(file_path, new_file_path)
                print(f'Renamed: {file_path} -> {new_file_path}')

# Example usage
# rename_media_files('/path/to/your/folder')
