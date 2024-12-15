import glob
import os
from typing import List, Dict, Any
from database import Database
import hashlib

def gen_hashed_name(filepath):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_entry_template(name: str, filepath: str) -> Dict[str, Any]:
        """Create a template entry for the media file."""
        return {
            "name": name,
            "filepath": filepath,
            "thumbnail": {
                "small": "",
                "medium": "",
                "large": ""
            },
            "tags": {
                "General": [],
                "Meta" : [],
                "Authors": []
            },
            "comment": "",
            "CreationDate": "",
            "Source": ""
        }

class MediaScanner:
    def __init__(self, db: Database, media_extensions: List[str], excluded_dirs: List[str] = None):
        """Initialize the media scanner with a database and media file extensions."""
        self.db = db
        self.media_extensions = media_extensions
        self.excluded_dirs = excluded_dirs if excluded_dirs else ['.thumb']

    def scan_folder(self, folder_path: str) -> None:
        """Scan the specified folder recursively for media files, excluding specified directories."""
        # Create a pattern to match all files recursively
        pattern = os.path.join(folder_path, '**', '*')
        
        # Use glob to find all files matching the pattern
        all_files = glob.glob(pattern, recursive=True)
        
        # Filter out excluded directories and non-media files
        for file in all_files:
            # Check if the file is in an excluded directory
            if any(excluded in file for excluded in self.excluded_dirs):
                continue
            
            # Check if the file is a media file
            if self.is_media_file(file):
                self.process_file(file)

    def is_media_file(self, filename: str) -> bool:
        """Check if the file is a media file based on its extension."""
        return any(filename.lower().endswith(ext) for ext in self.media_extensions)

    def process_file(self, file_path: str) -> None:
        """Process the media file and create an entry in the database."""
        print("Process_file call on",file_path)
        file_name = os.path.basename(file_path)

        file_name_hashed = gen_hashed_name(file_path)
        
        existing_entry = self.db.get(file_name_hashed) 
        if existing_entry:
            if not(os.path.exists(existing_entry["filepath"])):
                existing_entry["filepath"]= file_path
                print("Original file did not exist, current one is the original now")
                return 
             
            if file_path == existing_entry["filepath"]:
                print("File already exists in the database, skipping:", file_path)
                return  # Skip processing this file as it already exists    

            if "duplicates" not in existing_entry:
                existing_entry["duplicates"] = [] # Create the duplicates key if it doesn't exist 

            if file_path not in existing_entry["duplicates"]:
                existing_entry["duplicates"].append(file_path)  # Append the current file path to the duplicates list
                print("Added to duplicates:", file_path)
            for dupliPath in existing_entry["duplicates"]:
                if not(os.path.exists(dupliPath)):
                    existing_entry["duplicates"].remove(dupliPath)
                    print("Found a non existant duplicate of file, deleted duplicate entry")
            return
      
        else:
            print("Adding a new entry")
            entry = create_entry_template(file_name_hashed, file_path)
            self.db.append(entry)  # Append the new entry to the database
        
