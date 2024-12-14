import glob
import os
from typing import List, Dict, Any
from database import Database
from fileRename import rename_file_to_md5 as renameFile
from fileRename import gen_hashed_name 

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
            "comment": f"This is a media file named {name}.",
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
        file_name = os.path.basename(file_path)
        predicted_name = gen_hashed_name(file_path)
        potential_orig_file_path = os.path.join(os.path.dirname(file_path), predicted_name)
        existing_entry = self.db.get(predicted_name)  # Check if an entry with the same name exists
        
        print(bool(existing_entry), not(file_name == predicted_name))

        if existing_entry:
            # If the entry exists, check for duplicates
            if "duplicates" not in existing_entry:
                existing_entry["duplicates"] = []  # Create the duplicates key if it doesn't exist
            
            # If the current file name matches the predicted name, do not add it to duplicates
            if file_path == existing_entry["filepath"]:
                print("File already exists in the database, skipping:", file_path)
                return  # Skip processing this file as it already exists
            else:
                # Check if the current file path is already in the duplicates list
                if file_path not in existing_entry["duplicates"]:
                    existing_entry["duplicates"].append(file_path)  # Append the current file path to the duplicates list
                    print("Added to duplicates:", file_path)
        else:
            # If the entry does not exist, check if the current filename is a duplicate
            if not(file_name == predicted_name):
                
                print("This file is a probably exduplicate, and original is in the same folder, calling process file on the precited path",potential_orig_file_path)
                if os.path.exists(potential_orig_file_path):
                    self.process_file(potential_orig_file_path)
                print("calling itself again to make sure that this entry will be written as a duplicate to the original one",file_path)
                self.process_file(file_path)
                print("Skipping file as it is a duplicate:", file_path)
                return  # Skip processing this file

            # If the entry does not exist and the filename matches the predicted name, create a new entry
            new_file_path = renameFile(file_path)
            new_file_name = os.path.basename(new_file_path)
            
            if new_file_name == predicted_name:
                print("Adding a new entry")
                entry = create_entry_template(new_file_name, new_file_path)
                self.db.append(entry)  # Append the new entry to the database
            else:
                # If the new file name does not match the predicted name, treat it as a duplicate
                if "duplicates" not in existing_entry:
                    existing_entry["duplicates"] = []  # Create the duplicates key if it doesn't exist
                
                if file_path not in existing_entry["duplicates"]:
                    existing_entry["duplicates"].append(file_path)  # Append the current file path to the duplicates list
                    print("This entry is PROBABLY a duplicate of another one, skipping:", file_path)
