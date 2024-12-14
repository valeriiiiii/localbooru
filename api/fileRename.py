import os
import hashlib

def md5_hash_file(filepath):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def rename_file_to_md5(file_path):
    """Rename a single media file to its MD5 hash."""
    media_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webm', '.mp4', '.avi', '.mkv', '.webp')  # Add more extensions as needed

    if file_path.lower().endswith(media_extensions):
        file_hash = md5_hash_file(file_path)
        new_filename = f"{file_hash}{os.path.splitext(file_path)[1]}"
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

        # Rename the file
        os.rename(file_path, new_file_path)
        print(f'Renamed: {file_path} -> {new_file_path}')
    else:
        print(f'Skipped: {file_path} (not a media file)')

def rename_media_files(folder_path):
    """Recursively rename media files in the given folder to their MD5 hash."""
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            rename_file_to_md5(file_path)

# Example usage
# rename_media_files('/path/to/your/folder')
# rename_file_to_md5('/path/to/your/file.png')
