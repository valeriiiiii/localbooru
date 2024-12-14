import os
import hashlib

def md5_hash_file(filepath):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def gen_hashed_name(file_path):
    file_hash = md5_hash_file(file_path)
    return f"{file_hash}{os.path.splitext(file_path)[1]}"

def rename_file_to_md5(file_path):
    """Rename a single media file to its MD5 hash if the new file does not already exist."""
    media_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webm', '.mp4', '.avi', '.mkv', '.webp')  # Add more extensions as needed

    if file_path.lower().endswith(media_extensions):
        new_filename = gen_hashed_name(file_path)
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

        # Check if the new file path already exists
        if not os.path.exists(new_file_path):
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f'Renamed: {file_path} -> {new_file_path}')
            return new_file_path
        else:
            print(f'Skipped renaming: {new_file_path} (already exists)')
            return file_path  # Return the original file path if renaming is skipped
    else:
        print(f'Skipped renaming: {file_path} (not a media file)')
        return file_path  # Return the original file path if not a media file


def rename_media_files(folder_path):
    """Recursively rename media files in the given folder to their MD5 hash."""
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            rename_file_to_md5(file_path)

# Example usage
# rename_media_files('/path/to/your/folder')
# rename_file_to_md5('/path/to/your/file.png')
